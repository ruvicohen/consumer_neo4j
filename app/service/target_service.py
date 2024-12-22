from typing import List

from app.db.model.target import Target
from app.repository.event_repository import relate_event_to_target
from app.repository.target_repository import create_target

def create_targets_nodes(targets: List, event_id):
    for target_name in targets:
        target_model = Target(name=target_name)
        target_id = create_target(target_model)
        relate_event_to_target(target_id, event_id)