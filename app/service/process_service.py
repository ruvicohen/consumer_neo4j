from app.db.model.country import Country
from app.db.model.location import Location
from app.repository.country_repository import create_country
from app.repository.location_repository import (
    create_location,
    relate_location_to_country,
)
from app.service.terror_group_service import create_groups_targets_relationships


def process_event(event):
    country_model = Country(name=event["location"].get("country"))
    country = create_country(country_model).value_or(None)
    country_id = country["id"] if country else None
    location_model = Location(
        latitude=event["location"].get("latitude"),
        longitude=event["location"].get("longitude"),
    )
    location = create_location(location_model).value_or(None)
    location_id = location["id"] if location else None
    if location_id and country_id:
        relate_location_to_country(int(location_id), int(country_id))
    groups_involved = event.get("groups_involved", [])
    target_type = event.get("target_type", [])
    attack_type = event.get("attack_type", [])
    create_groups_targets_relationships(
        groups_involved, target_type, attack_type, location_id
    )
    # event_model = Event(fatalities=event["casualties"].get('fatalities', 0), injuries=event["casualties"].get('injuries', 0), score=event["casualties"].get('score', 0))
    # event_inserted = create_event(event_model).value_or(None)
    # event_id = event_inserted["id"] if event_inserted else None
    # if event_id and location_id:
    #     relate_event_to_location(int(event_id), int(location_id))
    # create_terror_groups_nodes(event.get('groups_involved', []), event_id)
    # create_targets_nodes(event.get('target_type', []), event_id)
    # create_attack_types_nodes(event.get('attack_type', []), event_id)
