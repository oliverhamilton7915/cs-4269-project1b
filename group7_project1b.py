from World import Country, World


def game_scheduler(country_name,
                   resources_filename,
                   operator_def_filename,
                   initial_state_filename,
                   output_schedule_filename,
                   num_output_schedules,
                   depth_bound,
                   frontier_max_size):

    with open(resources_filename, 'r') as resources:
        data = resources.readlines()[1:]
        data = [row.rstrip().split(' ') for row in data]
        resource_data = {r: {'weight': float(w), 'factor': float(f)} for (r, w, f) in data}

    countries = []
    with open(initial_state_filename, 'r') as initial:
        data = initial.readlines()
        data = [row.rstrip().split(' ') for row in data]
        initial_resources = data[0][1:]
        for row in data[1:]:
            country = Country(row[0],
                              {resource: int(amt) for (resource, amt) in zip(initial_resources, row[1:])},
                              resource_data)
            countries.append(country)
    world = World(countries)
    world.print_world()


def main():
    # First, we need to create a few countries.
    '''
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
    world.print_world()

    # Now, we want to generate our world's successors
    successors = world.generate_successors()
    print("--- WORLD\'S SUCCESSORS: ---")
    for (suc, op) in successors:
        print(op)
        suc.print_world()
    '''
    game_scheduler('self', # country_name
                   'resources_1.txt', # resources_filename
                   'operator_def_1.txt', # operator_def_filename
                   'initial_state_1.txt', # inital_state_filename
                   'output_schedules_1.txt', # output_schedule_filename
                   3, # num_output_schedules
                   5, # depth_bound
                   200) # frontier_max_size

if __name__ == "__main__":
    main()