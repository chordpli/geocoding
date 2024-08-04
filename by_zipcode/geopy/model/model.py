from decimal import Decimal


class Location:
    name: str
    latitude: Decimal
    longitude: Decimal

    def __init__(self, name: str, latitude: Decimal, longitude: Decimal):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
