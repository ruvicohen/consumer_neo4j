from dataclasses import asdict
from typing import List

from app.db.model.attack_type import AttackType
from app.db.model.target import Target
from app.db.model.terror_group import TerrorGroup
from app.repository.target_repository import create_target, relate_target_to_location
from app.repository.terror_group_repository import (
    create_terror_group,
    relate_target_to_group,
)


def create_terror_groups_nodes(terror_groups: List, event_id):
    print(300)
    print(terror_groups)
    for terror_group_name in terror_groups:
        group_model = TerrorGroup(name=terror_group_name)
        terror_group_id = create_terror_group(group_model).value_or(None)
        print(23)
        print(terror_group_id)
        print(event_id)
        if terror_group_id is None or event_id is None:
            print(event_id)
            return
        print(24)
        relate_target_to_group(int(event_id), int(terror_group_id["id"]))


def create_groups_targets_relationships(
    terror_groups: List, targets: List, attack_type_list: List, location_id
):
    for terror_group_name in terror_groups:
        group_model = TerrorGroup(name=terror_group_name)
        terror_group_id = create_terror_group(group_model).value_or(None)
        for target_name in targets:
            target_model = Target(name=target_name)
            target_id = create_target(target_model).value_or(None)
            if target_id and location_id:
                relate_target_to_location(int(target_id["id"]), int(location_id))
            if attack_type_list:
                for attack_type in attack_type_list:
                    attack_model = AttackType(name=attack_type)
                    if terror_group_id and target_id:
                        a = relate_target_to_group(
                            int(terror_group_id["id"]),
                            int(target_id["id"]),
                            asdict(attack_model),
                        )
                        print(a)
