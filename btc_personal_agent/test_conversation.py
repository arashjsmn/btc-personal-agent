from agent import analyze_bitcoin, short_memory

# First message
answer1 = analyze_bitcoin(
    "My name is Alex. Please explain Bitcoin analysis in very simple English."
)

print("\n--- First answer ---")
print(answer1)

# Second message: test whether the agent remembers the first message
answer2 = analyze_bitcoin(
    "What is my name, and how did I ask you to explain things?"
)

print("\n--- Memory test ---")
print(answer2)

# Show how many messages are stored
print("\nMessages stored:", len(short_memory.get_messages()))