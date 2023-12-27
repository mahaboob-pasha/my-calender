import unittest

from domain.model.availability import AvailableDateTime
from domain.service.availability import AvailabilityService, InvalidDataException


class TestAvailabilityService(unittest.TestCase):
    def test_validate_with_no_overlapping_intervals(self):
        svc = AvailabilityService()
        i1 = AvailableDateTime(available_date="2024-01-01", start_time="01:00:00", end_time="01:30:00")
        i2 = AvailableDateTime(available_date="2024-01-01", start_time="02:00:00", end_time="02:30:00")
        i3 = AvailableDateTime(available_date="2024-01-01", start_time="03:00:00", end_time="03:30:00")
        self.assertTrue(svc.validate([i1, i2, i3]))

    def test_validate_with_invalid_interval(self):
        svc = AvailabilityService()
        i1 = AvailableDateTime(available_date="2024-01-01", start_time="01:00:00", end_time="01:30:00")
        i2 = AvailableDateTime(available_date="2024-01-01", start_time="02:00:00", end_time="01:59:00")
        i3 = AvailableDateTime(available_date="2024-01-01", start_time="03:00:00", end_time="03:30:00")
        with self.assertRaises(InvalidDataException) as excep:
            #print("E--------", excep.exception.message)
            self.assertTrue(svc.validate([i1, i2, i3]))
        self.assertTrue('has to be lesser or equal to end time' in excep.exception.message)

    def test_validate_with_overlapping_interval(self):
        svc = AvailabilityService()
        i1 = AvailableDateTime(available_date="2024-01-01", start_time="01:00:00", end_time="01:30:00")
        i2 = AvailableDateTime(available_date="2024-01-01", start_time="02:00:00", end_time="02:59:00")
        i3 = AvailableDateTime(available_date="2024-01-01", start_time="02:10:00", end_time="03:30:00")
        with self.assertRaises(InvalidDataException) as excep:
            # print("E--------", excep.exception.message)
            self.assertTrue(svc.validate([i1, i2, i3]))
        self.assertTrue('Overlapping intervals' in excep.exception.message)


