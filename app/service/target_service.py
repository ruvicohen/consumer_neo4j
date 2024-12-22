from app.db.model.target import Target
from app.repository.target_repository import create_target

def create_targets_nodes(targets):
    for target_name in targets:
        target_model = Target(name=target_name)
        create_target(target_model)