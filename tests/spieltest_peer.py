"""Evidence-based, offline review drafts; no invented dialogue or human enjoyment scores."""
import html
import statistics

from spieltest_profile import PROFILE, VERSION
from spieltest_reviewstruktur import ABSCHNITTE, VERSION as REVIEW_VERSION

HINWEIS = ("Simulierte interne Review-Peer-Group, keine Rezensionen der genannten Medien. "
           "Bewertet werden technische Beobachtungen und Prüfabdeckung, nicht menschlicher Spaß. "
           "Dialoge des Sprachmodells, Stimme, Bildwirkung und Bedienung im Browser wurden nicht getestet. "
           "Herkunft, Geschlecht und Sexualität sind Kontext und bestimmen keine Bewertung.")

KRITERIEN = {
    "stabilitaet": ("Stabilität und Speichern", "Erreichen alle Läufe das gebaute Ende ohne Fehler und Speicherabweichung?",
                    "Tatsächliche Ladezeiten und Verhalten auf verschiedenen PCs prüfen."),
    "kampf": ("Kampf und Schwierigkeit", "Welche Kämpfe, Ergebnisse, Züge und Hilfseingriffe wurden beobachtet?",
              "Spielgefühl, Fairness, Steuerung und Verständlichkeit menschlich prüfen; Rätselkämpfe gesondert ansehen."),
    "romance": ("Beziehungen und Dating", "Werden Dates, Szenen und Veränderungen von Vertrauen oder Begehren erreicht?",
                "Chemie, unterschiedliche Flirtstile, Figurenautonomie und glaubwürdige Zurückweisung im tatsächlichen Dialog prüfen."),
    "verzahnung": ("Verbindung von Alltag, Romance und Kampf", "Kommen die drei Systeme im selben Lauf vor?",
                   "Gemeinsames Vorkommen belegt keine Wechselwirkung: konkrete Beziehungs-/Kampffolgen und stimmige Übergänge spielen."),
    "entscheidungen": ("Entscheidungen und Konsequenzen", "Haben angebotene Antworten unterschiedliche definierte Folgen?",
                        "Unterschiedliche Daten sind kein Beleg für bedeutungsvolle Wahl: Risiko, Konsequenzen und erzählerische Wirkung prüfen."),
    "tempo": ("Tempo und Langzeitmotivation", "Wie viele Tage bleiben ohne Events, Kämpfe oder Belohnungen?",
              "Reale Sessionlänge, Grind, Dialogtempo, Wiederholungen und Langzeitmotivation prüfen; Botzeit ist keine Spielzeit."),
    "wirtschaft": ("Wirtschaft und Belohnungen", "Welche Einnahmen, Ausgaben und vollen Taschen treten auf?",
                   "Preise, lohnende Käufe und künstlichen Grind prüfen; Restgeld allein ist kein Balanceurteil."),
    "zugaenglichkeit": ("Zugänglichkeit und Zeitdruck", "Wie kommt das Profil mit seiner simulierten Geschicklichkeit zurecht?",
                        "Tastatur, Umbelegung, Lesbarkeit, motorische Zugänglichkeit, Zeitlimits und Schwierigkeitsoptionen im Browser prüfen."),
    "intimitaet": ("Intimität, Grenzen und Fanservice", "Werden Intimitätsangebote und freigeschaltete Aktionen erreicht?",
                   "Erotische Spannung, Kinks, Einvernehmen, Grenzen, Outfits und eingelöste Versprechen menschlich prüfen. Platzhalterdialoge belegen nichts davon."),
    "alltag": ("Gemütlicher Alltag", "Werden Kochen, Farm und Angeln tatsächlich genutzt?",
               "Entspannung, Atmosphäre, kreative Freiheit und störenden Pflichtcharakter menschlich prüfen."),
    "entdeckung": ("Entdeckung und Einstieg", "Welche Orte, Events und Szenen erreicht das Profil?",
                   "Der Bot kennt interne Zustände und Folgen. Er kann Orientierung ohne Guide und Überraschung nicht wie ein neuer Mensch testen."),
    "builds": ("Builds und Wiederspielwert", "Welche Fähigkeiten, Ausrüstung und Befehle werden ausprobiert?",
               "Vielfalt ist keine Balance: echte Synergien, alternative Spielweisen und Entscheidungen statt Zahlenwachstum prüfen."),
    "gedaechtnis": ("Figurentreue und Beziehungsgedächtnis", "Passen spätere Antworten zur Figur und zum tatsächlich geführten Gespräch?",
                    "Im Live-Pilot Versprechen, Wünsche, Ablehnung und spätere Reaktionen protokollieren und vergleichen. Offline-Platzhalter liefern dafür keinen Beleg."),
}


def messwerte(r):
    a = r.get("aktionen", {})
    peer = r.get("peer")
    sig = (peer or {}).get("signale", {})
    w = list((peer or {}).get("wahl_folgen", {}).values())
    multi = [e for e in w if e["optionen"] >= 2]
    fights = [k for k in r.get("kaempfe", []) if k.get("id") != "maxwell_training" and k.get("art")]
    return {
        "ende": r.get("ende", {}).get("status") == "ende",
        "fehler": len(r.get("abstuerze", [])) + len(r.get("sackgassen", [])) + len(r.get("speicher_abweichung", [])),
        "ablehnungen": sum(r.get("angebot_abgelehnt", {}).values()),
        "hilfe": len(r.get("hilfe", [])), "kaempfe": len(fights),
        "selbststaendig": r.get("ende", {}).get("status") == "ende" and not any(
            r.get(k) for k in ("abstuerze", "sackgassen", "speicher_abweichung", "hilfe", "lange_phasen")),
        "siege": sum(k["art"] in ("ko", "aufgabe") for k in fights),
        "entkommen": sum(k["art"] == "entkommen" for k in fights),
        "kaempfe_mit_hilfe": sum(bool(k.get("hilfe_aktiv")) for k in fights) if (peer or {}).get("version", 0) >= 2 else None,
        "zuege_median": statistics.median([k["zuege"] for k in fights]) if fights else None,
        "events": len(r.get("events", {})), "orte": len(r.get("orte", {})), "szenen": sum(r.get("szenen", {}).values()),
        "dates": max(sum(n for s, n in r.get("szenen", {}).items() if s.startswith("date_")), sig.get("dates_begonnen", 0)),
        "einladungen_versucht": sig.get("einladungen_versucht", 0) if (peer or {}).get("version", 0) >= 2 else None,
        "dates_vereinbart": sig.get("dates_vereinbart", 0) if (peer or {}).get("version", 0) >= 2 else None,
        "vertrauen_aenderungen": sig.get("vertrauen_aenderungen", 0) if peer else None,
        "begehren_aenderungen": sig.get("begehren_aenderungen", 0) if peer else None,
        "intim_aktionen": a.get("intim", 0),
        "intim_angebote": sig.get("intim_angebote_events", 0) + sig.get("intim_optionen_sichtbar", 0) if peer else None,
        "mehrfachwahlen": len(multi) if peer else None,
        "gleiche_folgen": sum(e["folgenvarianten"] == 1 for e in multi) if peer else None,
        "leere_tage": sum(not any(d.get(k, 0) for k in ("events", "kaempfe", "belohnungen")) for d in r.get("tage", [])),
        "tage": len(r.get("tage", [])), "einnahmen": sum(r.get("einnahmen", {}).values()),
        "ausgaben": sum(r.get("ausgaben", {}).values()), "konto": r.get("konto"),
        "tasche_voll_tage": r.get("tasche_voll_tage", 0),
        "alltag_aktionen": sum(a.get(k, 0) for k in ("kochen", "kochen_baukasten", "garten_pflanzen", "angeln_start", "tier_kaufen")),
        "skills_gelernt": a.get("skill_lernen", 0), "chips": a.get("chip_einsetzen", 0),
        "faehigkeiten_genutzt": len([k for k, v in r.get("befehle", {}).items() if k.startswith("f:") and v]),
        "waffen": sorted({k["waffe"] for k in fights if k.get("waffe")}),
    }


def date_diagnose(m):
    if m["dates"]:
        return "Date-Szene begonnen; Qualität getrennt prüfen."
    if m["einladungen_versucht"] is None:
        return "Alter Lauf ohne Einladungstelemetrie: Ursache der fehlenden Dates ungeklärt."
    if not m["einladungen_versucht"]:
        return "Keine Einladung versucht: Lücke im Testweg, kein Beleg für fehlenden Spielinhalt."
    if not m["dates_vereinbart"]:
        return "Einladung versucht, keine Verabredung beobachtet: Probe, Voraussetzungen oder Antwort prüfen."
    return "Verabredung vorhanden, keine Date-Szene begonnen: Kalender, Ort und Szenenübergang prüfen."


def kriterium(id, r, m):
    """Status concerns a measured check/coverage only; unknown is never green."""
    status, art = "gruen", "Messprüfung"
    if id == "stabilitaet":
        keys = ["ende", "selbststaendig", "fehler", "ablehnungen", "hilfe"]
        status = "rot" if m["fehler"] or not m["ende"] else "gelb" if m["ablehnungen"] or not m["selbststaendig"] else "gruen"
    elif id in ("kampf", "zugaenglichkeit"):
        keys = ["kaempfe", "siege", "entkommen", "zuege_median", "hilfe", "kaempfe_mit_hilfe"]
        status = "gelb" if m["hilfe"] else "gruen" if m["kaempfe"] else "offen"
    elif id == "romance":
        keys = ["szenen", "einladungen_versucht", "dates_vereinbart", "dates", "vertrauen_aenderungen", "begehren_aenderungen"]
        status, art = ("gruen" if m["dates"] and m["vertrauen_aenderungen"] else "offen"), "Prüfabdeckung"
    elif id == "verzahnung":
        keys = ["kaempfe", "dates", "alltag_aktionen"]
        status, art = ("gruen" if all(m[k] for k in keys) else "offen"), "Gemeinsames Vorkommen, keine Qualitätswertung"
    elif id == "entscheidungen":
        keys = ["mehrfachwahlen", "gleiche_folgen"]
        n = m["mehrfachwahlen"]
        status = "offen" if not n else "gelb" if m["gleiche_folgen"] / n >= .25 else "gruen"
        art = "Heuristik: identische definierte Folgen ab 25 % auffällig"
    elif id == "tempo":
        keys = ["tage", "leere_tage"]
        status = "offen" if not m["tage"] else "gelb" if m["leere_tage"] else "gruen"
    elif id == "wirtschaft":
        keys = ["einnahmen", "ausgaben", "konto", "tasche_voll_tage"]
        status = "offen" if not m["einnahmen"] and not m["ausgaben"] else "gelb" if m["tasche_voll_tage"] else "gruen"
    elif id == "intimitaet":
        keys = ["intim_angebote", "intim_aktionen"]
        status, art = ("gruen" if m["intim_aktionen"] else "offen"), "Prüfabdeckung, keine Inhaltswertung"
    elif id == "alltag":
        keys = ["alltag_aktionen"]
        status, art = ("gruen" if m["alltag_aktionen"] else "offen"), "Prüfabdeckung"
    elif id == "entdeckung":
        keys = ["orte", "events", "szenen"]
        status, art = ("gruen" if m["orte"] and m["events"] else "offen"), "Prüfabdeckung"
    elif id == "gedaechtnis":
        keys = ["szenen", "dates"]
        status, art = "offen", "Kein Test echter Dialogkontinuität; gezielter Live-Pilot erforderlich"
    else:
        keys = ["skills_gelernt", "chips", "faehigkeiten_genutzt", "waffen"]
        status, art = ("gruen" if m["faehigkeiten_genutzt"] >= 2 else "offen"), "Prüfabdeckung, keine Balancewertung"
    return dict(status=status, art=art, messwerte={k: m[k] for k in keys}, lauf="%s/%s" % (r["typ"], r["seed"]))


def auswerten(roh):
    reviews = []
    for pid, p in PROFILE.items():
        runs = [r for r in roh["laeufe"] if r["typ"] == pid]
        kriterien = []
        for kid, gewicht in sorted(p["gewichte"].items(), key=lambda kv: -kv[1]):
            titel, frage, manuell = KRITERIEN[kid]
            belege = [kriterium(kid, r, messwerte(r)) for r in runs]
            stufen = [b["status"] for b in belege]
            status = "rot" if "rot" in stufen else "gelb" if "gelb" in stufen else "offen" if not stufen or "offen" in stufen else "gruen"
            kriterien.append(dict(id=kid, titel=titel, prioritaet=gewicht, frage=frage, status=status,
                                  belege=belege, menschlich=manuell))
        mess = [messwerte(r) for r in runs]
        blocker = any(not m["ende"] or m["fehler"] for m in mess)
        offen = sum(k["status"] == "offen" for k in kriterien)
        auffaellig = [k["titel"] for k in kriterien if k["status"] in ("gelb", "rot")]
        # Distinct question-led prose; every empirical statement comes from the same profile's runs.
        if not runs:
            text = "Für meine Perspektive liegt kein Lauf vor. Ich gebe noch kein Urteil ab."
        else:
            text = ("Ich prüfe Eden Rise mit Blick auf %s. In %d von %d Läufen erreiche ich das gebaute Ende. "
                    "Meine wichtigsten Prüffelder sind %s. " % (
                        p["vorlieben"], sum(m["ende"] for m in mess), len(runs),
                        ", ".join(k["titel"] for k in kriterien[:3])))
            text += ("Auffällig sind: %s. " % ", ".join(auffaellig)) if auffaellig else "In meinen gewählten Messprüfungen gibt es keine Warnung. "
            text += "%d Prüffelder bleiben mangels Abdeckung offen. " % offen
            text += "Mein inhaltliches Urteil bleibt vorläufig: %s" % p["fragen"][0]
        versionen = sorted({str(r.get("profil_version", roh.get("profil_version", "unbekannt"))) for r in runs})
        historisch = bool(runs) and versionen != [str(VERSION)]
        reviews.append(dict(id=pid, profil=p, laeufe=len(runs), seeds=[r["seed"] for r in runs],
                            status="nicht_getestet" if not runs else "blockiert" if blocker else "mit_hilfe" if any(not m["selbststaendig"] for m in mess) else "vorlaeufig",
                            laufstand=dict(profil_versionen=versionen, aktuelle_profilversion=VERSION, historisch=historisch,
                                hinweis="Kein Lauf vorhanden." if not runs else "Historische Messungen; die geänderte Testlogik wurde damit nicht erneut gespielt." if historisch else "Messungen dieser Profilversion."),
                            reviewstruktur=ABSCHNITTE,
                            review=text, kriterien=kriterien, menschliche_fragen=p["fragen"],
                            laufdaten=[dict(lauf="%s/%s" % (r["typ"], r["seed"]), messwerte=messwerte(r),
                                           date_diagnose=date_diagnose(messwerte(r)), testmodus=r.get("testmodus", {"dialog": "platzhalter", "wissen": "intern/alt"}),
                                           hilfe=r.get("hilfe", []), entscheidungen=(r.get("peer") or {}).get("entscheidungen", []),
                                           belege=(r.get("peer") or {}).get("belege", [])) for r in runs]))
    # Technical blockers from any profile remain visible irrespective of its taste weights.
    blocker = [{"lauf": "%s/%s" % (r["typ"], r["seed"]), "ende": r.get("ende"),
                "abstuerze": r.get("abstuerze", []), "sackgassen": r.get("sackgassen", []),
                "speicher_abweichung": r.get("speicher_abweichung", [])}
               for r in roh["laeufe"] if messwerte(r)["fehler"] or not messwerte(r)["ende"]]
    quer = [{"kriterium": kid, "titel": spec[0], "profile": {
        r["id"]: next((dict(status=k["status"], prioritaet=k["prioritaet"]) for k in r["kriterien"] if k["id"] == kid), None)
        for r in reviews}} for kid, spec in KRITERIEN.items()]
    spannungen = [
        "Noor / Tandi: Hypothese prüfen, ob zugängliche Kämpfe und anspruchsvolle Builds gleichzeitig möglich sind.",
        "Naomi / Lenny: Hypothese prüfen, ob erotische Spannung und Figurenautonomie neben lohnenden Freischaltungen bestehen.",
        "Deniz / Avery: Hypothese prüfen, ob kurze Sessions und wirtschaftlicher Fortschritt genug Raum für freie Entdeckung lassen.",
    ]
    return dict(version=VERSION, review_schema_version=REVIEW_VERSION, hinweis=HINWEIS, commit=roh["commit"], zeit=roh["zeit"],
                dirty=roh.get("dirty", False), blocker=blocker, quervergleich=quer,
                wieder=roh.get("wieder"), spannungsfelder=spannungen, reviews=reviews)


def markdown(d):
    out = ["# Eden Rise – simulierte Review-Peer-Group", "", HINWEIS, "",
           "Stand: %s · Commit: %s%s" % (d["zeit"], d["commit"], " + lokale Änderungen" if d["dirty"] else ""), "",
           "Grün = Messprüfung/Abdeckung erfüllt; Gelb = Auffälligkeit; Rot = technischer Fehler; Offen = nicht belegt. Keine Gesamtnote.", ""]
    out += ["## Perspektiven im Vergleich", "", "| Prüffeld | " + " | ".join(r["id"] for r in d["reviews"]) + " |",
            "|---|" + "---|" * len(d["reviews"])]
    for q in d["quervergleich"]:
        out += ["| %s | %s |" % (q["titel"], " | ".join(
            "%s (%d/3)" % (v["status"], v["prioritaet"]) if v else "–" for v in q["profile"].values()))]
    out += ["", "### Zu prüfende Zielkonflikte", ""] + ["- " + s for s in d["spannungsfelder"]] + [""]
    if d.get("wieder"):
        out += ["Wiederholungsprüfung: %s/%s · gleicher Endzustand: %s" % (
            d["wieder"]["typ"], d["wieder"]["seed"], d["wieder"]["gleich"]), ""]
    if any(r["laufstand"]["historisch"] for r in d["reviews"]):
        out.insert(4, "**Neuauswertung historischer Läufe. Die neue Testlogik wurde noch nicht im Spiel ausgeführt.**")
    if d["blocker"]:
        out += ["## Technische Blocker", ""] + ["- %s: %s" % (b["lauf"], b["ende"]) for b in d["blocker"]] + [""]
    for r in d["reviews"]:
        p = r["profil"]
        out += ["## %s – %s" % (p["name"], p["medium"]), "", p["hintergrund"], "",
                "Format: %s · Stil: %s" % (p["format"], p["ton"]), "", "Persona: " + p["persona"], "",
                "**Simulierter Review-Entwurf · %s · %d Läufe**" % (r["status"], r["laeufe"]), "", r["review"], ""]
        out += [r["laufstand"]["hinweis"], "", "### Review-Aufbau", ""] + [
            "- **%s:** %s" % (key.replace("_", " "), desc) for key, desc in r["reviewstruktur"].items()] + [""]
        for lauf in r["laufdaten"]:
            out += ["- `%s`: %s Selbstständig erreicht: %s. Hilfseingriffe: %d." % (
                lauf["lauf"], lauf["date_diagnose"], lauf["messwerte"]["selbststaendig"], len(lauf["hilfe"]))]
        out += [""]
        for k in r["kriterien"]:
            out += ["### %s · %s · Priorität %d/3" % (k["titel"], k["status"], k["prioritaet"]), "", k["frage"], ""]
            for b in k["belege"]:
                out += ["- `%s` · %s · %s: %s" % (b["lauf"], b["status"], b["art"],
                         "; ".join("%s=%s" % (key, value) for key, value in b["messwerte"].items()))]
            out += ["", "Menschlich offen: " + k["menschlich"], ""]
        out += ["### Persönliche Prüffragen", ""] + ["- " + f for f in r["menschliche_fragen"]] + [""]
    return "\n".join(out)


def seite(d):
    e = lambda x: html.escape(str(x))
    out = ["<!doctype html><html lang='de'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>",
           "<title>Eden Rise – Review-Peer-Group</title><style>body{font:16px/1.6 system-ui;background:#f5f4f0;color:#23241f;margin:0}main{max-width:1100px;margin:auto;padding:24px}article,header{background:white;border:1px solid #ddd;border-radius:12px;padding:24px;margin:16px 0}table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;border-bottom:1px solid #ddd;padding:10px}pre{white-space:pre-wrap;overflow-wrap:anywhere}h1,h2{line-height:1.2}.rolle{overflow-x:auto}.offen{color:#666}.gelb{color:#856000}.rot{color:#b02020}.gruen{color:#176b39}a{color:#225d78}</style><main>",
           "<header><h1>Eden Rise · Review-Peer-Group</h1><p>%s</p><p>%s · %s%s</p>" % (
               e(HINWEIS), e(d["zeit"]), e(d["commit"]), " + lokale Änderungen" if d["dirty"] else ""),
           "<p>Grün: Messprüfung oder Abdeckung erfüllt · Gelb: Auffälligkeit · Rot: technischer Fehler · Offen: nicht belegt. Keine Gesamtnote.</p>",
           "<nav>" + " · ".join("<a href='#%s'>%s</a>" % (r["id"], e(r["profil"]["name"])) for r in d["reviews"]) + "</nav></header>"]
    if any(r["laufstand"]["historisch"] for r in d["reviews"]):
        out += ["<article><b>Neuauswertung historischer Läufe.</b> Die neue Testlogik wurde noch nicht im Spiel ausgeführt.</article>"]
    out += ["<article><h2>Perspektiven im Vergleich</h2><p>Status (persönliche Priorität / 3). Ein Strich bedeutet: kein Schwerpunkt dieses Profils.</p><div class='rolle'><table><thead><tr><th>Prüffeld</th>" +
            "".join("<th>%s</th>" % e(r["id"]) for r in d["reviews"]) + "</tr></thead><tbody>"]
    for q in d["quervergleich"]:
        out += ["<tr><th>%s</th>%s</tr>" % (e(q["titel"]), "".join(
            "<td class='%s'>%s (%d)</td>" % (v["status"], e(v["status"]), v["prioritaet"]) if v else "<td>–</td>"
            for v in q["profile"].values()))]
    out += ["</tbody></table></div><h3>Zu prüfende Zielkonflikte</h3><ul>" +
            "".join("<li>%s</li>" % e(s) for s in d["spannungsfelder"]) + "</ul></article>"]
    if d.get("wieder"):
        out += ["<article><b>Wiederholungsprüfung:</b> %s/%s · gleicher Endzustand: %s</article>" % (
            e(d["wieder"]["typ"]), e(d["wieder"]["seed"]), e(d["wieder"]["gleich"]))]
    if d["blocker"]:
        out += ["<article><h2 class='rot'>Technische Blocker</h2><pre>%s</pre></article>" % e(str(d["blocker"]))]
    for r in d["reviews"]:
        p = r["profil"]
        out += ["<article id='%s'><h2>%s</h2><p>%s · %s</p><p>%s</p><p><b>%s</b> · %s</p><p>%s</p><p><b>%s · %d Läufe</b></p><p>%s</p>" % (
            r["id"], e(p["name"]), e(p["medium"]), e(p["persona"]), e(p["hintergrund"]), e(p["format"]), e(p["ton"]),
            e(p["vorlieben"]), e(r["status"]), r["laeufe"], e(r["review"])),
            "<div class='rolle'><table><thead><tr><th>Prüffeld</th><th>Messstatus und Belege je Seed</th><th>Menschlich offen</th></tr></thead><tbody>"]
        out.insert(len(out) - 1, "<p><b>%s</b></p><details><summary>Aufbau der persönlichen Rezension</summary><ol>%s</ol></details><ul>%s</ul>" % (
            e(r["laufstand"]["hinweis"]), "".join("<li>%s</li>" % e(desc) for desc in r["reviewstruktur"].values()),
            "".join("<li>%s: %s Selbstständig erreicht: %s. Hilfseingriffe: %d.</li>" % (
                e(lauf["lauf"]), e(lauf["date_diagnose"]), e(lauf["messwerte"]["selbststaendig"]), len(lauf["hilfe"])) for lauf in r["laufdaten"])))
        for k in r["kriterien"]:
            details = "".join("<details><summary>%s · %s</summary><p>%s</p><pre>%s</pre></details>" % (
                e(b["lauf"]), e(b["status"]), e(b["art"]), e("\n".join("%s: %s" % kv for kv in b["messwerte"].items()))) for b in k["belege"])
            out += ["<tr><td><b>%s</b><br>Priorität %d/3<br>%s</td><td><b class='%s'>%s</b>%s</td><td>%s</td></tr>" % (
                e(k["titel"]), k["prioritaet"], e(k["frage"]), k["status"], e(k["status"]), details, e(k["menschlich"]))]
        out += ["</tbody></table></div><h3>Persönliche Prüffragen</h3><ul>" + "".join("<li>%s</li>" % e(f) for f in r["menschliche_fragen"]) + "</ul></article>"]
    return "".join(out) + "</main></html>"
