from injectable import injectable


@injectable(qualifier="MEASURING_SERVICE", namespace="US")
class UnitedStatesMeasuringService:
    def earth_to_sun_distance(self):
        return "94.06 million miles"
