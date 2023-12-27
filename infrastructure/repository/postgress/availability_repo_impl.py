from typing import Optional

import psycopg2
from psycopg2 import pool
from psycopg2.extras import execute_values
from domain.model.availability import Overlaps, AvailableDateTime, OverlapInterval
from domain.repository.availability_repo import AvailabilityRepo


class PostgressAvailabilityRepo(AvailabilityRepo):
    pool = psycopg2.pool.SimpleConnectionPool(
        2, 3, user='postgres', password='mpasha',
        host='localhost', port='5432', database='test'
    )

    def add_availabilities(self, user_id: str, availabilities: list[AvailableDateTime]) -> bool:
        data = [a.to_tuple(user_id) for a in availabilities]
        sql = "INSERT INTO availability1 (user_id, availability_date, start_time, end_time) VALUES %s"
        try:
            connection = PostgressAvailabilityRepo.pool.getconn()
            cursor = connection.cursor()
            execute_values(cursor, sql, data)
            connection.commit()
        finally:
            cursor.close()
            PostgressAvailabilityRepo.pool.putconn(connection)
        return True

    def get_availabilities(self, user_id: str, start_date: Optional[str]=None, end_date: Optional[str]=None) -> list[AvailableDateTime]:
        connection = PostgressAvailabilityRepo.pool.getconn()
        cursor = connection.cursor()
        if start_date and end_date:
            cursor.execute(f'SELECT user_id, availability_date, start_time, end_time FROM availability1 WHERE user_id={user_id} AND availability_date BETWEEN {start_date} AND {end_date}')
        else:
            cursor.execute(f'SELECT user_id, availability_date, start_time, end_time FROM availability1 WHERE user_id={user_id}')
        results = cursor.fetchall()
        data = []
        try:
            data = [AvailableDateTime(str(d[1]), str(d[2]), str(d[3])) for d in results]
        finally:
            cursor.close()
            PostgressAvailabilityRepo.pool.putconn(connection)
        return data

    def get_overlap_intervals(self, user_id1: str, user_id2: str) -> list[Overlaps]:
        ovarlap_raw_query = f"""WITH overlapping_interval AS (
        SELECT
            a1.user_id AS user_id1,
        	a2.user_id AS user_id2,
            a1.availability_date AS availability_date,
        	CASE WHEN a1.start_time  < a2.start_time THEN a2.start_time ELSE a1.start_time END as start_overlap,
        	CASE WHEN a1.end_time  < a2.end_time THEN a1.end_time ELSE a2.end_time END as end_overlap,
            a1.start_time AS start_time1,
            a1.end_time AS end_time1,
            a2.start_time AS start_time2,
            a2.end_time AS end_time2
        FROM
            public.availability1 a1
        JOIN
            public.availability1 a2
        ON
            a1.availability_date = a2.availability_date
            AND (
                (a1.start_time BETWEEN a2.start_time AND a2.end_time)
                OR (a1.end_time BETWEEN a2.start_time AND a2.end_time)
                OR (a2.start_time BETWEEN a1.start_time AND a1.end_time)
                OR (a2.end_time BETWEEN a1.start_time AND a1.end_time)
            )
        WHERE a1.user_id={user_id1} AND a2.user_id={user_id2}
        ) 
        SELECT availability_date, start_overlap, end_overlap, start_time1, end_time1, start_time2, end_time2 FROM overlapping_interval"""

        connection = PostgressAvailabilityRepo.pool.getconn()
        cursor = connection.cursor()
        cursor.execute(ovarlap_raw_query)
        results = cursor.fetchall()
        data = []
        try:
            data = [OverlapInterval(str(dt), str(so), str(eo), str(s1), str(e1), str(s2), str(e2)) for dt, so, eo, s1, e1, s2, e2 in results]
        finally:
            cursor.close()
            PostgressAvailabilityRepo.pool.putconn(connection)
        return Overlaps(user1=user_id1, user2=user_id2, overlaps=data)