# -*- coding: utf-8 -*-
r"""Expeditionen messen (Duc 28.10.2026): Spieldauer, Kaempfe, Zuege und Niederlagen je Ortskapitel mit echten Kaempfen.

    python tests\expedition_sim.py                 alle Spielertypen
    python tests\expedition_sim.py klug            nur einer (einfach | klug | geuebt)

Spielertypen:
  einfach   greift nur an, Parade 35 % perfekt / 40 % gut / 25 % verfehlt (der alte Bot)
  klug      verteilt Attributpunkte und lernt Faehigkeiten beim Level-up, redet bei Rede-Gegnern, sucht die
            Schwachstelle, nutzt Spezialangriffe, Medkits unter 35 % LP und Granaten gegen Bosse; startet mit
            2 Verbandskaesten und 2 Granaten (KIT); Parade wie einfach
  geuebt    wie klug, Parade 55 % perfekt / 35 % gut / 10 % verfehlt
Duc steht auf dem Level des Kapitels (der Test springt per Abkuerzung zu frueh hinein). Nach einer Niederlage wird
weitergemessen, als haette der zweite Versuch geklappt - so zaehlt die volle Laenge, die Niederlagen stehen daneben.
Zeitmodell: Erzaehltext 200 Woerter/min, Sprechzeilen mit echter Audiodauer (sonst 150 Woerter/min), je Entscheidung
6 s + Optionstext; Kampf je Zug 8 s, je Parade 4 s, plus 15 s Auftakt und Abschluss."""
import copy, json, os, random, struct, sys

HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
import test_grotte as G  # noqa: E402

L, E, K, B = G.L, G.E, G.K, G.B
MOD = os.path.join(os.path.dirname(HIER), "module", "eden_rise")
PARADE = {"einfach": (.35, .75), "klug": (.35, .75), "geuebt": (.55, .90)}
KIT = ["verbandskasten", "verbandskasten", "grenade_water", "grenade_fire"]   # was ein Spieler vorher kauft (~140 EUR)
ATTR_REIHE = ("strength", "courage", "perception", "charm", "cunning", "empathy")
PFAD_REIHE = ("K", "M", "W", "L", "H")


def _wav(datei):
    p = os.path.join(MOD, "audio", datei)
    try:
        with open(p, "rb") as fh:
            rate = struct.unpack("<I", fh.read(44)[28:32])[0]
        return (os.path.getsize(p) - 44) / float(rate)
    except (OSError, struct.error, ZeroDivisionError):
        return None


def _woerter(t):
    return len((t or "").split())


class Messung:
    def __init__(self, typ, rng):
        self.typ, self.rng = typ, rng
        self.idx = json.load(open(os.path.join(MOD, "audio_index.json"), encoding="utf-8"))
        self.evs = {e["id"]: e for e in json.load(open(os.path.join(MOD, "ereignisse.json"), encoding="utf-8"))["events"]}

    def frame_zeit(self, ev):
        s = _woerter(ev.get("lage")) / 200 * 60
        for n, z in enumerate(ev.get("zeilen") or []):
            a = self.idx.get("%s#z%d" % (ev["id"], n))
            d = _wav(a["datei"]) if a else None
            s += d if d else _woerter(z.get("text")) / 150 * 60
        return s + 6 + sum(_woerter(o.get("text")) for o in ev.get("optionen") or []) / 200 * 60

    # ------------------------------------------------------------ Aufbau des Spielers
    def aufbauen(self):
        """klug/geuebt: freie Attributpunkte und Faehigkeitspunkte ausgeben (wie ein Spieler beim Level-up)."""
        if self.typ == "einfach":
            return
        z = E.aktiv()
        defs = E.kampf.daten(E.moddir("eden_rise"))
        c = E.kampf.progress(z)
        i = 0
        while c["attributpunkte"] > 0 and i < 60:
            try:
                E.kampf.attribut_steigern(z, ATTR_REIHE[i % len(ATTR_REIHE)])
            except ValueError:
                pass
            i += 1
        sp = sorted(defs["specials"].items(), key=lambda kv: (kv[1]["tier"], PFAD_REIHE.index(kv[1]["path"])))
        for _ in range(10):
            neu = next((sid for sid, s in sp if sid not in c["skills"] and not E.kampf.learn_reason(z, defs, sid)), None)
            if not neu:
                break
            E.kampf.lernen(z, defs, neu)
        E.sichern(z)

    def stufe(self, n):
        z = E.aktiv()
        c = E.kampf.progress(z)
        while c["level"] < n:
            E.kampf.award_xp(z, E.kampf.xp_needed(c["level"]) - c["xp"] + 1)
        if self.typ != "einfach":
            z["inventar"] = [i for i in z["inventar"] if i not in KIT] + list(KIT)
        E.sichern(z)
        self.aufbauen()

    # ------------------------------------------------------------ Kampf
    def zug(self, z, k, modul):
        sp, g = k["spieler"], k["gegner"][0]
        skills = {s["id"]: s for s in E.kampf.skills_view(z, k)}
        frei = lambda sid: sid in skills and not skills[sid]["gesperrt"]        # noqa: E731
        if g["def"].get("untouchable"):
            return ("faehigkeit", "reden") if frei("reden") else ("verteidigen", None)
        if self.typ == "einfach":
            return "angriff", None
        items = [x for x in E.kampf.gegenstaende(z, modul) if not x["gesperrt"]]
        if sp["lp"] < .35 * sp["lp_max"]:
            heil = [x for x in items if x.get("heilen")]
            if heil:
                return "gegenstand", max(heil, key=lambda x: x["heilen"])["id"]
        if g["def"].get("boss") and k["runde"] <= 2:
            gr = [x for x in items if (modul["items"][x["id"]].get("kampf") or {}).get("granate")]
            if gr:
                return "gegenstand", gr[0]["id"]
        if g["def"].get("weakness") == "charm" and frei("reden"):
            return "faehigkeit", "reden"
        if not g["schwaeche_bekannt"] and k["runde"] <= 1 and frei("schwachstelle"):
            return "faehigkeit", "schwachstelle"
        spez = [s for s in skills.values() if s["art"] == "spezial" and not s["gesperrt"] and not s.get("hinweis")]
        if spez:
            return "faehigkeit", max(spez, key=lambda s: s["stufe"])["id"]
        if g["def"].get("weakness") == "courage" and frei("einschuechtern"):
            return "faehigkeit", "einschuechtern"
        return "angriff", None

    def kampf(self, modul):
        zuege = paraden = 0
        p_perfekt, p_gut = PARADE[self.typ]
        for _ in range(400):
            z = E.aktiv()
            k = z["kampf"]
            if k["phase"] == "ende":
                erg = (k.get("ergebnis") or {}).get("art")
                E.aktion("kampf_schliessen", {})
                return erg, zuege, paraden
            if k["phase"] == "parade":
                paraden += 1
                r = self.rng.random()
                wahl = "perfekt" if r < p_perfekt else "gut" if r < p_gut else "verfehlt"
                p = k["parade"] or {}
                if p.get("nur_ausweichen") or p.get("modus") == "ring":
                    wahl = "ausweichen" if wahl != "verfehlt" and p.get("modus") == "ring" else "verfehlt"
                E.aktion("kampf_parade", {"ergebnis": wahl, "revision": k["revision"]})
                continue
            if k["phase"] != "spieler_wahl" or E.kampf.must_skip(k["spieler"]):
                E.aktion("kampf_zug", {"befehl": "aussetzen", "ziel": None, "revision": k["revision"]})
                continue
            zuege += 1
            befehl, ziel = self.zug(z, k, modul)
            try:
                E.aktion("kampf_zug", {"befehl": befehl, "ziel": ziel, "revision": k["revision"]})
            except ValueError:
                E.aktion("kampf_zug", {"befehl": "angriff", "ziel": None, "revision": E.aktiv()["kampf"]["revision"]})
        raise AssertionError("Kampf endet nicht")

    # ------------------------------------------------------------ Expedition
    def durchlauf(self, ort, praefix, wahl):
        E.aktion("ort_betreten", {"id": ort})
        modul = E.modul_laden()
        sek, frames, kaempfe = 0.0, [], []
        for _ in range(150):
            z = E.aktiv()
            if z["status"] == "kampf":
                lvl = (z["kampf"]["gegner"][0]["level"], E.kampf.progress(z)["level"])
                d, vorher = z["kampf"]["definition"], copy.deepcopy(z)
                erg, zuege, paraden = self.kampf(modul)
                kaempfe.append({"id": d, "ergebnis": erg, "zuege": zuege, "level": lvl})
                sek += 15 + 8 * zuege + 4 * paraden
                if erg in ("niederlage", "flucht", "entkommen"):         # weitermessen wie nach einem zweiten Versuch
                    E.kampf._finish(vorher, modul, vorher["kampf"], "ko")
                    E.sichern(vorher)
                    E.aktion("kampf_schliessen", {})
                self.aufbauen()
                continue
            ev = z.get("event") or {}
            if z["status"] != "ereignis" or not ev.get("id", "").startswith(praefix):
                break
            frames.append(ev["id"])
            sek += self.frame_zeit(self.evs.get(ev["id"], ev))
            if praefix == "rt_" and self.evs.get(ev["id"], {}).get("rast") and self.typ != "einfach":    # klug rastet am Feuer
                E.aktion("ort_rasten", {})
            liste = wahl.get(ev["id"]) or [0]
            E.aktion("event_wahl", {"index": liste.pop(0) if len(liste) > 1 else liste[0]})
            E.aktion("event_schliessen", {})
        return {"minuten": round(sek / 60, 1), "frames": frames, "kaempfe": kaempfe}


def kapitel(m):
    """Die gemessenen Wege: (Name, Vorbereitung, Ort, Praefix, Wahlen, Level)."""
    out = []

    def macchia(seed):
        K.bis_freie_phase(seed)
        K.flags_setzen("kloster_angenommen")
        K.inventar(frei=4)
    out.append(("Macchia (Faehrte)", lambda: macchia(7), "macchia", "kl_", {"kl_gabelung": [0], "kl_loewe_wahl": [0]}, 3))
    out.append(("Macchia (Schatz)", lambda: macchia(3), "macchia", "kl_", {"kl_gabelung": [1], "kl_loewe_wahl": [1]}, 3))

    def berge(seed):
        B.vorbereiten(seed)
        K.inventar(frei=4)
    out.append(("Berge (mit Umwegen)", lambda: berge(7), "berge", "bg_",
                {"bg_see_rast": [0], "bg_hochweide": [0], "bg_u1_wahl": [0], "bg_u2_wahl": [1]}, 4))
    out.append(("Berge (ohne Umwege)", lambda: berge(3), "berge", "bg_",
                {"bg_see_rast": [1], "bg_hochweide": [1], "bg_turm_f1": [1], "bg_turm_f2": [1], "bg_turm_f3": [1]}, 4))
    out.append(("Grotte (beide Umwege)", lambda: G.vorbereiten(7, "grotte_offen"), "grotte", "gr_",
                {"gr_strand": [0], "gr_u2_wahl": [0], "gr_teich": [0], "gr_u1_wahl": [0], "gr_wahl": [1]}, 4))
    out.append(("Grotte (ohne Umwege)", lambda: G.vorbereiten(3, "grotte_offen"), "grotte", "gr_",
                {"gr_strand": [1], "gr_teich": [1], "gr_halle": [0], "gr_wahl": [0]}, 4))

    def flut(sammeln):
        G.vorbereiten(5, "grotte_offen", "grotte_fertig")
        B.setzen(tag=12)
        G.bis_abend()
        if sammeln:
            K.flags_setzen("sirene_fertig")
    out.append(("Flut-Nacht (erster Besuch)", lambda: flut(False), "grotte_flut", "fn_", {"fn_teich": [0]}, 5))
    out.append(("Flut-Nacht (Sammel-Lauf)", lambda: flut(True), "grotte_flut", "fn_", {}, 5))

    def trio(seed, *flags):
        G.vorbereiten(seed, "kloster_angenommen", "kloster_fertig", "grotte_offen", "grotte_fertig", "kl_nische_geleert", "kl_loewe_frei", *flags)
        B.setzen(tag=12)
    pfade = ("rt_gestartet", "rt_getrennt")
    fertig = ("rt_danzel_fertig", "rt_bibi_fertig", "rt_charly_fertig")
    tisch = fertig + pfade + ("rt_notiz_gesteht", "rt_notiz_futter", "rt_notiz_spiel")
    out.append(("Red Trio I (Trio, Bruecke)", lambda: trio(7), "macchia", "rt_", {}, 5))
    for i, p in enumerate(("Koehlerweg", "Schlucht", "Mastgrat")):
        andere = tuple(f for j, f in enumerate(fertig) if j != i)
        out.append(("Red Trio II (%s)" % p, lambda a=andere: trio(7, *(pfade + a)), "macchia", "rt_", {}, 5))
    out.append(("Red Trio III (versoehnt)", lambda: trio(7, *tisch), "macchia", "rt_", {"rt_t_d2": [1], "rt_t_dc": [1]}, 5))
    out.append(("Red Trio III (getrennt)", lambda: trio(7, *tisch), "macchia", "rt_", {"rt_t_bruch": [1]}, 5))
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    typen = [a for a in sys.argv[1:] if a in PARADE] or list(PARADE)
    for typ in typen:
        print("\nSpielertyp: %s" % typ)
        m = Messung(typ, random.Random(28))
        for name, vorb, ort, praefix, wahl, lvl in kapitel(m):
            vorb()
            m.stufe(lvl)
            r = m.durchlauf(ort, praefix, copy.deepcopy(wahl))
            nieder = [k["id"] for k in r["kaempfe"] if k["ergebnis"] in ("niederlage", "flucht", "entkommen")]
            zuege = [k["zuege"] for k in r["kaempfe"]]
            print("%-30s %5.1f min | %2d Szenen | %2d Kaempfe, je %.1f Zuege | Niederlagen %d: %s" % (
                name, r["minuten"], len(r["frames"]), len(r["kaempfe"]), sum(zuege) / max(1, len(zuege)),
                len(nieder), ", ".join(nieder) or "-"))


if __name__ == "__main__":
    main()
