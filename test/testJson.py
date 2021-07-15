from handle_pddl import update_problem
import json

data = json.dumps({
    "temperature": 12.22,
    "humidity": 88.1,
    "lightness": 2
})

data_re = json.loads(data)

update_problem("environment", data_re)