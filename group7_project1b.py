from World import Country, World
import heapq


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

    with open(operator_def_filename, 'r') as operator_temps:
        data = operator_temps.readlines()
        templates = tuple([row.rstrip() for row in data])

    frontier = [world]
    for iteration in range(depth_bound):
        frontier = deepen_frontier(frontier, country_name, templates, frontier_max_size)
        print("After iteration {}, created optimized frontier of length {}".format(iteration + 1, len(frontier)))

    # Here is where we print schedules!
    with open(output_schedule_filename, 'w') as output:
        for i in range(min(num_output_schedules, frontier_max_size)):
            # We cannot print more schedules than we have in our frontier!
            current_world = heapq.heappop(frontier)
            output.write('[ ')
            for step in range(len(current_world.history)):
                output.write('{} EU: {}\n'.format(*current_world.history[step]))
            output.write(']\n')


def deepen_frontier(frontier, country_name, templates, frontier_max_size):
    temp_frontier = []
    for cur_world in frontier:
        heapq.heappush(temp_frontier, cur_world)
        # loop over all get_successors
        successors = cur_world.generate_successors(country_name, templates)
        for successor in successors:
            heapq.heappush(temp_frontier, successor)
    # Here, we clip the length of the frontier
    frontier = []
    for i in range(min(frontier_max_size, len(temp_frontier))):
        frontier.append(heapq.heappop(temp_frontier))
    heapq.heapify(frontier)
    return frontier


def main():
    game_scheduler('self',  # country_name
                   'resources_1.txt',  # resources_filename
                   'operator_def_1.txt',  # operator_def_filename
                   'initial_state_1.txt',  # initial_state_filename
                   'output_schedules_1.txt',  # output_schedule_filename
                   20,  # num_output_schedules
                   3,  # depth_bound
                   100)  # frontier_max_size


if __name__ == "__main__":
    main()