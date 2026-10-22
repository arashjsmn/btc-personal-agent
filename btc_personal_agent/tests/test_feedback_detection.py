
import unittest

from agent import detect_user_feedback


class TestFeedbackDetection(unittest.TestCase):

    def test_detects_long_answer_feedback(self):
        self.assertTrue(
            detect_user_feedback(
                "Your previous answer was too long."
            )
        )

    def test_detects_complexity_feedback(self):
        self.assertTrue(
            detect_user_feedback(
                "The explanation was too complicated."
            )
        )

    def test_ignores_normal_market_question(self):
        self.assertFalse(
            detect_user_feedback(
                "Analyze Bitcoin for me."
            )
        )


if __name__ == "__main__":
    unittest.main()
