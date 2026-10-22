import json
from pathlib import Path
from datetime import datetime, timezone


class EpisodicMemory:
    def __init__(self, file_path="data/episodic_memory.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.episodes = json.load(file)
        else:
            self.episodes = []

    def add_episode(self, event, details):
        episode = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "details": details
        }

        self.episodes.append(episode)
        self.save()

    def get_recent(self, limit=5):
        return self.episodes[-limit:]

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.episodes, file, ensure_ascii=False, indent=4)