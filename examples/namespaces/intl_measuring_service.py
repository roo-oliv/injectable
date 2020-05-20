from injectable import injectable


@injectable(qualifier="MEASURING_SERVICE", namespace="INTL")
class InternationalMeasuringService:
    def earth_to_sun_distance(self):
        return "151.38 million km"
