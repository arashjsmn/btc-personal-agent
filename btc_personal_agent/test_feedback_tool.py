
from agent import analyze_bitcoin
from memory.episodic import EpisodicMemory
from memory.long_term import LongTermMemory

memory = EpisodicMemory()
before = len(memory.episodes)

answer = analyze_bitcoin(
    "Your previous answer was too long. "
    "Please use three short bullet points in future responses."
)

print("\nAgent response:")
print(answer)

memory = EpisodicMemory()
new_episodes = memory.episodes[before:]

print("\nNew episodes:")
for episode in new_episodes:
    print(episode)

feedback_saved = any(
    episode.get("event") == "user_feedback"
    for episode in new_episodes
)

print("\nAutomatic feedback saving:", feedback_saved)

preferences = LongTermMemory()
print(
    "Saved explanation style:",
    preferences.get("explanation_style", "not set")
)
