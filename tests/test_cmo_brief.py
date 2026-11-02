import json
import unittest

from cmo_brief import CONTROLS, brief, jargon

with open("examples/q4_setup.json", encoding="utf-8") as fh:
    SETUP = json.load(fh)


class BriefTest(unittest.TestCase):
    def test_brief_is_jargon_free(self):
        self.assertEqual(jargon(brief(SETUP)), [])

    def test_every_control_text_is_jargon_free(self):
        for c, (risk, outcome) in CONTROLS.items():
            self.assertEqual(jargon(risk + " " + outcome), [], c)

    def test_open_risks_listed(self):
        text = brief(SETUP)
        self.assertIn("6 of 8 safeguards", text)
        self.assertIn("What could still happen", text)

    def test_jargon_caught(self):
        self.assertEqual(jargon("we added an MCP server and a YAML policy"), ["mcp", "yaml"])


if __name__ == "__main__":
    unittest.main()
