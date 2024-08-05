from examples.namespaces.measuring_service_abc import MeasuringService
from injectable import injectable


@injectable(namespace="INTL")
class InternationalMeasuringService(MeasuringService):
    def earth_to_sun_distance(self):
        return "151.38 million km"
