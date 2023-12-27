from api.types.availability import AvailableDateTime as _AvailableDateTime
from api.types.availability import OverlapInterval as _OverlapInterval
from api.types.availability import Overlaps as _Overlaps

# ideally we should have DTOs and Domain models separate, and SerDe(serializer-deserializer) will do the transformation
# since it's the simple app keeping both of them same
# also there is no separate data-model as well
AvailableDateTime = _AvailableDateTime
OverlapInterval = _OverlapInterval
Overlaps = _Overlaps
