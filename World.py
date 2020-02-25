import heapq, math

# population is 0, regular resources are 1, created resources are 2, and waste is -1
RESOURCE_WEIGHTS = {
    "r1": 0,
    "r2": 1.0,
    "r3": 1.0,
    "r21": 2.0,
    "r22": 2.0,
    "r23": -1.0
}


class Country:
    def __init__(self, name, resources_dict):
        self.name = name
        self.resource_dict = resources_dict
        created_resources = ["r21", "r22", "r23"]
        for created in created_resources:
            self.resource_dict[created] = 0

    def get_utility(self):
        return sum([value * RESOURCE_WEIGHTS[key] for (key, value) in self.resource_dict.items()])

    def print(self):
        resource_str = self.name + ": "
        for r, v in self.resource_dict.items():
            resource_str += r + ": " + str(v) + " "
        print(resource_str + "utility: " + str(self.get_utility()))


class World:
    def __init__(self, countries):
        self.countries = countries
        self.big_U = self.big_U()
        self.pq = []

    def generate_successors(self):
        heapq.heapify(self.pq)

    def get_entropy(self, vec):
        ent = 0
        max_val = max(vec)
        for val in vec:
            ent -= (val / max_val) * math.log(val / max_val, 2)
        return ent

    def big_U(self):
        country_utilities = [c.get_utility() for c in self.countries]
        # Big U measure: average(utilities) / entropy(utilities)
        return (sum(country_utilities) / len(country_utilities)) * self.get_entropy(country_utilities)

    def print(self):
        print("Current World State: ")
        for c in self.countries:
            c.print()
        print("Big U: " + str(self.big_U))
        print()
