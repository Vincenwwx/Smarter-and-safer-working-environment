import pathlib


def updata_problem(place, key, value):
    file_name = "safetyProblem.pddl" \
        if place == "entrance" else "comfortProblem.pddl"
    problem_file = pathlib.Path(__file__).parent.joinpath(file_name)
    with open(problem_file, 'w') as f:

