from domain.repository.availability_repo import AvailabilityRepo



class AvailabilityRepoFactory:
    _INSTANCE: AvailabilityRepo = None

    @classmethod
    def instance(cls) -> AvailabilityRepo:
        if cls._INSTANCE is None:
            from infrastructure.repository.postgress.availability_repo_impl import PostgressAvailabilityRepo
            cls._INSTANCE = PostgressAvailabilityRepo()
            # from infrastructure.repository.in_memory.availability_repo_impl import InMemoryAvailabilityRepo
            # cls._INSTANCE = InMemoryAvailabilityRepo()
        return cls._INSTANCE
