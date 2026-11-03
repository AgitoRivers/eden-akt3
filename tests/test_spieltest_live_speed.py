"""Pure speed-up contracts; no engine import and no model/network access."""
import ast
import json
import tempfile
import unittest
from pathlib import Path

from spieltest_live_speed import check_key, read_check


class SpeedContracts(unittest.TestCase):
    def test_actor_dialogue_and_player_choices_are_never_memoized(self):
        self.assertIsNone(check_key("s", "u", (), {}, "engine"))
        self.assertIsNone(check_key("s", "u", (), {"grammar": "g"}, "spieler"))
        self.assertIsNone(check_key("s", "u", (), {"grammar": "g", "sampler": {"temperature": .7}}, "engine"))
        self.assertIsNone(check_key("s", "u", (), {"grammar": "g", "sampler": {}}, "engine"))

    def test_exact_context_rules_sampling_and_model_are_part_of_key(self):
        kwargs = {"grammar": "g", "sampler": {"temperature": 0}, "max_tokens": 20}
        key = check_key("rules", "facts", (), kwargs, "engine")
        self.assertEqual(key, check_key("rules", "facts", (), dict(kwargs), "engine"))
        for variant in (check_key("changed", "facts", (), kwargs, "engine"),
                        check_key("rules", "new facts", (), kwargs, "engine"),
                        check_key("rules", "facts", (), dict(kwargs, max_tokens=30), "engine"),
                        check_key("rules", "facts", (), kwargs, "engine", model="other")):
            self.assertNotEqual(key, variant)

    def test_corrupt_or_mismatched_cache_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "check.json"
            self.assertIsNone(read_check(path, "key"))
            path.write_text(json.dumps(dict(key="key", text='{"verdict": true}')), encoding="utf-8")
            self.assertEqual(read_check(path, "key"), '{"verdict": true}')
            self.assertIsNone(read_check(path, "other"))
            path.write_text(json.dumps(dict(key="key", text="not JSON")), encoding="utf-8")
            self.assertIsNone(read_check(path, "key"))

    def test_single_option_skips_model_but_multiple_options_still_use_it(self):
        source = ast.parse((Path(__file__).parent / "spieltest_live.py").read_text(encoding="utf-8"))
        klass = next(n for n in source.body if isinstance(n, ast.ClassDef) and n.name == "LiveLauf")
        method = next(n for n in klass.body if isinstance(n, ast.FunctionDef) and n.name == "player")
        class NoModel:
            @staticmethod
            def chat(*args, **kwargs):
                raise AssertionError("model reached")
            @staticmethod
            def wahl_grammatik(*args):
                return "grammar"
        contract = ast.ClassDef(name="Contract", bases=[], keywords=[], body=[method], decorator_list=[])
        ns = dict(llm=NoModel, stamp=lambda: "time", json=json)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[contract],type_ignores=[])), "choice", "exec"), ns)
        bot = ns["Contract"]()
        bot.profil = dict(vorlieben="test", gespraechsstrategie="test")
        bot.append = lambda *a: None
        self.assertEqual(bot.player({}, {7:"Continue"}), 7)
        self.assertEqual(bot.forced_choices, 1)
        with self.assertRaisesRegex(AssertionError, "model reached"):
            bot.player({}, {2:"Yes",7:"No"})


if __name__ == "__main__":
    unittest.main()
