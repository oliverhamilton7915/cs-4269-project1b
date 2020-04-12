import heapq
import math
from copy import deepcopy


class Country:
    def __init__(self, name, resource_dict, resource_info):
        self.name = name
        self.resource_info = resource_info
        self.resource_dict = resource_dict
        created_resources = ["PopulationWaste",
                             "MetallicAlloys",
                             "MetallicAlloysWaste",
                             "Electronics",
                             "ElectronicsWaste",
                             "Housing",
                             "HousingWaste"]
        for created in created_resources:
            self.resource_dict[created] = 0
        self.start_quality = self.get_state_quality()

    def get_undiscounted_reward(self):
        return self.get_state_quality() - self.start_quality

    def get_discounted_reward(self, gamma, N):
        return (gamma ** N) * self.get_undiscounted_reward()

    def get_state_quality(self):
        return sum([value * self.resource_info[key]['weight'] * self.resource_info[key]['factor']
                    for (key, value) in self.resource_dict.items()]) / float(1 + self.resource_dict['Population'])

    def print_self(self):
        resource_str = self.name + ": "
        for r, v in self.resource_dict.items():
            resource_str += r + ": " + str(v) + " "
        print(resource_str + "quality: " + str(self.get_state_quality()))


class World:
    def __init__(self, countries):
        self.C = -0.1  # cost of proposing a schedule!
        self.countries = countries
        self.history = []  # this will store tuples of (action, reward) pairs
        self.EU = 0

    def __lt__(self, other):
        # higher EU <-lesser ordering <- higher priority in queue
        return self.EU > other.EU

    def get_country_index(self, country_name):
        for i in range(len(self.countries)):
            if self.countries[i].name == country_name:
                return i
        return -1

    def generate_successors(self, country_name, templates):
        bins = [1, 5, 10, 25, 100]
        suc = []
        (alloy_temp, electronics_temp, housing_temp, transfer_temp) = templates
        transform_templates = {(("Population", 1), ("MetallicElements", 2)):
                                   (("Population", 1), ("MetallicAlloys", 1), ("MetallicAlloysWaste", 1)),
                               (("Population", 3), ("MetallicElements", 2), ("MetallicAlloys", 2)):
                                   (("Electronics", 2), ("ElectronicsWaste", 2), ("Population", 3)),
                               (("Population", 5), ("MetallicElements", 1), ("Timber", 5), ("MetallicAlloys", 3)):
                                   (("Population", 5), ("Housing", 1), ("HousingWaste", 1))}

        deepcopy_world = deepcopy(self)
        country_index = self.get_country_index(country_name)

        # Transform template
        for size in bins:
            for (inputs, outputs) in transform_templates.items():
                lacks_enough = False
                for (resource, amt) in inputs:
                    if size * amt > self.countries[country_index].resource_dict[resource]:
                        lacks_enough = True
                if lacks_enough:
                    continue
                else:
                    # country_name has enough resources to satisfy this transform operation
                    successor_world = deepcopy_world
                    deepcopy_world = deepcopy(deepcopy_world)
                    for (resource, amt) in inputs:
                        successor_world.countries[country_index].resource_dict[resource] -= size * amt
                    for (resource, amt) in outputs:
                        successor_world.countries[country_index].resource_dict[resource] += size * amt

                    # Since there is NO uncertainty in this operation
                    EU = successor_world.countries[country_index].get_discounted_reward(0.9, len(self.history) + 1)
                    # using alloy temp
                    input_dict = {key:val for (key, val) in inputs}
                    output_dict = {key:val for (key, val) in outputs}
                    if ('MetallicAlloys', 1) in outputs:
                        formatted_template = alloy_temp.format(country_name,
                                                               input_dict['Population'],
                                                               input_dict['MetallicElements'],
                                                               output_dict['Population'],
                                                               output_dict['MetallicAlloys'],
                                                               output_dict['MetallicAlloysWaste'])
                    # using electronics temp
                    elif ('Electronics', 2) in outputs:
                        formatted_template = electronics_temp.format(country_name,
                                                                     input_dict['Population'],
                                                                     input_dict['MetallicElements'],
                                                                     input_dict['MetallicAlloys'],
                                                                     output_dict['Electronics'],
                                                                     output_dict['ElectronicsWaste'],
                                                                     output_dict['Population'])
                    # using housing temp
                    else:
                        formatted_template = housing_temp.format(country_name,
                                                                 input_dict['Population'],
                                                                 input_dict['MetallicElements'],
                                                                 input_dict['Timber'],
                                                                 input_dict['MetallicAlloys'],
                                                                 output_dict['Population'],
                                                                 output_dict['Housing'],
                                                                 output_dict['HousingWaste'])
                    successor_world.history.append((formatted_template, EU))
                    successor_world.EU = EU
                    suc.append(successor_world)

        # Transfer Template (1) -- when someone is transferring something to our country
        for first_ind in range(len(self.countries)):
            if first_ind != country_index:
                for size in bins:
                    for resource_given in self.countries[first_ind].resource_dict.keys():
                        for resource_received in self.countries[country_index].resource_dict.keys():
                            if resource_given != resource_received:
                                 if self.countries[first_ind].resource_dict[resource_given] > size:
                                    if self.countries[country_index].resource_dict[resource_received] > size:
                                        successor_world = deepcopy_world
                                        deepcopy_world = deepcopy(deepcopy_world)
                                        first = successor_world.countries[first_ind]
                                        country = successor_world.countries[country_index]
                                        first.resource_dict[resource_given] -= size
                                        country.resource_dict[resource_received] += size
                                        first.resource_dict[resource_received] -= size
                                        country.resource_dict[resource_given] += size
                                        DR = first.get_discounted_reward(0.9, len(self.history) + 1)
                                        probability_accept = 1.0 / (1.0 + math.exp(-1 * DR))
                                        EU = probability_accept * country.get_discounted_reward(0.9, len(self.history) + 1) + (1 - probability_accept) * self.C
                                        formatted_template = '(TRANSFER {} {} ({} {}) ({} {}))'.format(
                                            first.name,
                                            country_name,
                                            resource_given,
                                            size,
                                            resource_received,
                                            size)
                                        successor_world.history.append((formatted_template, EU))
                                        successor_world.EU = EU
                                        suc.append(successor_world)

        # Transfer Template (2) -- when our country is transferring something to another country
        for second_ind in range(len(self.countries)):
            if second_ind != country_index:
                for size in bins:
                    for resource_given in self.countries[country_index].resource_dict.keys():
                        for resource_received in self.countries[second_ind].resource_dict.keys():
                            if resource_given != resource_received:
                                if self.countries[country_index].resource_dict[resource_given] > size:
                                     if self.countries[second_ind].resource_dict[resource_received] > size:
                                        successor_world = deepcopy_world
                                        deepcopy_world = deepcopy(deepcopy_world)
                                        second = successor_world.countries[second_ind]
                                        country = successor_world.countries[country_index]
                                        second.resource_dict[resource_given] += size
                                        country.resource_dict[resource_received] += size
                                        second.resource_dict[resource_received] -= size
                                        country.resource_dict[resource_given] -= size
                                        DR = second.get_discounted_reward(0.9, len(self.history) + 1)
                                        probability_accept = 1.0 / (1.0 + math.exp(-1 * DR))
                                        EU = probability_accept * country.get_discounted_reward(0.9, len(self.history) + 1) + (1 - probability_accept) * self.C
                                        formatted_template = '(TRANSFER {} {} ({} {}) ({} {}))'.format(
                                            country_name,
                                            second.name,
                                            resource_given,
                                            size,
                                            resource_received,
                                            size)
                                        successor_world.history.append((formatted_template, EU))
                                        successor_world.EU = EU
                                        suc.append(successor_world)

        heapq.heapify(suc)
        return suc

    def print_world(self):
        print("Current World State: ")
        for c in self.countries:
            c.print_self()
        print()
