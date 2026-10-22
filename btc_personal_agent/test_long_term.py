from memory.long_term import LongTermMemory

memory = LongTermMemory()

memory.update("risk_tolerance", "medium")
memory.update("investment_horizon", "long-term")
memory.update("knowledge_level", "beginner")

print("Risk tolerance:", memory.get("risk_tolerance"))
print("Investment horizon:", memory.get("investment_horizon"))
print("Knowledge level:", memory.get("knowledge_level"))