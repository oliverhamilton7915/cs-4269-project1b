import heapq
from copy import deepcopy

# population is 0, regular resources are 1, created resources are 2, and waste is -1
RESOURCE_WEIGHTS = {
    "r1": 0,
    "r2": 1.0,
    "r3": 1.0,
    "r21": 6.0,
    "r22": 5.5,
    "r23": 19.0,
    "r21\'": -0.5,
    "r22\'": -1,
    "r23\'": -0.5
}


class Country:
    def __init__(self, name, resources_dict):
        self.name = name
        self.resource_dict = resources_dict
        created_resources = ["r21", "r21\'", "r22", "r22\'", "r23", "r23\'"]
        for created in created_resources:
            self.resource_dict[created] = 0

    def get_utility(self):
        return sum([value * RESOURCE_WEIGHTS[key] for (key, value) in self.resource_dict.items()])

    def print_self(self):
        resource_str = self.name + ": "
        for r, v in self.resource_dict.items():
            resource_str += r + ": " + str(v) + " "
        print(resource_str + "utility: " + str(self.get_utility()))


class World:
    def __init__(self, countries):
        self.countries = countries
        self.big_U = self.get_big_U()

    def __lt__(self, other):
        # This is unconventional here: we push worlds with the largest big_U value to the top of our priority queue
        return self.big_U > other.big_U

    def generate_successors(self):
        bins = [1, 5, 10, 25, 100]
        suc = []
        transform_templates = {(("r1", 1), ("r2", 2)): (("r1", 1), ("r21", 1), ("r21\'", 1)),
                               (("r1", 3), ("r2", 2), ("r21", 2)): (("r22", 2), ("r22\'", 2), ("r1", 3)),
                               (("r1", 5), ("r2", 1), ("r3", 5), ("r21", 3)): (("r1", 5), ("r23", 1), ("r23\'", 1))}

        deepcopy_world = deepcopy(self)

        for country_index in range(len(self.countries)):
            for size in bins:
                for (inputs, outputs) in transform_templates.items():
                    lacks_enough = False
                    for (resource, amt) in inputs:
                        if size * amt > self.countries[country_index].resource_dict[resource]:
                            lacks_enough = True
                    if lacks_enough:
                        continue
                    else:
                        successor_world = deepcopy_world
                        deepcopy_world = deepcopy(deepcopy_world)
                        for (resource, amt) in inputs:
                            successor_world.countries[country_index].resource_dict[resource] -= size * amt
                        for (resource, amt) in outputs:
                            successor_world.countries[country_index].resource_dict[resource] += size * amt
                        successor_world.big_U = successor_world.get_big_U()
                        operation = ("TRANSFORM", {r: size * a for (r, a) in inputs}, {r: size * a for (r, a) in outputs})
                        suc.append((successor_world, operation))

        for first_ind in range(len(self.countries)):
            for second_ind in range(len(self.countries)):
                if first_ind != second_ind:
                    for size in bins:
                        for resource_given in self.countries[first_ind].resource_dict.keys():
                            for resource_received in self.countries[second_ind].resource_dict.keys():
                                if resource_given != resource_received:
                                    if self.countries[first_ind].resource_dict[resource_given] > size:
                                        if self.countries[second_ind].resource_dict[resource_received] > size:
                                            successor_world = deepcopy_world
                                            deepcopy_world = deepcopy(deepcopy_world)
                                            successor_world.countries[first_ind].resource_dict[resource_given] -= size
                                            successor_world.countries[second_ind].resource_dict[resource_received] += size
                                            successor_world.countries[first_ind].resource_dict[resource_received] -= size
                                            successor_world.countries[second_ind].resource_dict[resource_given] += size
                                            successor_world.big_U = successor_world.get_big_U()
                                            operation = ("TRANSFER", self.countries[first_ind].name, resource_given, size,
                                                         self.countries[second_ind].name, resource_received, size)
                                            suc.append((successor_world, operation))

        heapq.heapify(suc)
        return suc

    def get_sd(self, vec):
        sd = 0
        average = sum(vec) / float(len(vec))
        for val in vec:
            sd += (val - average) ** 2
        return sd ** 0.5

    def get_big_U(self):
        country_utilities = [c.get_utility() for c in self.countries]
        # Big U measure: average(utilities) / sd(utilities)
        return (sum(country_utilities) / len(country_utilities)) / self.get_sd(country_utilities)

    def print_world(self):
        print("Current World State: ")
        for c in self.countries:
            c.print_self()
        print("Big U: " + str(self.big_U))
        print()
