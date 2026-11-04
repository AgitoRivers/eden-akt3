# -*- coding: utf-8 -*-
"""Abschluss der Hauptstory eden_rise (B4, 18.10.2026) - das Ende aus Ducs Entscheidungen, nie aus Zufall.

story.json "ende": vier Dimensionen (Schiff, Aufklaerung, Gemeinschaft, Zukunft), ein konsistenter Grundabschluss plus
je Dimension ein gepruefter Absatz, dazu fuer jede Frau ein eigener kurzer Abschluss (auch ohne Romanze).
Woraus jede Dimension entsteht:
  Schiff       technischer Weg (Tag 6), Isolation, Warnzeichen, Hilfe (Material aus dem Dorf oder Megans Kooperation)
  Aufklaerung  Kette belegt, zweite Wahrheit bekannt, Berichtsfassung, Endfassung, offene falsche Vorwuerfe
  Gemeinschaft Crew-Moral (Rueckhalt), gehaltenes Versprechen, oeffentliche Korrektur, offene falsche Vorwuerfe
  Zukunft      Antwort am letzten Abend (see / posten / offen) und die vertrauteste Frau
Texte sind deutsch (Oberflaeche); ab hier ist die Aufloesung erlaubt - das Spiel ist vorbei.

Akt-Stories (story "akt": 1, seit 24.10.2026): statt des Gesamtendes eine Schlusskarte "Ende von Akt 1" in derselben
Form (titel, absaetze, frauen leer, fall) - Anhoerung, Crew, Was bleibt. Das Urteil kommt aus der Anhoerung
(ermittlung.stand(z)["urteil"], Scheibe 3); fehlt es, wird es aus Kette, Gestaendnis und Vorwuerfen abgeleitet."""
from . import ermittlung, hauptstory, moral


def _name(modul, pid):
    p = modul["personen"].get(pid, {})
    return p.get("kurz") or p.get("name", "?").split(" ")[0]


AKT2_BETA = {"titel": "End of Act 2", "akt": 2, "dimensionen": {}, "frauen": [], "fall": None,
             "absaetze": [{"titel": "Act 3", "text": "Coming soon."},
                          {"titel": "Beta", "text": "You reached the ending of the Beta release. Thank you so much for testing and supporting."}]}


AKT3_BETA = {"titel": "End of Act 3", "akt": 3, "dimensionen": {}, "frauen": [], "fall": None,
             "absaetze": [{"titel": "The Festa", "text": "The endings are coming soon."},
                          {"titel": "Beta", "text": "You reached the ending of the Beta release. Thank you so much for testing and supporting."}]}


def akt3_ende(z, modul):
    """Schlusskarte Akt 3 (Paket F): welches Ende, welche Saeulen, wer ausgesagt hat, Minicu, Pascal, Minas Epilog.
    Platzhalter-Texte bis zum Feinschliff (enden.md, Duc). Ohne Saeulen-Daten: AKT3_BETA."""
    from . import akt3
    if "a3_festa_fertig" not in z.get("flags", []):
        return dict(AKT3_BETA)
    eid, s = akt3.ende(z), akt3.saeulen(z)
    namen = [_name(modul, p) for p in akt3.zeugen(z) if p in modul.get("personen", {})]
    saeule = {"wahrheit": "Truth", "geld": "Money", "gemeinschaft": "Community", "staerke": "Strength"}
    bild, buena, pascal = akt3.ENDE_TEXT[eid]
    if eid == "2b" and "a3_mast_aus" in z.get("flags", []):     # The Red Light: der Mast auf dem Kamm ist dunkel
        bild = "The most beautiful festa the bay has seen. At midnight, the ridge above San Martinu stays dark."
    fehlt = [akt3.FEHLT[k] for k, v in s.items() if not v] if eid in ("0", "2.5a", "2.5b", "2.5c", "2a", "2b", "2c") else []
    absaetze = [
        {"titel": "The Last Picture", "text": bild},
        {"titel": "The Pillars", "text": " · ".join("%s %s" % (saeule[k], "✓" if v else "–") for k, v in s.items())}]
    if fehlt:                                          # F-35: fair erklaert, was gefehlt hat
        absaetze.append({"titel": "What Was Missing", "text": " ".join(fehlt)})
    absaetze += [
        {"titel": "Who Saw It", "text": ("They signed their names: " + ", ".join(namen) + ".") if namen else "Nobody signed."},
        {"titel": "Minicu", "text": "Minicu is in the picture, a bandage around his head, clapping much too loud."
                                    if eid != "1" else "Minicu carries crates at the harbour, for A.V., and doesn't ask."},
        {"titel": "Buenaventura", "text": buena},
        {"titel": "Pascal", "text": pascal},
        {"titel": "Epilogue", "text": "Mina rings at Pascal's door with a registered letter. “Sign here.” Nobody opens. "
                                      "It's the first letter she can't deliver."},
        {"titel": "Beta", "text": "The endings are still being polished. Thank you so much for testing and supporting."}]
    if eid == "stern":
        absaetze[0]["text"] += " You played the long game."
    return {"titel": "Ending: " + akt3.ENDEN[eid], "akt": 3, "ende": eid, "saeulen": s, "dimensionen": {}, "frauen": [],
            "fall": None, "absaetze": absaetze}


def berechnen(z, modul):
    if "akt2_ende" in z.get("flags", []):          # Cliffhanger Akt 2 gesehen (Duc 02.11.2026): Schluss der Beta
        # Akt 3 (Drehbuch akt3): solange modul.akt3_spielbar fehlt, endet die Beta nach Tag 23. Danach Platzhalter bis zu den Enden (Paket F).
        return akt3_ende(z, modul) if modul.get("akt3_spielbar") else dict(AKT2_BETA)
    if not ermittlung.aktiv(z):
        return None
    if (ermittlung._story(z) or {}).get("akt") == 1:
        return akt1(z, modul)
    f, e, F = ermittlung.fall(z), ermittlung.stand(z), z["flags"]
    kette = ermittlung.kette_bekannt(z)
    zweite = ermittlung.kennt(z, "z_01") or ermittlung.kennt(z, "z_02")
    haltung = ermittlung.megan_haltung(z)
    v = f.get("verantwortlich")

    # ---------------------------------------------------------------- Schiff
    brand = "brand" in F
    schiff = schiff_ergebnis(z, modul)

    # ---------------------------------------------------------------- Aufklaerung
    falsch_offen = [x["pid"] for x in e["vorwuerfe"] if x["oeffentlich"] and x["pid"] != v and not x.get("korrigiert")]
    korrigiert = "endfassung_korrigiert" in F
    if falsch_offen:
        auf = "falsch"
    elif "bericht_vollstaendig" in F or korrigiert:
        auf = "vollstaendig" if kette and zweite else "vorlaeufig_ehrlich"
    elif "bericht_vorlaeufig" in F:
        auf = "vorlaeufig_ehrlich"
    elif "bericht_pro_crew" in F or "bericht_pro_firma" in F:
        auf = "beschoenigt"
    else:
        auf = "vorlaeufig_ehrlich"

    # ---------------------------------------------------------------- Gemeinschaft
    punkte = moral.alte_skala(z, modul)
    punkte += (z["werte"].get("rueckhalt", 50) - 50) // 20          # Rueckhalt aus Bordrat und Versprechen (B5)
    punkte += 1 if "vorhaben_versprechen" in F else 0
    punkte += 1 if any(x.get("korrigiert") for x in e["vorwuerfe"]) else 0
    punkte -= 2 * len(falsch_offen)
    punkte -= 1 if "bericht_pro_firma" in F and not korrigiert else 0
    punkte -= 1 if brand else 0
    gemeinschaft = "getragen" if punkte >= 4 else "angeschlagen" if punkte >= 2 else "zerbrochen"

    # ---------------------------------------------------------------- Zukunft
    partner = hauptstory.partner(z, modul)
    nah = partner and z["werte"].get("vertrauen." + partner, 0) >= 3 and z["werte"].get("begehren." + partner, 0) >= 3
    if "zukunft_offen" in F:
        zukunft = "offen"
    elif nah:
        zukunft = "person"
    else:
        zukunft = "allein"
    weg = "posten" if "zukunft_posten" in F else "see" if "zukunft_see" in F else "offen"

    absaetze = [
        ("Das Schiff", SCHIFF[schiff] + (" " + BRAND if brand else "")),
        ("Die Wahrheit", AUFKLAERUNG[auf] + (" " + GESTAENDNIS if e.get("gestaendnis") else "")
         + (" " + ZWEITE if zweite else " " + ZWEITE_NICHT)),
        ("Die Crew", GEMEINSCHAFT[gemeinschaft]),
        ("Du", ZUKUNFT[(zukunft, weg)].format(name=_name(modul, partner) if partner else "")),
    ]
    frauen = [{"id": p, "name": _name(modul, p), "text": frau_text(z, modul, p, partner if zukunft == "person" else None)}
              for p in hauptstory.frauen(modul)]
    titel = TITEL.get((schiff, auf), TITEL_GRUND.get(auf, "Ende der Fahrt"))
    return {"titel": titel, "dimensionen": {"schiff": schiff, "brand": brand, "aufklaerung": auf,
                                            "gemeinschaft": gemeinschaft, "zukunft": zukunft, "weg": weg},
            "absaetze": [{"titel": t, "text": x} for t, x in absaetze], "frauen": frauen,
            "fall": {"nr": f.get("nr"), "titel": f.get("kurz", ""), "kette": kette,
                     "glieder": ermittlung.glieder_status(z),
                     "verantwortlich": _name(modul, v) if v else None,
                     "wiedergutmachung": f.get("wiedergutmachung", "") if e.get("gestaendnis") else ""}}


def _gemeinschaft(z, falsch_offen, e, modul=None):
    punkte = moral.alte_skala(z, modul) if modul else z["werte"].get("moral", 3)
    punkte += (z["werte"].get("rueckhalt", 50) - 50) // 20
    punkte += 1 if "vorhaben_versprechen" in z["flags"] else 0
    punkte += 1 if any(x.get("korrigiert") for x in e["vorwuerfe"]) else 0
    punkte -= 2 * len(falsch_offen)
    return "getragen" if punkte >= 4 else "angeschlagen" if punkte >= 2 else "zerbrochen"


def urteil(z):
    """erbarmen / aufgeklaert / falsch / offen - aus der Anhoerung, sonst aus dem Ermittlungsstand abgeleitet."""
    e, f = ermittlung.stand(z), ermittlung.fall(z)
    if e.get("urteil"):
        return e["urteil"]
    v = f.get("verantwortlich")
    if any(x["oeffentlich"] and x["pid"] != v and not x.get("korrigiert") for x in e["vorwuerfe"]):
        return "falsch"
    if ermittlung.kette_bekannt(z) or e.get("gestaendnis"):
        return "aufgeklaert"
    return "offen"


def akt1(z, modul):
    f, e = ermittlung.fall(z), ermittlung.stand(z)
    v = f.get("verantwortlich")
    falsch_offen = [x["pid"] for x in e["vorwuerfe"] if x["oeffentlich"] and x["pid"] != v and not x.get("korrigiert")]
    u = urteil(z)
    gemeinschaft = _gemeinschaft(z, falsch_offen, e, modul)
    bleibt = AKT1_BLEIBT + (" " + AKT1_LICHT if ermittlung.kennt(z, "z_01") else "")
    absaetze = [("The Hearing", AKT1_URTEIL[u] + (" " + GESTAENDNIS if e.get("gestaendnis") else "")),
                ("The Crew", AKT1_CREW[gemeinschaft]),
                ("What Remains", bleibt)]
    return {"titel": "End of Act 1", "akt": 1,
            "dimensionen": {"urteil": u, "gemeinschaft": gemeinschaft, "megan_haltung": ermittlung.megan_haltung(z)},
            "absaetze": [{"titel": t, "text": x} for t, x in absaetze], "frauen": [],
            "fall": {"nr": f.get("nr"), "titel": f.get("kurz", ""), "kette": ermittlung.kette_bekannt(z),
                     "glieder": ermittlung.glieder_status(z),
                     "verantwortlich": _name(modul, v) if v else None,
                     "wiedergutmachung": f.get("wiedergutmachung", "") if e.get("gestaendnis") else ""}}


AKT1_URTEIL = {
    # Englisch seit 28.10.2026 (Duc: alles Spieler-Sichtbare Englisch)
    "erbarmen": "You laid the chain out in front of Megan, link by link, and then you asked for mercy. Megan was quiet "
                "for a long time. Then she put her pen down. The person stays aboard – and everyone saw that the boss "
                "has a heart.",
    "aufgeklaert": "You proved what happened that night. Megan passed judgement, just the way she said she would. The "
                   "crew stays. It was fair. It wasn't easy.",
    "falsch": "Megan has passed judgement – on a name that doesn't belong there. You said it and never took it back. "
              "The truth about that night is still somewhere on board.",
    "unbelegt": "You had the right suspicion, but not a complete chain. Megan doesn't convict anyone on a gut feeling – "
                "she judged for herself: the bonus is cancelled, and the question stays open.",
    "entlastet": "You showed that nobody did it alone – a chain of small things, proven link by link. Megan checked "
                 "every one of them and accepted it. Whoever was blamed all week is cleared.",
    "offen": "You stood in front of Megan with almost nothing in your hands. She judged for herself: the bonus is "
             "cancelled, and she has written a few names on her list. The questions about that night stay open.",
}
AKT1_CREW = {
    "getragen": "In the evening everyone sits together in the mess. Nobody talks about the verdict, but someone puts a "
                "plate in front of you before you have to ask.",
    "angeschlagen": "The crew is tired and careful. People talk to each other, but not about everything. This week has "
                    "left its marks.",
    "zerbrochen": "The mess is half empty. Whoever is there doesn't look at you. This crew has to become a crew again.",
}
AKT1_BLEIBT = ("The Eden Rise is still lying in the bay of Cala d'Orsu, and the inverter is a black hole in the "
               "drive room. And at night, high up in the hills, a red light is blinking. From the macchia comes a howl "
               "that no dog makes.")
AKT1_LICHT = "You know the rhythm of that light. You've seen it before – behind the inverter."


def schiff_ergebnis(z, modul=None):
    """eigenfahrt / schlepp / verlust - aus technischem Weg, Brand und Hilfe (Material oder Megans Kooperation)."""
    F = z["flags"]
    brand = "brand" in F
    hilfe = "vorhaben_material" in F or ermittlung.megan_haltung(z) >= 1
    if "weg_schlepp" in F:
        schiff = "schlepp"
    elif "weg_isolation" in F:
        schiff = "eigenfahrt" if hilfe else "schlepp"
    else:
        schiff = "eigenfahrt" if hilfe and not brand else "schlepp"
    if brand and (moral.meuterei(z, modul) if modul else z["werte"].get("moral", 3) <= 1):
        schiff = "verlust"
    return schiff


SCHIFF_BILD = {"eigenfahrt": "calvi_harbour.png", "schlepp": "yacht_under_tow.png",
               "verlust": "yacht_swim_platform_rescue_dawn.png"}


def szenenbild(z, sid):
    """Bilder, die vom Spielverlauf abhaengen (B4): Auslaufen je Ausgang, technischer Weg mit Warnzeichen."""
    if not ermittlung.aktiv(z):
        return None
    if sid == "auslaufen":
        return SCHIFF_BILD[schiff_ergebnis(z)]
    if sid == "technischer_weg" and "warnung_5" in z["flags"] and "warnzeichen_beachtet" not in z["flags"]:
        return "yacht_power_room_smoke.png"
    return None


def frau_text(z, modul, pid, partner):
    vt = z["werte"].get("vertrauen." + pid, 0)
    stufe = "hoch" if vt >= 4 else "mitte" if vt >= 2 else "tief"
    if pid == partner:
        return FRAU[pid]["partner"]
    return FRAU.get(pid, {}).get(stufe, "")


TITEL_GRUND = {"vollstaendig": "Die ganze Wahrheit", "vorlaeufig_ehrlich": "Was wir wissen",
               "beschoenigt": "Eine saubere Fassung", "falsch": "Der falsche Name"}
TITEL = {("eigenfahrt", "vollstaendig"): "Aus eigener Kraft", ("verlust", "falsch"): "Asche und Papier",
         ("verlust", "beschoenigt"): "Asche und Papier"}

SCHIFF = {
    "eigenfahrt": "Die Eden Rise läuft aus eigener Kraft in Calvi ein. Langsam, mit einem Ersatzteil, das jemand "
                  "für euch besorgt hat, und mit Rosi, die die ganze Fahrt die Messwerte nicht aus den Augen lässt. "
                  "Die Werft nimmt sie pünktlich.",
    "schlepp": "Ein Schlepper zieht die Eden Rise nach Calvi. Niemand an Bord schämt sich dafür – eine sichere "
               "Ankunft ist eine Ankunft. Die Werft bekommt ein Schiff, das sie reparieren kann.",
    "verlust": "Die Eden Rise erreicht Calvi nicht mehr aus eigener Kraft und nicht mehr als das Schiff, das sie war. "
               "Was vom Achterschiff übrig ist, wird in die Werft geschleppt; die Versicherung spricht von Totalschaden.",
}
BRAND = ("In der letzten Nacht hat es im Technikraum gebrannt. Die Warnzeichen waren da – Wärme, Geruch, die "
         "Messwerte. Alle sind von Bord gekommen. Das Schiff trägt die Spuren.")
AUFKLAERUNG = {
    "vollstaendig": "Dein Bericht ist vollständig und belegbar: was in der Nacht passiert ist, wer es ausgelöst hat "
                    "und warum es den Antrieb zerstören konnte. Auch deine eigene Rolle steht darin.",
    "vorlaeufig_ehrlich": "Dein Bericht sagt, was belegt ist, und nennt offen, was nicht belegt ist. Er ist nicht "
                          "vollständig, aber er lügt nicht. Wer ihn liest, weiß, wo weitergefragt werden muss.",
    "beschoenigt": "Dein Bericht ist sauber formuliert und lässt etwas weg. Es fällt nicht sofort auf. Aber die, die "
                   "es wissen, wissen auch, dass du es weißt.",
    "falsch": "Ein Name steht im Raum, der nicht dorthin gehört – du hast ihn vor allen ausgesprochen und nicht "
              "zurückgenommen. Daran ändert auch der beste Bericht nichts mehr.",
}
GESTAENDNIS = "The person who set it off told you so themselves – and is helping to put it right."
ZWEITE = ("Und du weißt, was die Zentrale vor der Reise wusste: die Meldung zum Modul, die Entscheidung, trotzdem "
          "weiterzufahren. Persönliche Verantwortung und das Versagen der Organisation stehen getrennt im Bericht.")
ZWEITE_NICHT = ("Was die Zentrale vor der Reise wusste, hast du nicht herausgefunden. Die Werft wird das Modul "
                "tauschen, und niemand wird fragen, warum es überhaupt noch eingebaut war.")
GEMEINSCHAFT = {
    "getragen": "Die Crew trägt dich. Weniger Geld, weniger Komfort, eine Woche, die keiner vergisst – und trotzdem "
                "sitzen am letzten Abend alle an einem Tisch, und jemand stellt noch einen Stuhl dazu.",
    "angeschlagen": "Die Crew ist angeschlagen. Man redet miteinander, aber nicht mehr über alles. Ein paar werden "
                    "nach Calvi abmustern, ein paar bleiben – deinetwegen oder trotz dir.",
    "zerbrochen": "Die Crew ist zerbrochen. Am letzten Abend sitzen nur noch wenige zusammen, und keiner sieht dich "
                  "an, wenn du die Messe betrittst.",
}
ZUKUNFT = {
    ("person", "see"): "Du bleibst auf See. {name} steht neben dir, als die Lichter von Calvi auftauchen, und keiner "
                       "von euch muss etwas sagen.",
    ("person", "posten"): "Du nimmst den Posten an Land. {name} weiß es, bevor du es sagst – und kommt trotzdem mit "
                          "zum Bahnhof. Was daraus wird, entscheidet ihr nicht heute.",
    ("person", "offen"): "Du weißt noch nicht, wohin. {name} sagt, das sei die erste ehrliche Antwort dieser Woche.",
    ("allein", "see"): "Du bleibst auf See. Am letzten Abend stehst du allein an der Reling, und es ist in Ordnung so.",
    ("allein", "posten"): "Du nimmst den Posten an Land. Ein Büro, ein Titel, kein Meer. Du packst deine Seekiste "
                          "allein.",
    ("allein", "offen"): "Du hast keine Antwort gegeben – nicht der Zentrale, nicht dir selbst. Das Angebot wartet "
                         "noch ein paar Tage.",
    ("offen", "see"): "Du sagst, du bleibst – vorerst. Ob das eine Antwort ist, weißt du selbst nicht.",
    ("offen", "posten"): "Du sagst zu und zweifelst im selben Atemzug. Die Frage nach Frankfurt bleibt.",
    ("offen", "offen"): "Du lässt es offen. Calvi ist erst der Anfang einer anderen Frage.",
}
FRAU = {
    "chiara": {"partner": "Chiara rückt deinen Kragen gerade, bevor ihr von Bord geht. „Ordentlich“, sagt sie. Dann "
                          "lässt sie die Hand liegen.",
               "hoch": "Chiara übergibt dir die Liste für die Werft und hat einen Punkt für dich dazugeschrieben: "
                       "„Danke.“ Mehr schreibt sie nie.",
               "mitte": "Chiara nickt dir zu, als ihr festmacht. Zwischen euch ist mehr Respekt als vor einer Woche.",
               "tief": "Chiara verabschiedet dich korrekt. Mehr nicht."},
    "sophia": {"partner": "Sophia schenkt dir das erste Kapitel. Du bist darin – nicht unter deinem Namen, aber sie "
                          "hat dich gut getroffen.",
               "hoch": "Sophia sagt, sie schreibe jetzt doch das Buch. Über ein Schiff, das nicht weiterkam. Sie "
                       "fragt, ob du es lesen willst.",
               "mitte": "Sophia winkt vom Kai. Ihr Notizbuch ist voller als vor einer Woche.",
               "tief": "Sophia ist schon weg, bevor du dich verabschieden kannst."},
    "lea": {"partner": "Lea zieht dich zur Badeplattform, ein letztes Mal ins Wasser, bevor Calvi alles wieder "
                       "normal macht. „Nur fünf Minuten“, sagt sie. Es werden mehr.",
            "hoch": "Lea drückt dir ihre Taucheruhr in die Hand. „Bis zur nächsten Saison. Dann holst du sie ab.“",
            "mitte": "Lea grinst dir zu, als die Leinen fest sind. „Nächstes Mal ohne Drama, ja?“",
            "tief": "Lea hat Kopfhörer auf, als ihr festmacht."},
    "rosi": {"partner": "Rosi hat Öl an den Händen und wischt sie an deinem Hemd ab. Mit Absicht. „Jetzt gehörst du "
                        "zum Maschinenraum.“",
             "hoch": "Rosi schreibt deinen Namen mit Kreide neben ihren auf den Umrichter. „Damit die Werft weiß, wen "
                     "sie fragen muss.“",
             "mitte": "Rosi hebt den Daumen aus dem Maschinenraum. Das ist bei ihr eine lange Rede.",
             "tief": "Rosi ist mit der Werft beschäftigt. Sie hat keine Zeit für Abschiede."},
    "siri": {"partner": "Siri postet nichts von diesem Abend. Zum ersten Mal ist ein Moment nur für sie – und für "
                        "dich.",
             "hoch": "Siri löscht den Clip von der Party. „Das war nicht ich“, sagt sie. Dann fragt sie nach deiner "
                     "Nummer.",
             "mitte": "Siri macht ein letztes Foto von der Crew. Du bist drauf, und sie schneidet dich nicht raus.",
             "tief": "Siri ist mit Yasin beim ersten Taxi. Sie dreht sich nicht um."},
}
