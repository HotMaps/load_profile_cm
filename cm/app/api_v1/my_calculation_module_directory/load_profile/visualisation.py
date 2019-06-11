import fiona
from fiona.crs import from_epsg
from collections import OrderedDict
from math import floor, log10

output_driver = "ESRI Shapefile"
schema = {
                "geometry": "LineString",
                "properties": OrderedDict([
                    ("Flow", "str"),
                    ("Temp", "str"),
                    ("Cost", "str"),
                    ("Length", "str")
                ])
                }


def round_to_n(x, n):
    length = 0
    if x > 1:
        while x > 1:
            x /= 10
            length += 1
    else:
        while x < 1:
            x *= 10
            length -= 1

    return round(x, n) * 10 ** length


def create_transmission_line_shp(transmission_lines, flows, temperatures, costs, lengths, file):
    with fiona.open(file,  "w", crs=from_epsg(4326), driver=output_driver, schema=schema) as shp:
        for transmission_line, flow, temperature, cost, length in zip(transmission_lines, flows, temperatures, costs,
                                                                      lengths):
            line = {
                "geometry": {
                    "type": "LineString",
                    "coordinates": transmission_line
                },
                "properties": OrderedDict([
                    ("Flow", str(round_to_n(flow, 3)) + " MWh/a"),
                    ("Temp", str(round_to_n(temperature, 3)) + " C"),
                    ("Cost", str(round_to_n(cost, 3)) + " Euro"),
                    ("Length", str(round_to_n(length, 3)) + " km")
                ])
            }
            shp.write(line)
