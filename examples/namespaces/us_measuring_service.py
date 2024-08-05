from examples.namespaces.measuring_service_abc import MeasuringService
from injectable import injectable


@injectable(namespace="US")
class UnitedStatesMeasuringService(MeasuringService):
    def earth_to_sun_distance(self):
        return "94.06 million miles"
