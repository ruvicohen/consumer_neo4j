from app.db.model.city import City
from app.db.model.country import Country
from app.repository.country_repository import create_country
from app.repository.crud_node import create_node, create_relationship

create_city = create_node("city")
relate_city_to_country = create_relationship("city_in", "city", "country")

# city = City(name="London")
# a = create_city(city)
# print(a)
#
# country = Country(name="England")
# b = create_country(country)
# print(b)
#
# c = relate_city_to_country(int(a.value_or(None)["id"]), int(b.value_or(None)["id"]))
# print(c)