from app.repository.crud_node import create_node, create_relationship

create_target = create_node("target")
relate_target_to_location = create_relationship("target_in", "target", "location")
