from typing import List
from app.db.model.terror_group import TerrorGroup
from app.repository.event_repository import relate_event_to_group
from app.repository.terror_group_repository import create_terror_group

def create_terror_groups_nodes(terror_groups: List, event_id):
    for terror_group_name in terror_groups:
        group_model = TerrorGroup(name=terror_group_name)
        terror_group_id = create_terror_group(group_model)
        relate_event_to_group(event_id, terror_group_id)