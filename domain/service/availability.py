from collections import defaultdict
from datetime import datetime
from domain.model.availability import AvailableDateTime


class InvalidDataException(Exception):
    def __init__(self, message="Invalid data"):
        self.message = message
        super().__init__(self.message)


class AvailabilityService:
    @classmethod
    def instance(cls):
        return AvailabilityService()

    def validate(self, availabilities:list[AvailableDateTime]) -> bool:
        # validate for no overlapping timestamp

        TIME_FORMAT = "%H:%M:%S"

        # group by date, then find overlapping timestamps
        map_by_dates = defaultdict(list)
        for a in availabilities:
            st = datetime.strptime(a.start_time, TIME_FORMAT)
            ed = datetime.strptime(a.end_time, TIME_FORMAT)
            if ed < st:
                raise InvalidDataException(f"Start time '{a.start_time}' has to be lesser or equal to end time '{a.end_time}'")
            map_by_dates[a.available_date].append((st, ed))

        # now for given date, check for overlapping time
        # sort them first
        for avail_date, timestamps in map_by_dates.items():
            timestamps.sort()
            overlapping_ts = self._validate_overlapping(timestamps)
            if overlapping_ts is not None:
                def str_ts(ts):
                    start, end = ts
                    return start.strftime(TIME_FORMAT)+"-"+end.strftime(TIME_FORMAT)
                raise InvalidDataException(f"Overlapping intervals {str_ts(overlapping_ts[0])} and {str_ts(overlapping_ts[1])} for date {avail_date}")
        return True

    def _validate_overlapping(self, ts: list[tuple[datetime, datetime]]) -> list[tuple[datetime, datetime]]:
        # return overlapping [tuple1, tuple2] as list
        prevts = ts[0]
        for ts in ts[1:]:
            s2 = ts[0]
            s1, e1 = prevts
            if s1 <= s2 < e1:
                return [prevts, ts]
            prevts = ts
        return None

