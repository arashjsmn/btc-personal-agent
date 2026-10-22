
from memory.short_term import ShortTermMemory

memory = ShortTermMemory()

memory.add_message("user", "Analyze Bitcoin for me.")
memory.add_message("assistant", "The latest RSI is around 44.")

print(memory.get_messages())
