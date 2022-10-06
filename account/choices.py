import pycountry 
from operator import itemgetter

country_list = sorted(
  [(country.name, country.name) for country in list(pycountry.countries)], 
  key=itemgetter(0)
)

country_list.insert(0, ("*Select country", "*Select country"))

COUNTRIES = country_list