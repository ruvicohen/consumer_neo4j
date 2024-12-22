from app.db.model.city import City
from app.db.model.country import Country
from app.db.model.event import Event
from app.db.model.location import Location
from app.db.model.region import Region
from app.repository.city_repository import create_city, relate_city_to_country
from app.repository.country_repository import create_country, relate_country_to_region
from app.repository.event_repository import create_event, relate_event_to_location
from app.repository.location_repository import create_location, relate_location_to_city
from app.repository.region_repository import create_region
from app.service.attack_type_service import create_attack_types_nodes
from app.service.target_service import create_targets_nodes
from app.service.terror_group_service import create_terror_groups_nodes


def process_event(event):
    region_model = Region(name=event['location'].get("region"))
    region = create_region(region_model).value_or(None)
    region_id = region["id"] if region else None
    country_model = Country(name=event['location'].get("country"))
    country = create_country(country_model).value_or(None)
    country_id = country["id"] if country else None
    if region_id and country_id:
        relate_country_to_region(int(country_id), int(region_id))
    city_model = City(name=event['location'].get("city"))
    city = create_city(city_model).value_or(None)
    city_id = city["id"] if city else None
    if city_id and country_id:
        relate_city_to_country(int(city_id), int(country_id))
    location_model = Location(latitude=event['location'].get('latitude'), longitude=event['location'].get('longitude'))
    location = create_location(location_model).value_or(None)
    location_id = location["id"] if location else None
    if location_id and city_id:
        relate_location_to_city(int(location_id), int(city_id))
    event_model = Event(fatalities=event["casualties"].get('fatalities', 0), injuries=event["casualties"].get('injuries', 0), score=event["casualties"].get('score', 0))
    event_inserted = create_event(event_model).value_or(None)
    event_id = event_inserted["id"] if event_inserted else None
    if event_id and location_id:
        relate_event_to_location(int(event_id), int(location_id))
    create_terror_groups_nodes(event.get('groups_involved', []), event_id)
    create_targets_nodes(event.get('target_type', []), event_id)
    create_attack_types_nodes(event.get('attack_type', []), event_id)
