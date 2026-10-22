
from agent import analyze_bitcoin
from memory.episodic import EpisodicMemory

episodic_memory = EpisodicMemory()

# Simulate feedback from a previous conversation
episodic_memory.add_episode(
    "user_feedback",
    "The previous analysis was too complicated. "
    "Use simpler words and shorter explanations."
)

print("Saved feedback:")
print(episodic_memory.get_recent(limit=1))

print("\nRunning the agent...\n")

answer = analyze_bitcoin(
    "Analyze Bitcoin for me. Keep the explanation clear."
)

print("Agent response:")
print(answer)
