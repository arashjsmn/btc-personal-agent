from memory.long_term import LongTermMemory

memory = LongTermMemory()

print("Current knowledge level:",
      memory.get("knowledge_level", "not set"))

print("Current risk tolerance:",
      memory.get("risk_tolerance", "not set"))

print("Current investment horizon:",
      memory.get("investment_horizon", "not set"))

# Update a preference
memory.update("knowledge_level", "beginner")
memory.update("explanation_style", "simple English")

print("\nUpdated preferences:")
print("Knowledge level:", memory.get("knowledge_level"))
print("Explanation style:", memory.get("explanation_style"))