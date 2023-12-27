from domain.model.availability import Overlaps, AvailableDateTime, OverlapInterval
from domain.repository.availability_repo import AvailabilityRepo


class InMemoryAvailabilityRepo(AvailabilityRepo):

    def add_availabilities(self, user_id: str, availabilities: list[AvailableDateTime]) -> bool:
        return True

    def get_availabilities(self, user_id: str, start_date: str, end_sate: str) -> list[AvailableDateTime]:
        return [AvailableDateTime(available_date="2024-01-01", start_time="01:00:00", end_time="01:30:00")]

    def get_overlap_intervals(self, user_id1: str, user_id2: str) -> list[Overlaps]:
        i1 = OverlapInterval(available_date="2024-01-01",
                             start_overlap="01:00:00", end_overlap="01:30:00",
                             start_time1="01:00:00", end_time1="01:30:00",
                             start_time2="01:00:00", end_time2="01:30:00")
        return Overlaps(user1=user_id1, user2=user_id2, overlaps=[i1])
