from app.db.model.city import City
from app.db.model.country import Country
from app.db.model.event import Event
from app.db.model.location import Location
from app.db.model.region import Region
from app.repository.city_repository import create_city, relate_city_to_country
from app.repository.country_repository import create_country, relate_country_to_region
from app.repository.event_repository import create_event, relate_event_to_location
from app.repository.location_repository import create_location
from app.repository.region_repository import create_region
from app.service.attack_type_service import create_attack_types_nodes
from app.service.target_service import create_targets_nodes
from app.service.terror_group_service import create_terror_groups_nodes


def process_event(event):
    region_model = Region(name=event['location'].get("region"))
    region_id = create_region(region_model)
    country_model = Country(name=event['location'].get("country"))
    country_id = create_country(country_model)
    relate_country_to_region(country_id, region_id)
    city_model = City(name=event['location'].get("city"))
    city_id = create_city(city_model)
    relate_city_to_country(city_id, country_id)
    location_model = Location(latitude=event['location'].get('latitude'), longitude=event['location'].get('longitude'))
    location_id = create_location(location_model)
    event_model = Event(fatalities=event["casualties"].get('fatalities', 0), injuries=event["casualties"].get('injuries', 0), score=event["casualties"].get('score', 0))
    event_id = create_event(event_model)
    relate_event_to_location(event_id, location_id)
    create_terror_groups_nodes(event.get('groups_involved', []), event_id)
    create_targets_nodes(event.get('target_type', []), event_id)
    create_attack_types_nodes(event.get('attack_type', []), event_id)
