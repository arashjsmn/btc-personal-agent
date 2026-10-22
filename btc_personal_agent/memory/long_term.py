import json
from pathlib import Path


class LongTermMemory:
    def __init__(self, file_path="data/long_term_memory.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.profile = json.load(file)
        else:
            self.profile = {}

    def update(self, key, value):
        self.profile[key] = value
        self.save()

    def get(self, key, default=None):
        return self.profile.get(key, default)

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.profile, file, ensure_ascii=False, indent=4)