import unittest

from triage_helpers import extract_message_parts, find_nearby_clinics


class TriageHelpersTests(unittest.TestCase):
    def test_extracts_text_and_uploaded_file_paths(self):
        message = {
            "text": "  I have chest pain  ",
            "files": [{"path": "/tmp/symptoms.wav"}],
        }

        self.assertEqual(
            extract_message_parts(message),
            ["I have chest pain", "/tmp/symptoms.wav"],
        )

    def test_empty_message_has_no_parts(self):
        self.assertEqual(extract_message_parts({"text": " ", "files": []}), [])

    def test_city_lookup_is_case_insensitive(self):
        result = find_nearby_clinics("  PESHAWAR  ")

        self.assertIn("Lady Reading Hospital", result)

    def test_unknown_city_has_safe_fallback(self):
        result = find_nearby_clinics("Mardan")

        self.assertIn("nearest district hospital", result)


if __name__ == "__main__":
    unittest.main()
