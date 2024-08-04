import asyncio
import ssl
from decimal import Decimal
from typing import Tuple

import certifi
from geopy import Point
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from by_zipcode.geopy.model.model import Location

BEVERLY_HILLS_ZIP_CODE = "90210"


async def init_locations() -> list[Location]:
    return [
        Location("Los Angles, CA", Decimal(34.052235), Decimal(-118.243683)),
        Location("Las Vegas, NV", Decimal(36.169941), Decimal(-115.139832)),
        Location("New York, NY", Decimal(40.712776), Decimal(-74.005974)),
        Location("San Francisco, CA", Decimal(37.774929), Decimal(-122.419418)),
    ]


async def get_from_zip_code(zip_code: str) -> Tuple[float, float] | None:
    # 배포 환경에서 Certification 처리를 어떻게 해야 하는지 확인이 필요.
    ctx = ssl.create_default_context(cafile=certifi.where())
    geolocator = Nominatim(user_agent="zip_code_locator", ssl_context=ctx)

    try:
        """
        `street`, `city`, `county`, `state`, `country`, or `postalcode`
        를 매개변수로 받아 해당 위치의 위도와 경도를 반환합니다.
        """
        location: Point = geolocator.geocode(zip_code, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            raise Exception("해당 ZIP 코드에 대한 위치를 찾을 수 없습니다: " + zip_code)

    except GeocoderTimedOut:
        print("서비스 시간 초과. 다시 시도해주세요.")
        return None


async def main():
    locations = await init_locations()
    target_location = await get_from_zip_code(BEVERLY_HILLS_ZIP_CODE)
    print(f"ZIP 코드 {BEVERLY_HILLS_ZIP_CODE}의 위도와 경도는 {target_location}입니다.")

    distances = []
    for location in locations:
        """
        geodesic() 함수는 두 지점 사이의 거리를 계산합니다.
        이 함수는 두 지점의 위도와 경도를 인자로 받으며, 튜플 형태로 받습니다.
        """
        distance = geodesic(
            target_location, (location.latitude, location.longitude)
        ).miles
        distances.append((location.name, distance))

    sorted_locations = sorted(distances, key=lambda x: x[1])

    print("ZIP 코드로부터 거리순으로 정렬된 위치들:")
    for name, distance in sorted_locations:
        print(f"{name}: {distance:.2f} miles")


if __name__ == "__main__":
    asyncio.run(main())
