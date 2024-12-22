from typing import List
from app.db.model.terror_group import TerrorGroup
from app.repository.event_repository import relate_event_to_group
from app.repository.terror_group_repository import create_terror_group

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
        relate_event_to_group(int(event_id), int(terror_group_id["id"]))