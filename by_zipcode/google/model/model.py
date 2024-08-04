from decimal import Decimal


class Location:
    name: str
    latitude: Decimal
    longitude: Decimal

    def __init__(self, name: str, latitude: Decimal, longitude: Decimal):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude


class ApiResult:
    miles: str
    meter_value: int

    def __init__(self, miles: str, meter_value: int):
        self.miles = miles
        self.meter_value = meter_value


class Distance:
    name: str
    distance: Decimal
    api_result: ApiResult

    def __init__(self, name: str, distance: Decimal, api_result: ApiResult):
        self.name = name
        self.distance = distance
        self.api_result = api_result
