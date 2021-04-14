import json


def load_tools():
    with open("db/mock_tools.json") as f:
        return json.load(f)


tools_db = load_tools()


def load_user_stories():
    with open("db/user_stories_db.json") as f:
        return json.load(f)


user_stories = load_user_stories()

def load_work_roles():
    with open("db/mock_work_roles.json") as f:
        return json.load(f)


work_roles = load_work_roles()