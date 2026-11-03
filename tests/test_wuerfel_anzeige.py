"""Presentation capture must not change game results, RNG consumption or hidden checks."""
import concurrent.futures
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kern import wuerfel, wuerfel_anzeige


class AnzeigeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eden_dice_unit_")
        self.addCleanup(self.temp.cleanup)
        self.moddir = self.temp.name
        self.z = {"id": "test-run", "event": {"id": "test-event"}, "szene": None}

    def test_same_result_and_no_extra_rng_calls(self):
        with patch.object(wuerfel.random, "randint", side_effect=[1, 20]) as rand:
            with wuerfel_anzeige.sammeln("job", {}, self.z, self.moddir) as packet:
                result = wuerfel.probe("cunning", 15, [("Cunning", 2)], vorteil=True)
        self.assertEqual(rand.call_count, 2)
        self.assertEqual(result["wuerfe"], [1, 20])
        self.assertEqual(result["ergebnis"], "kritisch")
        self.assertEqual(packet["rolls"][0]["probe"], result)
        self.assertEqual(set(self.z), {"id", "event", "szene"})
        result["boni"].append(("later", 5))
        self.assertEqual(len(packet["rolls"][0]["probe"]["boni"]), 1)

    def test_hidden_and_unwatched_actions_are_not_exposed(self):
        with wuerfel_anzeige.sammeln("zug", {}, self.z, self.moddir) as packet:
            wuerfel.verdeckt(2, 12)
        self.assertEqual(packet["rolls"], [])
        with wuerfel_anzeige.sammeln("handy_antwort", {}, self.z, self.moddir) as packet:
            wuerfel.probe("charm", 12, [])
        self.assertEqual(packet["rolls"], [])
        self.assertIsNone(wuerfel_anzeige._AKTUELL.get())

    def test_policy_is_module_data(self):
        Path(self.moddir, "wuerfel_anzeige.json").write_text(json.dumps({"gross": {"ereignisse": ["test-event"]}, "kritisch_gross": False}), encoding="utf-8")
        with wuerfel_anzeige.sammeln("event_wahl", {}, self.z, self.moddir) as packet:
            wuerfel.probe("charm", 12, [])
        self.assertEqual(packet["rolls"][0]["modus"], "gross")
        self.assertFalse(packet["policy"]["kritisch_gross"])

    def test_cleanup_on_exception_and_nested_contexts(self):
        with self.assertRaises(ValueError):
            with wuerfel_anzeige.sammeln("job", {}, self.z, self.moddir):
                raise ValueError("test")
        self.assertIsNone(wuerfel_anzeige._AKTUELL.get())
        with wuerfel_anzeige.sammeln("job", {}, self.z, self.moddir) as outer:
            with wuerfel_anzeige.sammeln("job", {}, self.z, self.moddir) as inner:
                wuerfel.probe("cunning", 12, [])
            wuerfel.probe("charm", 12, [])
        self.assertEqual(len(outer["rolls"]), 1)
        self.assertEqual(len(inner["rolls"]), 1)
        self.assertNotEqual(outer["rolls"][0]["id"], inner["rolls"][0]["id"])

    def test_thread_isolation(self):
        def task(i):
            with wuerfel_anzeige.sammeln("job", {}, {"id": str(i)}, self.moddir) as packet:
                wuerfel.probe("cunning", 12, [])
                return packet
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            packets = list(executor.map(task, range(12)))
        self.assertEqual({p["run_id"] for p in packets}, {str(i) for i in range(12)})
        self.assertTrue(all(len(p["rolls"]) == 1 for p in packets))
        self.assertEqual(len({p["rolls"][0]["id"] for p in packets}), 12)

    def test_disabled_and_invalid_config(self):
        path = Path(self.moddir, "wuerfel_anzeige.json")
        path.write_text('{"aktiv":false}', encoding="utf-8")
        with wuerfel_anzeige.sammeln("job", {}, self.z, self.moddir) as packet:
            wuerfel.probe("cunning", 12, [])
        self.assertEqual(packet["rolls"], [])
        path.write_text("not json", encoding="utf-8")
        self.assertEqual(wuerfel_anzeige.einstellungen(self.moddir), {})


if __name__ == "__main__":
    unittest.main()
