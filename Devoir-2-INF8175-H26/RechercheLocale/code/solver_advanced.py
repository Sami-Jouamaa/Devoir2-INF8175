import random as rand
import math
import time


def solution_initial(schedule):
#Gready approach
    solution = {}

    for course in schedule.course_list:

        used_courses = set()

        for n in schedule.get_node_conflicts(course):
            if n in solution:
                used_courses.add(solution[n])

        c = 1
        while c in used_courses:
            c += 1

        solution[course] = c

    return solution


def count_conflicts(solution, schedule):

    conflicts = 0

    for c1, c2 in schedule.conflict_list:
        if solution[c1] == solution[c2]:
            conflicts += 1

    return conflicts


def cost(solution, schedule):

    conflicts = count_conflicts(solution, schedule)

    if conflicts > 0:
        return conflicts * 1000

    return schedule.get_n_creneaux(solution)


def neighbor(solution, schedule, k):

    new_solution = solution.copy()

    course = rand.choice(list(schedule.course_list))

    new_solution[course] = rand.randint(1, k)

    return new_solution


def simulated_annealing(solution, schedule, k, time_limit):

    temparature = 100
    cooling = 0.995

    current = solution.copy()
    current_cost = cost(current, schedule)

    best_solution = current.copy()
    best_cost = current_cost

    start = time.time()

    while time.time() - start < time_limit:

        new = neighbor(current, schedule, k)
        new_cost = cost(new, schedule)

        delta = new_cost - current_cost
        selectiton_probability = math.exp(-delta / temparature)

        if delta < 0 or rand.random() < selectiton_probability:
            current = new
            current_cost = new_cost

        if current_cost < best_cost: #search local minimum
            best_solution = current.copy()
            best_cost = current_cost

        temparature *= cooling #decrease temperature to select a valid neighbor

        if temparature < 0.001:
            temparature = 100

    return best_solution


def solve(schedule):
    """
    Your solution of the problem
    :param schedule: object describing the input
    :return: a list of tuples of the form (c,t) where c is a course and t a time slot.
    """
    # Add here your agent

    start_time = time.time()

    solution = solution_initial(schedule)

    best_solution = solution.copy()
    best_k = schedule.get_n_creneaux(solution)

    while time.time() - start_time < 280: #Each instance in main is max 4 min 30

        k = best_k - 1

        if k <= 1:
            break

        candidate = simulated_annealing(best_solution, schedule, k, 20)

        if count_conflicts(candidate, schedule) == 0:
            best_solution = candidate
            best_k = k
        else:
            break

    return best_solution