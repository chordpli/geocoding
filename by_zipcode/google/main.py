import asyncio
from decimal import Decimal

import aiohttp

from by_zipcode.google.model.model import Location, Distance, ApiResult
from by_zipcode.google.secret import API_KEY


async def init_locations() -> list[Location]:
    return [
        Location("Los Angles, CA", Decimal(34.052235), Decimal(-118.243683)),
        Location("Las Vegas, NV", Decimal(36.169941), Decimal(-115.139832)),
        Location("New York, NY", Decimal(40.712776), Decimal(-74.005974)),
        Location("San Francisco, CA", Decimal(37.774929), Decimal(-122.419418)),
    ]

async def call_google_api(postal_code:str):
    URL = f"https://maps.googleapis.com/maps/api/geocode/json?components=country:US|postal_code:{postal_code}&key={API_KEY}"
    print("*" * 100)
    print(URL)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as response:
                response = await response.json()
                coordinates = response["results"][0]["geometry"]["location"]
                return coordinates
    except Exception as e:
        print(e)
        return None

# 거리 계산 함수 google api
async def calculate_distance(locations: list[Location], target_location: tuple):
    distances = []

    for location in locations:
        URL = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&mode=transit&origins={target_location[0]},{target_location[1]}&destinations={location.latitude},{location.longitude}&region=US&key={API_KEY}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(URL) as response:
                    response = await response.json()
                    api_result = ApiResult(miles=response["rows"][0]["elements"][0]["distance"]["text"], meter_value=response["rows"][0]["elements"][0]["distance"]["value"])
                    mile = api_result.meter_value/Decimal('1609.34')
                    distance = Distance(name=location.name, distance=mile, api_result=api_result)
                    distances.append(distance)
        except Exception as e:
            print(e)
            return None

    sorted_locations = sorted(distances, key=lambda x: x.distance)
    return sorted_locations


async def main():
    locations = await init_locations()
    response = await call_google_api(postal_code="77036")
    lng_ = await calculate_distance(locations, (response["lat"], response["lng"]))

    for location in lng_:
        print(f"{location.name}: {location.distance:.2f} miles")

if __name__ == "__main__":
    asyncio.run(main())
