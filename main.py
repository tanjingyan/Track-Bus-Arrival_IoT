from lta_api import get_bus_arrivals
from display import display_bus_info

data = get_bus_arrivals(YOUR_BUS_CODE)

display_bus_info(data)