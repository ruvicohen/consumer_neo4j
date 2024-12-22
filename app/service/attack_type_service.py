from typing import List
from app.db.model.attack_type import AttackType
from app.repository.attack_type_repository import create_attack_type
from app.repository.event_repository import relate_event_to_type_attack


def create_attack_types_nodes(attack_type_list: List, event_id):
    for attack_type in attack_type_list:
        attack_model = AttackType(name=attack_type)
        attack_type_id = create_attack_type(attack_model)
        relate_event_to_type_attack(event_id, attack_type_id)