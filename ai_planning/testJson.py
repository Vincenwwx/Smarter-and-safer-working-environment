from handle_pddl import update_problem, get_plans
import json

data = json.dumps({
    "temperature": 19.0,
    "humidity": 30.1,
    "lightness": 1
})

data_re = json.loads(data)

update_problem("office", data_re)
plans = get_plans("entrance")
#print(a1["name"])
for act in plans:
    print(str(act["name"]))