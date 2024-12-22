from app.repository.crud_node import create_node1, create_relationship

create_event = create_node1("event")
relate_event_to_location = create_relationship("event_in", "event", "location")
relate_event_to_group = create_relationship("involved", "event", "terror_group")
relate_event_to_type_attack = create_relationship("used", "event", "attack_type")
relate_event_to_target = create_relationship("targeted", "event", "target")