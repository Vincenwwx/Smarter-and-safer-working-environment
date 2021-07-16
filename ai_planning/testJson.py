from handle_pddl import update_problem, get_plans
import json

data = json.dumps({
    "body_temperature": 19.0,
    "people_detected": 1,
})

data_re = json.loads(data)

# update_problem("entrance", data_re)
plans = get_plans("entrance")
a1, a2 = plans
print(a1["name"])
for act in plans:
    print(str(act["name"]))