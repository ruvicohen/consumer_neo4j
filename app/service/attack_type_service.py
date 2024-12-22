from app.db.model.attack_type import AttackType
from app.repository.attack_type_repository import create_attack_type

def create_attack_types_nodes(attack_type_list: list):
    for attack_type in attack_type_list:
        attack_model = AttackType(name=attack_type)
        create_attack_type(attack_model)