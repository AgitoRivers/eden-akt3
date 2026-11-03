"""Regression checks for honest coverage, seed isolation and persona priorities."""
import copy
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import spieltest_peer as P
import spieltest_rezension as R
from spieltest_profile import PROFILE, option_bonus
from spieltest_verhalten import antwort_werten, geste_waehlen, date_signale
from spieltest_reviewstruktur import ABSCHNITTE, sprechtext


def lauf(typ="naomi", seed=1):
    return dict(typ=typ, seed=seed, ende={"status": "ende", "tag": 15}, aktionen={},
                abstuerze=[], sackgassen=[], tage=[], events={}, szenen={}, kaempfe=[],
                peer={"signale": {}, "wahl_folgen": {}, "belege": []})


def roh(*runs):
    return dict(laeufe=list(runs), zeit="30.10.2026", commit="test", dirty=False)


class PeerTests(unittest.TestCase):
    def test_naomi_does_not_reject_invitation_for_hidden_points(self):
        context = "Loser does what the winner says. I'm already winning."
        warm = dict(text="Tells her the mark on the board is for both of them.", folgen=[{"geld": -100}])
        cold = dict(text="Go and cool off. Goodnight.", folgen=[{"begehren": ["npc", 999]}])
        self.assertGreater(antwort_werten(PROFILE["naomi"], warm, context)[0],
                           antwort_werten(PROFILE["naomi"], cold, context)[0])
        changed = copy.deepcopy(warm)
        changed["folgen"] = [{"begehren": ["npc", 99999]}]
        self.assertEqual(antwort_werten(PROFILE["naomi"], warm, context),
                         antwort_werten(PROFILE["naomi"], changed, context))

    def test_invitation_beats_first_compliment_and_avoids_duplicate_date(self):
        gestures = [dict(id=gid, je={"npc": {"gesperrt": "", "abgenutzt": False}})
                    for gid in ("kompliment", "einladen")]
        self.assertEqual(geste_waehlen(PROFILE["naomi"], gestures, random.Random(1))["id"], "einladen")
        self.assertEqual(geste_waehlen(PROFILE["naomi"], gestures, random.Random(1), verabredet={"npc"})["id"], "kompliment")
        gestures[1]["je"]["npc"]["gesperrt"] = "Not available"
        self.assertEqual(geste_waehlen(PROFILE["naomi"], gestures, random.Random(1))["id"], "kompliment")

    def test_invitation_schedule_and_scene_are_distinct(self):
        before = dict(status="szene", tag=2, phase="tag", szene={"def": {"id": "normal"}})
        attempted = date_signale(before, before, "geste", dict(id="einladen"))
        self.assertEqual(attempted, {"einladungen_angenommen_engine": 1})
        scheduled = dict(before, verabredungen=[dict(pid="npc", tag=2, phase="abend")])
        self.assertEqual(date_signale(before, scheduled, "geste", dict(id="einladen"))["dates_vereinbart"], 1)
        scene = dict(scheduled, phase="abend", szene={"def": {"id": "date_npc"}})
        self.assertEqual(date_signale(scheduled, scene, "phase_beenden", {})["dates_begonnen"], 1)
        self.assertNotIn("dates_begonnen", date_signale(scene, scene, "zug", {}))

    def test_old_zero_dates_does_not_claim_no_invitation(self):
        m = P.messwerte(lauf())
        self.assertIsNone(m["einladungen_versucht"])
        self.assertIn("ungeklärt", P.date_diagnose(m))

    def test_assisted_completion_is_not_independent_or_green(self):
        r = lauf("noor")
        r["hilfe"] = [{"tag": 8, "kampf": "fixture", "eingriff": "Parade erhöht"}]
        m = P.messwerte(r)
        self.assertFalse(m["selbststaendig"])
        self.assertEqual(P.kriterium("stabilitaet", r, m)["status"], "gelb")
        review = next(x for x in P.auswerten(roh(r))["reviews"] if x["id"] == "noor")
        self.assertEqual(review["status"], "mit_hilfe")
        self.assertEqual(review["laufdaten"][0]["hilfe"][0]["tag"], 8)

    def test_escape_is_not_counted_as_victory(self):
        r = lauf()
        r["kaempfe"] = [dict(id="fixture", art="entkommen", zuege=2)]
        self.assertEqual(P.messwerte(r)["siege"], 0)
        self.assertEqual(P.messwerte(r)["entkommen"], 1)

    def test_new_structure_does_not_relabel_historic_runs_as_retested(self):
        r = lauf()
        r["profil_version"] = 1
        n = next(x for x in P.auswerten(roh(r))["reviews"] if x["id"] == "naomi")
        self.assertTrue(n["laufstand"]["historisch"])
        self.assertEqual(n["laufstand"]["profil_versionen"], ["1"])

    def test_missing_persona_never_borrows_another_run(self):
        reviews = P.auswerten(roh(lauf()))["reviews"]
        self.assertEqual(len(reviews), 9)
        alex = next(r for r in reviews if r["id"] == "alex")
        self.assertEqual(alex["status"], "nicht_getestet")
        self.assertTrue(all(k["status"] == "offen" and not k["belege"] for k in alex["kriterien"]))

    def test_worst_seed_not_hidden_by_success(self):
        good, bad = lauf("alex"), lauf("alex", 2)
        bad["sackgassen"] = [{"tag": 3, "text": "fixture"}]
        bad["ende"]["status"] = "wahl"
        d = P.auswerten(roh(good, bad))
        alex = d["reviews"][0]
        self.assertEqual(alex["status"], "blockiert")
        self.assertEqual(next(k for k in alex["kriterien"] if k["id"] == "stabilitaet")["status"], "rot")
        self.assertEqual(d["blocker"][0]["lauf"], "alex/2")

    def test_missing_telemetry_is_not_zero_or_green(self):
        r = lauf()
        del r["peer"]
        m = P.messwerte(r)
        self.assertIsNone(m["vertrauen_aenderungen"])
        self.assertEqual(P.kriterium("romance", r, m)["status"], "offen")
        self.assertEqual(P.kriterium("intimitaet", r, m)["status"], "offen")

    def test_intimacy_actions_do_not_claim_chemistry_or_consent(self):
        r = lauf()
        r["aktionen"]["intim"] = 2
        d = P.auswerten(roh(r))
        naomi = next(x for x in d["reviews"] if x["id"] == "naomi")
        k = next(x for x in naomi["kriterien"] if x["id"] == "intimitaet")
        self.assertEqual(k["status"], "gruen")
        self.assertIn("keine Inhaltswertung", k["belege"][0]["art"])
        self.assertIn("Einvernehmen", k["menschlich"])

    def test_same_source_can_matter_differently_without_changing_facts(self):
        d = P.auswerten(roh(lauf("naomi"), lauf("tandi")))
        n = next(x for x in d["reviews"] if x["id"] == "naomi")
        t = next(x for x in d["reviews"] if x["id"] == "tandi")
        self.assertIn("intimitaet", [k["id"] for k in n["kriterien"]])
        self.assertIn("builds", [k["id"] for k in t["kriterien"]])
        self.assertNotEqual(n["review"], t["review"])

    def test_demographics_do_not_drive_choice_scores(self):
        p = copy.deepcopy(PROFILE["naomi"])
        f = [{"vertrauen": ["npc", 2]}, {"begehren": ["npc", 1]}]
        before = option_bonus(p, f)
        p["hintergrund"] = "Andere Herkunft und anderes Geschlecht"
        self.assertEqual(before, option_bonus(p, f))
        self.assertNotEqual(before, option_bonus(PROFILE["tandi"], f))

    def test_html_escapes_external_error_text(self):
        r = lauf()
        r["abstuerze"] = [{"text": "<script>alert(1)</script>"}]
        page = P.seite(P.auswerten(roh(r)))
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_every_profile_has_questions_and_legal_policy(self):
        for p in PROFILE.values():
            self.assertTrue(p["fragen"])
            self.assertEqual(len(set(p["attribute"])), 6)
            self.assertTrue(0 <= p["parade"][0] <= p["parade"][1] <= 1)
            self.assertTrue(set(p["gewichte"]) <= set(P.KRITERIEN))

    def test_content_packet_excludes_unreached_events(self):
        r = lauf()
        r["events"] = {"gesehen": 2}
        events = [dict(id="gesehen", lage="sichtbare Quelle", zeilen=[], optionen=[]),
                  dict(id="geheim", lage="UNGESPIELTES_GEHEIMNIS", zeilen=[], optionen=[])]
        packet = R.pakete(roh(r), events)
        import json
        text = json.dumps(packet)
        self.assertIn("sichtbare Quelle", text)
        self.assertNotIn("UNGESPIELTES_GEHEIMNIS", text)
        self.assertEqual(len(packet["pakete"]), 1)

    def test_content_review_requires_known_evidence_and_exact_criteria(self):
        p = dict(kriterien=[dict(id="romance")], quellen=[dict(id="event:test")])
        result = dict(kurzfazit="Vorläufig", kriterien=[dict(id="romance", status="interpretation",
                      urteil="Textinterpretation", belege=["event:test"], naechster_test="Dialog spielen")])
        self.assertEqual(R.validieren(result, p), result)
        for refs in ([], ["event:erfunden"]):
            bad = copy.deepcopy(result)
            bad["kriterien"][0]["belege"] = refs
            with self.assertRaises(ValueError):
                R.validieren(bad, p)
        bad = copy.deepcopy(result)
        bad["kriterien"][0]["id"] = "erfunden"
        with self.assertRaises(ValueError):
            R.validieren(bad, p)

    def test_personal_review_structure_and_separate_narration(self):
        p = dict(review_schema_version=2, kriterien=[dict(id="romance")], quellen=[dict(id="event:test")])
        result = dict(kurzfazit="Vorläufig", kriterien=[dict(id="romance", status="interpretation",
                      urteil="Textinterpretation", belege=["event:test"], naechster_test="Dialog spielen")],
                      rezension={key: dict(text="Persönlicher Absatz über " + key, status="interpretation", belege=["event:test"])
                                 for key in ABSCHNITTE}, befunde=[dict(kriterium="romance", art="geschmack",
                      beobachtung="Eine Einladung ist belegt.", interpretation="Sie reizt mich.",
                      auswirkung="Ich möchte die Figur näher kennenlernen.", prioritaet="P2", belege=["event:test"],
                      naechster_test="Einladung annehmen und die nächste Begegnung vergleichen.")])
        R.validieren(result, p)
        text = sprechtext([dict(name="Naomi Malice", review=result)])
        self.assertIn("Naomi Malice", text)
        self.assertNotIn("event:test", text)
        self.assertIn("Persönlicher Absatz", text)
        bad = copy.deepcopy(result)
        del bad["rezension"]["fazit"]
        with self.assertRaises(ValueError):
            R.validieren(bad, p)
        bad = copy.deepcopy(result)
        bad["befunde"][0]["prioritaet"] = "P1"
        with self.assertRaises(ValueError):
            R.validieren(bad, p)
        bad = copy.deepcopy(result)
        bad["rezension"]["kritik"]["belege"] = ["unbelegt"]
        with self.assertRaises(ValueError):
            R.validieren(bad, p)

    def test_memory_review_cannot_claim_generated_dialogue_from_static_text(self):
        p = dict(kriterien=[dict(id="gedaechtnis")], quellen=[dict(id="event:test", art="Eventdefinition")])
        result = dict(kurzfazit="Vorläufig", kriterien=[dict(id="gedaechtnis", status="interpretation",
                      urteil="Behauptetes Gedächtnis", belege=["event:test"], naechster_test="Später nachfragen")])
        with self.assertRaises(ValueError):
            R.validieren(result, p)
        result["kriterien"][0]["status"] = "offen"
        R.validieren(result, p)


if __name__ == "__main__":
    unittest.main()
