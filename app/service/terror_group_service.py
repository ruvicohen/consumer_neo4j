from typing import List
from app.db.model.terror_group import TerrorGroup
from app.repository.terror_group_repository import create_terror_group

def create_terror_groups_nodes(terror_groups: List):
    for terror_group_name in terror_groups:
        group_model = TerrorGroup(name=terror_group_name)
        create_terror_group(group_model)