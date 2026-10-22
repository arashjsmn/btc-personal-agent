from memory.episodic import EpisodicMemory

memory = EpisodicMemory()

memory.add_episode(
    "user_feedback",
    "The previous Bitcoin analysis was too complicated."
)

memory.add_episode(
    "analysis_preference",
    "The user prefers simple explanations of RSI and moving averages."
)

for episode in memory.get_recent():
    print(episode)