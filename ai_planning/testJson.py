from handle_pddl import update_problem, get_plans
import json

data = json.dumps({
    "body_temperature": 39.0,
    "people_detected": 1,
})

data_re = json.loads(data)

update_problem("entrance", data_re)
plans = get_plans("entrance")
for act in plans:
    print(str(act["name"]))