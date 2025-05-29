# utils\profile_loader.py

import json
import os

def load_user_profile(path="users/user_profile.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}