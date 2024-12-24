from dataclasses import asdict
from typing import List
from app.db.model.attack_type import AttackType
from app.db.model.target import Target
from app.db.model.terror_group import TerrorGroup
from app.db.model.location import Location
from app.db.model.country import Country
from app.repository.target_repository import create_target, relate_target_to_location
from app.repository.terror_group_repository import (
    create_terror_group,
    relate_target_to_group,
)
from app.repository.country_repository import create_country
from app.repository.location_repository import create_location, relate_location_to_country

def process_event(event):
    country_id = process_country(event)
    location_id = process_location(event)

    if location_id and country_id:
        relate_location_to_country(int(location_id), int(country_id))

    groups_involved = event.get("groups_involved", [])
    target_type = event.get("target_type", [])
    attack_type = event.get("attack_type", [])

    create_groups_targets_relationships(groups_involved, target_type, attack_type, location_id)

def process_country(event):
    country_name = event["location"].get("country")
    if not country_name:
        return None

    country_model = Country(name=country_name)
    country = create_country(country_model).value_or(None)
    return country["id"] if country else None

def process_location(event):
    latitude = event["location"].get("latitude")
    longitude = event["location"].get("longitude")

    if latitude is None or longitude is None:
        return None

    location_model = Location(latitude=latitude, longitude=longitude)
    location = create_location(location_model).value_or(None)
    return location["id"] if location else None

def create_groups_targets_relationships(terror_groups: List, targets: List, attack_type_list: List, location_id):
    for terror_group_name in terror_groups:
        terror_group_id = create_terror_group_node(terror_group_name)
        for target_name in targets:
            target_id = create_target_node(target_name)
            if target_id and location_id:
                relate_target_to_location(int(target_id), int(location_id))
            create_attack_relationships(terror_group_id, target_id, attack_type_list)

def create_terror_group_node(terror_group_name):
    if not terror_group_name:
        return None

    group_model = TerrorGroup(name=terror_group_name)
    terror_group = create_terror_group(group_model).value_or(None)
    return terror_group["id"] if terror_group else None

def create_target_node(target_name):
    if not target_name:
        return None

    target_model = Target(name=target_name)
    target = create_target(target_model).value_or(None)
    return target["id"] if target else None

def create_attack_relationships(terror_group_id, target_id, attack_type_list):
    if not terror_group_id or not target_id or not attack_type_list:
        return

    for attack_type in attack_type_list:
        attack_model = AttackType(name=attack_type)
        relate_target_to_group(
            int(terror_group_id),
            int(target_id),
            asdict(attack_model),
        )
