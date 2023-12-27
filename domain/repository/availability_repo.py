from abc import abstractmethod

from domain.model.availability import AvailableDateTime, Overlaps


class AvailabilityRepo:
    @abstractmethod
    def add_availabilities(self, user_id: str, availabilities: list[AvailableDateTime]) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def get_availabilities(self, user_id: str, start_date: str, end_sate: str) -> list[AvailableDateTime]:
        raise NotImplementedError()

    @abstractmethod
    def get_overlap_intervals(self, user_id1: str, user_id2: str) -> list[Overlaps]:
        raise NotImplementedError()

