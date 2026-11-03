"""Test selected live boundaries without importing the engine or calling any service."""
import ast
import types
import unittest
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE = ast.parse((Path(__file__).parent / "spieltest_live.py").read_text(encoding="utf-8"))


class LiveContracts(unittest.TestCase):
    def test_network_guard_only_allows_local_model(self):
        node = next(x for x in SOURCE.body if isinstance(x, ast.FunctionDef) and x.name == "local_open")
        namespace = dict(urllib=urllib, REAL_OPEN=lambda req,*a,**k: "allowed")
        exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])), "guard", "exec"), namespace)
        guard = namespace["local_open"]
        self.assertEqual(guard("http://127.0.0.1:5010/v1/chat/completions"), "allowed")
        for url in ("https://example.com", "http://127.0.0.1:8004", "http://127.0.0.1.evil.test:5010"):
            with self.assertRaises(RuntimeError):
                guard(url)

    def test_gesture_log_entries_do_not_replace_free_player_speech(self):
        klass = next(x for x in SOURCE.body if isinstance(x, ast.ClassDef) and x.name == "LiveLauf")
        method = next(x for x in klass.body if isinstance(x, ast.FunctionDef) and x.name == "szene")
        class Base:
            def szene(self, z):
                self.base_calls += 1
        contract = ast.ClassDef(name="Contract", bases=[ast.Name(id="Base", ctx=ast.Load())], keywords=[], body=[method], decorator_list=[])
        namespace = dict(Base=Base)
        exec(compile(ast.fix_missing_locations(ast.Module(body=[contract], type_ignores=[])), "scene_contract", "exec"), namespace)
        bot = namespace["Contract"]()
        bot.sprach_szenen, bot.base_calls, calls = set(), 0, []
        bot.tu = lambda *args: calls.append(args)
        z = dict(tag=1, phase="abend", szene={"def": {"id": "party"}, "log": [{"art":"duc"}]*3})
        bot.szene(z)
        self.assertEqual(calls, [("zug", {})])
        self.assertEqual(bot.base_calls, 0)
        bot.szene(z)
        self.assertEqual(bot.base_calls, 1)

    def test_reviews_get_the_siege_as_own_source(self):
        """02.11.2026: Live-Rezensionen sahen die Belagerung nur als einen Kalenderpunkt (bl_welle_6)."""
        batch = ast.parse((Path(__file__).parent / "spieltest_live_batch.py").read_text(encoding="utf-8"))
        node = next(x for x in batch.body if isinstance(x, ast.FunctionDef) and x.name == "belagerung_quellen")
        namespace = {}
        exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])), "siege", "exec"), namespace)
        ev = lambda i, n=1: {"id": i, "titel": i.upper(), "lage": "x" * 500, "zeilen": [{"wer": "a", "text": "y" * 500}] * 3,
                              "optionen": [{"text": "opt %d" % k} for k in range(n)]}
        index = {e["id"]: e for e in (ev("bl_rede"), ev("bl_welle_6", 2), ev("bl_cliff_alon"), ev("t0_start"))}
        run = {"typ": "mia", "seed": 1, "events": {"t0_start": 1, "bl_rede": 21, "bl_welle_6": 23, "bl_cliff_alon": 23},
               "event_wahl": {"bl_welle_6:1": 1}, "taktik": {"wellen": {"6": 1}, "wahlen": ["bl_minicu_duc_zuerst"]},
               "ende": {"tag": 24}}
        roh = {"laeufe": [run, dict(run, typ="lenny", events={"t0_start": 1}, taktik=None)]}
        q = namespace["belagerung_quellen"](roh, "mia", index)
        self.assertEqual([x["id"] for x in q], ["belagerung:mia/1"])
        self.assertEqual(q[0]["taktik"]["wahlen"], ["bl_minicu_duc_zuerst"])
        self.assertEqual([s["id"] for s in q[0]["szenen"]], ["bl_rede", "bl_welle_6", "bl_cliff_alon"])
        s = {x["id"]: x for x in q[0]["szenen"]}
        self.assertEqual(s["bl_welle_6"]["wahl"], "opt 1")
        self.assertTrue(s["bl_cliff_alon"]["dialog"] and "dialog" not in s["bl_rede"] and "lage" not in s["bl_rede"])
        self.assertLess(len(str(q)), 2000)
        self.assertEqual(namespace["belagerung_quellen"](roh, "lenny", index), [])


if __name__ == "__main__":
    unittest.main()
