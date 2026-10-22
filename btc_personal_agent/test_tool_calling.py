
from agent import analyze_bitcoin
from memory.long_term import LongTermMemory

memory = LongTermMemory()

print("Before:", memory.get("explanation_style", "not set"))

memory.update("explanation_style", "formal English")

answer = analyze_bitcoin(
    "Change my explanation style to beginner-friendly English. "
    "Please save this new preference."
)

print("\nAgent response:")
print(answer)

# Reload memory to verify that it was saved to disk
memory_after = LongTermMemory()

print(
    "\nSaved explanation style:",
    memory_after.get("explanation_style", "not set")
)
