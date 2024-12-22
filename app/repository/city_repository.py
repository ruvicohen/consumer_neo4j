from app.repository.crud_node import create_node, create_relationship

create_city = create_node("city")
relate_city_to_country = create_relationship("city_in", "city", "country")