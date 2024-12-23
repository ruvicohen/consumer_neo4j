from app.repository.crud_node import create_node, create_relationship

create_terror_group = create_node("terror_group")
relate_target_to_group = create_relationship("attack", "terror_group", "target")
