from app.db.model.location import Location
from app.repository.location_repository import create_location
from app.service.target_service import create_targets_nodes
from app.service.terror_group_service import create_terror_groups_nodes


def create_attack_type_nodes(param):
    pass


def process_event(event):
    create_terror_groups_nodes(event.get('groups_involved', []))
    create_targets_nodes(event.get('target_type', []))
    create_attack_type_nodes(event.get('attack_type', []))
    location_model = Location(latitude=event['location'].get('latitude'), longitude=event['location'].get('longitude'))
    create_location(location_model)
    

    # יצירת קשרים
    link_event_to_groups(event)
    link_event_to_location(event)
    link_event_to_target(event)
    link_event_to_attack_type(event)
