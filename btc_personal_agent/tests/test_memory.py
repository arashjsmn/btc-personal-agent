
import tempfile
import unittest
from pathlib import Path

from memory.short_term import ShortTermMemory
from memory.long_term import LongTermMemory
from memory.episodic import EpisodicMemory


class TestMemory(unittest.TestCase):

    def test_short_term_memory(self):
        memory = ShortTermMemory()

        memory.add_message("user", "Analyze Bitcoin.")
        memory.add_message("assistant", "Here is the analysis.")

        self.assertEqual(len(memory.get_messages()), 2)
        self.assertEqual(
            memory.get_messages()[0]["role"],
            "user"
        )

        memory.clear()
        self.assertEqual(memory.get_messages(), [])

    def test_long_term_memory_persistence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "long_term.json"

            memory = LongTermMemory(str(path))
            memory.update("explanation_style", "simple English")

            reloaded = LongTermMemory(str(path))

            self.assertEqual(
                reloaded.get("explanation_style"),
                "simple English"
            )

    def test_episodic_memory_persistence(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "episodes.json"

            memory = EpisodicMemory(str(path))
            memory.add_episode(
                "user_feedback",
                "Use shorter explanations."
            )

            reloaded = EpisodicMemory(str(path))
            recent = reloaded.get_recent(limit=1)

            self.assertEqual(len(recent), 1)
            self.assertEqual(
                recent[0]["event"],
                "user_feedback"
            )
            self.assertEqual(
                recent[0]["details"],
                "Use shorter explanations."
            )


if __name__ == "__main__":
    unittest.main()
