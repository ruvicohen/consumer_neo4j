from app.repository.crud_node import create_node, create_relationship

create_location = create_node("location")
relate_location_to_country = create_relationship("location_in", "location", "country")
