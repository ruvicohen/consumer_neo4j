from typing import List

from app.db.model.target import Target
from app.repository.event_repository import relate_event_to_target
from app.repository.target_repository import create_target

def create_targets_nodes(targets: List, event_id):
    print(200)
    print(targets)
    for target_name in targets:
        print(target_name)
        target_model = Target(name=target_name)
        target_id = create_target(target_model).value_or(None)
        if target_id is None or event_id is None:
            return
        relate_event_to_target(int(event_id), int(target_id["id"]))