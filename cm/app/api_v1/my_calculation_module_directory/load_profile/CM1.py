from geopy.distance import distance
import numpy as np


def temp_check(temp_source, temp_sink, condition):
    """
    function determining if source can provide heat for a sink.

    :param temp_source: temperature of the heat source.
    :type temp_source: float.
    :param temp_sink: temperature of the heat sink.
    :type temp_sink: float.
    :param condition: determines condition the temperature check uses.
    :type condition: str of following list [">", ">=", "=", "<", "<=", "!=", "true", "false"].

    :return: returns true, if source can provide heat for sink.
    :rtype: bool.
    """

    if condition == ">":
        if temp_source > temp_sink:
            return True
        else:
            return False
    elif condition == ">=":
        if temp_source > temp_sink:
            return True
        else:
            return False
    elif condition == "=":
        if temp_source == temp_sink:
            return True
        else:
            return False
    elif condition == "<=":
        if temp_source <= temp_sink:
            return True
        else:
            return False
    elif condition == "<":
        if temp_source < temp_sink:
            return True
        else:
            return False
    elif condition == "!=":
        if temp_source != temp_sink:
            return True
        else:
            return False
    elif condition == "true":
        return True
    elif condition == "false:":
        return False


def orthodrome_distance(coordinate_1, coordinate_2, ellipsoid="WGS-84"):
    """
    function computing the geodesic distance of two points on an ellipsoid (aka orthodrome).

    :param coordinate_1: (longitude, latitude) of first location.
    :type coordinate_1: tuple(float, float).
    :param coordinate_2: (longitude, latitude) of second location.
    :type coordinate_2: tuple(float, float).
    :param ellipsoid: optional ellipsoid model used for computation of distance.
    :type ellipsoid: str {"WGS-84", "GRS_80", "Airy (1830)", "Intl 1924", "Clarke (1880)", "GRS-67"}.

    :return: orthodrome length in km.
    :rtype: float.
    """

    return distance(coordinate_1, coordinate_2, ellipsoid=ellipsoid).km


def approximate_distance(coordinate_1, coordinate_2):
    """
    function computing the approximate distance of two points  with small angle approximation.

    :param coordinate_1: (longitude, latitude) of first location.
    :type coordinate_1: tuple(float, float).
    :param coordinate_2: (longitude, latitude) of second location.
    :type coordinate_2: tuple(float, float).

    :return: distance in km.
    :rtype: float.
    """

    return ((coordinate_2[0] - coordinate_1[0]) ** 2 + (coordinate_2[1] - coordinate_1[1]) ** 2)**0.5 /\
        360 * 6378.137 * 2 * np.pi


def find_neighbours(sites1, sites2, lon1_header, lat1_header, lon2_header, lat2_header, temp1_header, temp2_header,
                    max_distance, network_temp, site1_condition, site2_condition, site1_site2_condition,
                    small_angle_approximation=False):
    """
    Function searching for neighbours in a fixed search radius. Only adds the next neighbour if all temperature
    conditions are met.

    :param sites1: Dataframe containing coordinates of sites 1.
    :type sites1: pandas Dataframe
    :param sites2: Dataframe containing coordinates of sites 2.
    :type sites2: pandas Dataframe
    :param lon1_header: Column name of longitude of sites 1.
    :type lon1_header: string
    :param lat1_header: Column name of latitude of sites 1.
    :type lat1_header: string
    :param lon2_header: Column name of longitude of sites 2.
    :type lon2_header: string
    :param lat2_header: Column name of latitude of sites 2.
    :type lat2_header: string
    :param temp1_header: Column name of the temperature of sites 1.
    :type temp1_header: string
    :param temp2_header: Column name of the temperature of sites 2.
    :type temp2_header: string
    :param max_distance: Maximum distance in km for the fixed radius search.
    :type max_distance: float
    :param network_temp: Temperature of the network in °C. The site1_condition and site2_condition are in reference to
                         this network temperature.
    :type network_temp: float
    :param site1_condition: Condition the site 1 temp should fulfill in aspect to the network temp.
    :type site1_condition: str of following list [">", ">=", "=", "<", "<=", "!=", "true", "false"]
    :param site2_condition: Condition the site 2 temp should fulfill in aspect to the network temp.
    :type site2_condition: str of following list [">", ">=", "=", "<", "<=", "!=", "true", "false"]
    :param site1_site2_condition: Condition the site 1 temp should fulfill in aspect the the site 2 temp.
    :type site1_site2_condition: str of following list [">", ">=", "=", "<", "<=", "!=", "true", "false"]
    :param small_angle_approximation: Determines if small angle approximation should be used for the distance
                                      calculation.
    :type small_angle_approximation: bool
    :return: Adjacency list and distances.
    :rtype: tuple of Adjacency list and distances. Both lists have the same shape.
    """
    # get indices of columns
    lon1_ind = sites1.columns.get_loc(lon1_header)
    lat1_ind = sites1.columns.get_loc(lat1_header)
    lon2_ind = sites2.columns.get_loc(lon2_header)
    lat2_ind = sites2.columns.get_loc(lat2_header)
    temp1_ind = sites1.columns.get_loc(temp1_header)
    temp2_ind = sites2.columns.get_loc(temp2_header)

    connections = []
    distances = []
    for site1 in sites1.values:
        connections.append([])
        distances.append([])
        coordinate1 = (site1[lon1_ind], site1[lat1_ind])
        temp1 = site1[temp1_ind]
        for i, site2 in enumerate(sites2.values):
            coordinate2 = (site2[lon2_ind], site2[lat2_ind])
            temp2 = site2[temp2_ind]
            # check if source and sink are close enough
            if small_angle_approximation is False:
                dist = orthodrome_distance(coordinate1, coordinate2)
            else:
                dist = approximate_distance(coordinate1, coordinate2)
            if dist <= max_distance:
                if temp_check(temp1, network_temp, site1_condition) and \
                        temp_check(temp2, network_temp, site2_condition) and \
                        temp_check(temp1, temp2, site1_site2_condition):
                    connections[-1].append(i)
                    distances[-1].append(dist)

    return connections, distances


def create_normalized_profiles(profiles, region_header, time_header, value_header):
    """
    function normalizing profiles so that the sum of values over all time stamps of each region is 1

    :param profiles: dataframe containing profiles of different regions.
    :type profiles: pandas dataframe.
    :param region_header: header indicating the column containing the names of the regions.
    :type region_header: str.
    :param time_header: header indicating the column containing the time stamps of the profiles.
    :type time_header: str.
    :param value_header: header indicating the column containing the value of the profile.
    :type value_header: str.
    :return: list containing normalized profiles in form of numpy arrays. The keys are the region names.
    :rtype: dictionary {region_name: np.array(profile), region_name2: np.array(profile2), ...}
    """

    normalized_profiles = dict()
    regions = profiles[region_header].unique()
    for region in regions:
        profile = profiles.loc[profiles[region_header] == region]
        profile = profile.sort_values(time_header)
        profile = np.array(profile[value_header].values)
        profile = profile / np.sum(profile)
        normalized_profiles[region] = profile

    return normalized_profiles


def moving_average(array, order):
    """
    returns the moving average of the specified order.

    :param array: array of which the moving average should be computed.
    :type array: array like.
    :param order: order of moving average.
    :type order: int.
    :return: moving average of array.
    :rtype: array of same length as the input array.
    """
    return np.convolve(array, [1] * order) / order


def cost_of_connection(connection_distance, hourly_heat_flow, order=24):
    """
    function estimating the cost of transmission lines.

    :param connection_distance: distance of the pipe in meters.
    :type connection_distance: float.
    :param hourly_heat_flow: hourly heat flow in MW.
    :type hourly_heat_flow: array like.
    :param order: specifies how many hours should be used for the moving average.
    :type order: int.
    :return: cost of heat pipe in €.
    :rtype: float.
    """

    pipe_capacities = [0.2, 0.3, 0.6, 1.2, 1.9, 3.6, 6.1, 9.8, 20, 45, 75, 125, 190, 1e19]
    pipe_costs = [195, 206, 220, 240, 261, 288, 323, 357, 426, 564, 701, 839, 976, 976]
    if np.sum(hourly_heat_flow) != 0:
        capacity = np.max(moving_average(hourly_heat_flow, order))
        # create boolean array and np.argmax will return the index of the first True, hence the first pipe capacity
        # exceeding the required capacity
        pipe = int(np.argmax(pipe_capacities >= capacity))
        pipe_cost = pipe_costs[pipe]

        return pipe_cost * connection_distance * 1000
    else:
        return -1


def cost_of_heat_exchanger_source(hourly_heat_flow, order=24):
    """
    function estimating the cost of an air to liquid heat exchanger.

    :param hourly_heat_flow: hourly heat flow in MW.
    :type hourly_heat_flow: array like.
    :param order: specifies how many hours should be used for the moving average.
    :type order: int.
    :return: cost of heat exchanger in €.
    :rtype: float.
    """
    return np.max(moving_average(hourly_heat_flow, order)) * 15000


def cost_of_heat_exchanger_sink(hourly_heat_flow, order=24):
    """
    function estimating the cost of a liquid to liquid heat exchanger.

    :param hourly_heat_flow: hourly heat flow in MW.
    :type hourly_heat_flow: array like.
    :param order: specifies how many hours should be used for the moving average.
    :type order: int.
    :return: cost of heat exchanger in €.
    :rtype: float.
    """
    capacity = np.max(moving_average(hourly_heat_flow, order))

    if capacity < 1:
        return capacity * (265000 + 240000)
    else:
        return capacity * (100000 + 90000)


def cost_after_discount(cost, discount_rate, years):
    return cost * (discount_rate + 1) ** years + ((discount_rate + 1) ** years - 1) / ((discount_rate + 1) - 1)
