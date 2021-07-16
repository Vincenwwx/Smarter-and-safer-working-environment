import re

content = None

with open("test.txt", "r") as f:
    content = f.read()
    new_content = re.sub(r'test', r'hello', content)
    f.close()

with open("test.txt", "w") as f:
    f.write(new_content)
    f.close()