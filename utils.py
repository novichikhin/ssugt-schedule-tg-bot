import json

from aiogram.types.base import Boolean

with open('groups.json', encoding='utf-8') as f:
    groups = json.load(f)

def find_group(group_name):
    return next((a for b in groups.values() for a in b if a['name'].lower() == group_name), None)

def get_groups_message():
    message = ''
    for key, value in groups.items():
        message += f"❗ {key}\n"
        for group in value:
            message += f"{group['name']}\n"
        message += '\n\n'

    return message