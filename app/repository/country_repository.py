from app.repository.crud_node import create_node, create_relationship

create_country = create_node("country")
relate_country_to_region = create_relationship("country_in", "country", "region")
