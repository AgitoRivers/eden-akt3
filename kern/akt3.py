# -*- coding: utf-8 -*-
"""Akt 3, kleine Morgen-Vignetten ohne Phase (Drehbuch docs/wiki/welt/drehbuch_akt3.md, Abschnitt 3 und 4.1).

Am Ende jeder Nacht (eden.py, Tagesende) kommen hoechstens drei Zeilen in die Meldung "Day X is over":
  * Kevin auf dem Kirchendach (Tag 25-34, ausser Tag 26: da sitzt er auf Casanovas Tafel). Damit niemand Minicu vergisst.
  * Dank eines Hauses, das nicht abgebrannt ist (Tag 25-28, je Morgen eins). Ohne Frage, gefragt wird spaeter.
  * Die Legion baut einen Tag mit (bl_verband_wolff): einmal eine Stufe an der begonnenen Baustelle, die am weitesten ist.
Alles nur nach dem Cliffhanger (akt2_ende)."""
from . import aufbau

KEVIN = "Kevin is on the church roof again, above the back room. He hasn't moved."
DANK = {
    "post": "Mina rides past on her bicycle and honks twice. The post office came through the fire. She waves a letter at you: “Not a bill!”",
    "batu": "There is a tin of biscuits on the step of Bà Tư's shop, with your name on it. Her shop came through the fire.",
    "bar": "Alva has written one word on Papa's board, under all the names: OPEN. Her bar came through the fire.",
    "werkstatt": "Petru's rudder still hangs over his workshop door, not burned. He nods at you once when you walk past.",
}
LEGION = "Wolff and two men of the Legion carried beams all day. Wolff: “You gave me the good bandage, the only one. The Legion pays its debts.”"


def morgen(z):
    """Zeilen fuer den neuen Morgen (z["tag"] ist schon der neue Tag)."""
    f = z.get("flags", [])
    if "akt2_ende" not in f or not 25 <= z.get("tag", 0) <= 35:
        return []
    tag, zeilen = z["tag"], []
    if tag <= 34 and tag != 26:
        zeilen.append(KEVIN)
    if tag <= 28:
        heil = [h for h in aufbau.ORTE if "tk_haus_weg_" + h not in f and "a3_dank_heil_" + h not in f]
        if heil:
            f.append("a3_dank_heil_" + heil[0])
            zeilen.append(DANK[heil[0]])
    if "bl_verband_wolff" in f and "a3_legion" not in f:
        st = aufbau.baustellen(z)
        offen = [(s["stufe"], h) for h, s in st.items() if s["begonnen"] and s["stufe"] < len(aufbau.STUFEN[h])]
        if offen:
            f.append("a3_legion")
            zeilen.append(LEGION)
            zeilen += aufbau.stufe_geschenkt(z, max(offen)[1])
    return zeilen


# ------------------------------------------------------------------ Die vier Saeulen und das Ende (Drehbuch Abschnitt 8, enden.md)
# Vorschlag der Cloud-Sitzung; der Feinschliff der Enden ist Ducs (enden.md). Listen wie in ereignisse_akt3_woche5.py.
ZEUGEN = ["petru", "mina", "batu", "alva", "anghjulu", "casanova", "sandru", "bonaventure"]
BEWEISE = ["alon_kiste_genutzt", "a3_siri_post", "sophia_notizen", "bl_funk_white", "bl_funk_charly", "bl_wache_gesehen",
           "rt_ausgang_alle", "mo_ark_beweis", "a3_beweis_feuer", "a3_mast_an"]
ENDEN = {"0": "Too Late", "1": "The Deal", "2a": "Broke, but Free", "2b": "The Village Holds Together",
         "2c": "Alon in Handcuffs", "2.5a": "On Credit", "2.5b": "Saved, but Not Ours", "2.5c": "He'll Be Back",
         "3": "Rewritten", "stern": "The Long Game"}

# Entwuerfe der Schlusskarte (Duc 04.11.2026: Entwurf hier, Feinschliff Duc, enden.md). Je Ende: das letzte Bild, Buenaventura, Pascal.
ENDE_TEXT = {
    "0": ("Diggers on the beach. They start with Lola's hut. Kevin sits on the first digger and doesn't move.",
          "Buenaventura works for the hotel now: Pirate Experience, plastic parrot, “Arrr!” for tips.",
          "Pascal reads out the eviction letters on the piazza. He calls everyone by their first name."),
    "1": ("The festa happens under an A.V. banner. Alon raises a glass from a hologram. Rosi doesn't say a word all night. The church roof still leaks.",
          "Buenaventura works for the hotel now: Pirate Experience, plastic parrot, “Arrr!” for tips.",
          "Alon thanks his partner on the ground, under the wrong name. Pascal raises his glass to him anyway."),
    "2a": ("The Eden Group falls apart live on every phone. The village argues. The festa is half empty. Rosi buys back the workshop in Catania.",
           "Buenaventura runs his Eco Tours, a hat made from a feeding bucket on his head.",
           "Pascal stands in a queue of creditors in Monaco, a number in his hand."),
    "2b": ("The most beautiful festa the bay has seen. At midnight, a red light blinks once in the mountains.",
           "Buenaventura runs his Eco Tours, a hat made from a feeding bucket on his head.",
           "Nonna's seedlings bloom on the festa table. Nobody says who sent them."),
    "2c": ("Elsa leads Alon away in handcuffs. Above the bay, a new helicopter is already coming: the next buyer.",
           "Buenaventura runs his Eco Tours, a hat made from a feeding bucket on his head.",
           "Pascal climbs out of the helicopter, with the next buyer's folder under his arm."),
    "2.5a": ("The village owns the bay now, and it owes everyone. Petru sells his green boat to pay the first bill.",
             "Buenaventura runs his Eco Tours, a hat made from a feeding bucket on his head.",
             "The cooperative keeps its books in Pascal's old ledger, because his numbers were right."),
    "2.5b": ("The bay is a nature park now, owned by a foundation in Paris. Petru stands outside a fence.",
             "Buenaventura runs his Eco Tours, with a badge from the foundation.",
             "Pascal says good morning to Petru at the fence. He wears the foundation's badge around his neck."),
    "2.5c": ("A quiet morning after the festa. Then your phone rings. A calm voice: “Round two, Officer.”",
             "Buenaventura runs his Eco Tours, a hat made from a feeding bucket on his head.",
             "In the background of the call, a careful voice says: “Leave it with me.”"),
    "3": ("The cooperative signs at Lola's beach bar. Every name goes into a knot of Petru's net. Rosi buys back the workshop in Catania.",
          "Buenaventura runs his Eco Tours, a hat made from a feeding bucket on his head.",
          "Pascal's name is missing from the net. Don ties an empty knot for him, without a word."),
    "stern": ("The whole village stands at the foot of the villa. Madame Casanova walks into her parents' house for the first time in years.",
              "Buenaventura runs his Eco Tours, a hat made from a feeding bucket on his head.",
              "Casanova says his full name in front of Alon: Pascal Leca. Alon asks: “Who?”"),
}
FEHLT = {"wahrheit": "Nobody believed what you saw. Without proof, Alon's story stayed the true one.",
         "geld": "There was no money to protect the bay.", "gemeinschaft": "Too few people dared to say their names.",
         "staerke": "Alon walked away. Nobody stopped him."}


def zeugen(z):
    return [p for p in ZEUGEN if "a3_zeuge_" + p in z.get("flags", [])]


def beweise(z):
    return [b for b in BEWEISE if b in z.get("flags", [])]


def saeulen(z):
    """-> dict Saeule -> bool. Wahrheit: 3 Beweise oder 2 mit Kassenbuch 'alles'. Geld: ein Weg (Margot, Yamamoto 5,
    Megans Wende). Gemeinschaft: 5 Zeugen oder 4 mit Kassenbuch 'teil' (Ruf ab 5 zaehlt wie ein Zeuge). Staerke: Endkampf
    gewonnen oder Festnahme."""
    f, w = z.get("flags", []), z.get("werte", {})
    nb, nz = len(beweise(z)), len(zeugen(z)) + (1 if w.get("ruf", 0) >= 5 else 0)
    return {
        "wahrheit": nb >= 3 or (nb >= 2 and "a3_kassenbuch_alles" in f)
                    or "a3_kom_runden_2" in f or "a3_kom_runden_3" in f,          # Kommission als Verhandlung: 2 von 3 Runden
        "geld": "margot_geborgen" in f or w.get("vertrauen.yamamoto", 0) >= 5 or "a3_megan_wende" in f,
        "gemeinschaft": nz >= 5 or (nz >= 4 and "a3_kassenbuch_teil" in f),
        "staerke": "a3_alon_besiegt" in f or "a3_alon_festgenommen" in f,
    }


def ende(z):
    """-> Kennung aus ENDEN. Ohne Wahrheit traegt keine Saeule (Vorschlag, Fragenliste F-35)."""
    if "a3_stern" in z.get("flags", []):
        return "stern"
    if "a3_deal" in z.get("flags", []):
        return "1"
    s = saeulen(z)
    n = sum(s.values())
    if n == 4:
        return "3"
    if n == 3:
        return "2.5a" if not s["geld"] else "2.5b" if not s["gemeinschaft"] else "2.5c" if not s["staerke"] else "0"
    if n == 2 and s["wahrheit"]:
        return "2a" if s["geld"] else "2b" if s["gemeinschaft"] else "2c"
    return "0"


# ------------------------------------------------------------------ Lose beim Besuch (Umbau nach dem Review, 04.11.2026)
# Wo Duc ohnehin hingeht, ohne Phase: Petrus Werkstatt, Alvas Bar, Angeln, Kochen, Nonnas Laden. Kommt ein offenes Los dieser
# Person, oeffnet es sich als Frame ohne Ausflug (eden.py: laden_besuch, angeln_ende, kochen_baukasten, nonna_verlassen).
BESUCH = {"petru": ["tafel"], "alva": ["getraenk"], "angeln": ["fang"], "kochen": ["topf", "menue"], "nonna": ["garten"]}


SZENEN_BESUCH = {"petru": [("a3_petru_netz", 25)]}   # Petrus Netz beim Werkstattbesuch (ereignisse_akt3_petru.py)


def szene_besuch(z, wo):
    """-> Frame einer kleinen Szene beim Besuch (ohne Phase), wenn kein Los kommt, oder None."""
    if z.get("status") != "wahl" or "akt2_ende" not in z.get("flags", []):
        return None
    for eid, ab in SZENEN_BESUCH.get(wo, []):
        if z.get("tag", 0) >= ab and eid not in z.get("flags", []):
            return eid
    return None


def los_besuch(z, moddir, wo):
    """-> Frame-ID eines offenen Loses fuer diesen Besuch, oder None. Bedingungen wie an der Tafel (auftraege.json)."""
    if z.get("status") != "wahl" or "akt2_ende" not in z.get("flags", []) or wo not in BESUCH:
        return None
    from . import auftraege, regeln
    start = ((auftraege.daten(moddir) or {}).get("orte", {}).get("a3_lose") or {}).get("start", [])
    wenn = {s["id"]: s.get("wenn") for s in start}
    for lid in BESUCH[wo]:
        eid = "a3_los_" + lid
        if eid in wenn and regeln.gilt(wenn[eid], z):
            return eid
    return None
