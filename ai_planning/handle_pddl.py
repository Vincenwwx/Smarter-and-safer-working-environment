import pathlib
import requests
import re


def update_problem(place, data):
    """
    Update the ###Problem.pddl file
    :param place:   "entrance" or "environment"
    :param data:    data (json)
    :return: None
    """
    if place == "office":
        file_name = str(pathlib.Path(__file__).parent.joinpath("comfortProblem.pddl"))
        with open(file_name, "r") as f:
            content = f.read()
            new_content = re.sub(r'temp r\) [0-9]+\.[0-9]+',
                                 r'temp r) '+str(data["temperature"]), content)
            new_content = re.sub(r'humidity r\) [0-9]+\.[0-9]+',
                                 r'humidity r) '+str(data["humidity"]), new_content)
            new_content = re.sub(r'lightintensity r\) [0-9]+',
                                 r'lightintensity r) '+str(data["lightness"]), new_content)
            f.close()
        with open(file_name, "w") as f:
            f.write(new_content)
            f.close()

    else:
        file_name = str(pathlib.Path(__file__).parent.joinpath("safetyProblem.pddl"))
        with open(file_name, "r") as f:
            content = f.read()
            new_content = re.sub(r'bodytemp p\) [0-9]+\.[0-9]+',
                                 r'bodytemp p) '+str(data["body_temperature"]), content)
            new_content = re.sub(r'motion p\) [0-9]',
                                 r'motion p) '+str(data["people_at_gate"]), new_content)
            new_content = re.sub(r'movement p\) [0-9]',
                                 r'movement p) '+str(data["people_enter"]), new_content)
            f.close()
        with open(file_name, "w") as f:
            f.write(new_content)
            f.close()


def get_plans(place):
    """
    Get AI planing result and write plans to a file
    :param place: str, can be "entrance" or "environment"
    :return: None
    """
    file_name = "safety" if place == "entrance" else "comfort"
    domain_file = pathlib.Path(__file__).parent.joinpath(file_name+"Domain.pddl")
    problem_file = pathlib.Path(__file__).parent.joinpath(file_name+"Problem.pddl")
    try:
        data = {"domain": open(domain_file,"r").read(),
                "problem": open(problem_file, "r").read()}
    except:
        print("Failed to read domain or problem file...")
        exit(0)

    response = requests.post("http://solver.planning.domains/solve", json=data).json()

    # Save the plan to file and
    # result_file = pathlib.Path(__file__).parent.joinpath(file_name+"_plans")
    # result_file.touch(exist_ok=True)
    # with open(result_file, 'w') as f:
    #     for act in response['result']['plan']:
    #         f.write(str(act['name']))
    #         f.write('\n')

    return response["result"]["plan"]


if __name__ == '__main__':
    res = get_plans("environment")
    for act in res:
        print(str(act["name"]))