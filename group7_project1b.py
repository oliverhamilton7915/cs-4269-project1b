from World import Country, World

def main():
    # First, we need to create a few countries.
    france_resources = {"r1": 100, "r2": 30, "r3": 110}
    france = Country("France", france_resources)
    germany_resources = {"r1": 140, "r2": 120, "r3": 65}
    germany = Country("Germany", germany_resources)
    america_resources = {"r1": 190, "r2": 130, "r3": 100}
    america = Country("America", america_resources)
    thailand_resources = {"r1": 35, "r2": 12, "r3": 45}
    thailand = Country("Thailand", thailand_resources)
    countries = [france, germany, america, thailand]

    # Now, we create our world
    world = World(countries)
    world.print()

if __name__ == "__main__":
    main()