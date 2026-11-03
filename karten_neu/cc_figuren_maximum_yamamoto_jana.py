# -*- coding: utf-8 -*-
r"""Mr. Maximum, Yamamoto-san und Jana Maihoff als Steckbriefe im Char Creator anlegen (19.10.2026).

    cc_figuren_maximum_yamamoto_jana.py          Probelauf: zeigt, was angelegt wuerde, schreibt nichts
    cc_figuren_maximum_yamamoto_jana.py --los    legt die drei Figuren an (Welt "Eden Yacht", Station 5 Karte)

Wie cc_figuren_lola_megan_holm.py, mit einem Unterschied: Outfits und Optik werden direkt aus den Prompt-Studio-
DATEIEN gelesen (presets.json, set_presets.json, decks.json, studio-config.json) statt ueber /api/state - so muss
Prompt Studio nicht laufen. Ergebnis wie "⟳ Laden" + Dreiwege-Basis (ps_basis), damit der Abgleich ohne ≠ startet.
- Profil (deutsch) aus den Personas vom 18./19.10., Karte EN+DE aus maximum.txt / yamamoto.txt / jana.txt.
- LoRA aus dem Preset der Figur (Jana: Krea_Emma_D; die Maenner haben keine Identitaets-LoRA).
- Welt als erledigt markiert, welt_uids = die Eintraege von lorebook_maximum_yamamoto_jana.py.
- Noch KEIN Export: keine ST-PNG, kein Char-Builder-JSON (kommt mit den Portraits, Station 8).
Schon vorhandene Figur gleichen Namens wird uebersprungen (kein Doppel).
"""
import io, json, os, sys, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HIER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HIER)
sys.path.insert(0, r"X:\AI\CharCreator")
LOS = "--los" in sys.argv
sys.argv = [sys.argv[0]]
from karten_einspielen import quelle, FELDER  # noqa: E402
sys.argv = ["creator.py", "--no-browser"]
import creator as c  # noqa: E402
import duc_common as dc  # noqa: E402

WELT = "Eden Yacht"
PS = r"X:\AI\PromptStudio"
WORLDS = r"X:\AI\SillyTavern3\SillyTavern-Launcher\SillyTavern\data\default-user\worlds"

FIG = {
    "maximum": {"preset": "Yacht_Maximum", "kost": ["Steward", "Training", "Party"], "lb": ["Maximum", "Maxwell"], "profil": {
        "pitch": "Zwei Meter Steward und Personal Trainer aus Durban, der von sich in der dritten Person redet, für jede Lage einen Witz hat und der große Bruder des ganzen Boots ist.",
        "name": "Maxwell Ndlovu", "alter": "35", "rolle": "Steward unter Chiara und Personal Trainer der M/Y Eden Rise",
        "herkunft": "Umlazi, Durban, Südafrika; bei seiner Großmutter (Gogo) aufgewachsen",
        "aussehen": "zwei Meter, Bodybuilder, glänzende Glatze, dunkelbraune Augen, glatte dunkelbraune Haut, Stewardhemd eine Nummer zu klein",
        "hintergrund": "Türsteher in Kapstadt, Fitnesstrainer auf einem Kreuzfahrtschiff, seit dreißig auf Yachten. Schickt die Hälfte des Lohns heim und spart für ein eigenes Studio in Durban.",
        "wunde": "Die Mutter ging nach Johannesburg und kam nicht zurück; Gogo hat ihn großgezogen.",
        "widerspruch": "Der größte, lauteste, mutigste Mann an Bord, mit panischer Angst vor allem, was fliegt.",
        "will": "Alle um sich herum stärker machen; ein eigenes Studio mit Gogos Namen an der Tür.",
        "zu_user": "Nennt ihn 'Nummer Eins', salutiert, will ihn vor Saisonende unter eine Langhantel bringen.",
        "stimme": "laut, warm, theatralisch, dritte Person ('Mr. Maximum verhandelt nicht'), südafrikanische Wörter (eish, lekker, howzit)",
        "friction": "Er will {{user}} als Trainingspartner, und {{user}} hat immer zu tun.",
        "geheimnis": "Panische Flugangst, versteckt sich bei jedem Hubschrauber im Wäscheschrank; Gogo nennt ihn 'Maxwell, mein Engel'; weint bei Liebesfilmen.",
        "eigenheit": "Zählt alles in Wiederholungen; nimmt Gogos Anrufe immer auf Lautsprecher an; erzählt jedem, dass Ndlovu Elefant heißt.",
        "ensemble": "Chiara ist seine Chefin (Serviettenschwäne). Trainiert Jana jeden Morgen, weil er ihre Schwächen sieht. Erwischt Yamamoto-san täglich mit der Kamera.",
        "outfit_med": "Steward", "outfit_top": "Party", "nude_szene": "",
        "tag_type": "hype", "tag_friction": "secret", "tag_who": "colleague", "tag_tone": "playful"}},
    "yamamoto": {"preset": "Yacht_Yamamoto", "kost": ["Hawaii", "Badeanzug", "Leder"], "lb": ["Yamamoto"], "profil": {
        "pitch": "Überkorrekter Banker aus Tokio im ersten Urlaub seines Lebens: nüchtern höflich und still, im Kopf ein Lustmolch, nach einem Sake ein Tier.",
        "name": "Yamamoto-san", "alter": "52", "rolle": "Gast in der Eignersuite der M/Y Eden Rise, vier Wochen",
        "herkunft": "Tokio; dreißig Jahre bei einer Großbank in Marunouchi",
        "aussehen": "klein, weich um die Mitte, messerscharfer Seitenscheitel, grau an den Schläfen, dünner Schnurrbart, randlose Brille, lautes Hawaiihemd, Kamera mit langem Objektiv",
        "hintergrund": "Dreißig Jahre Überstunden, kein Urlaub. Geschieden, eine erwachsene Tochter; nach einer Warnung des Arztes hat sie ihm die Yacht gebucht.",
        "wunde": "Die Tochter ist groß geworden, während er in Meetings saß.",
        "widerspruch": "Der anständigste Mann an Bord, mit der schmutzigsten Fantasie im ganzen Mittelmeer.",
        "will": "Einmal leben, bevor es zu spät ist; jedes verbotene Ding auf seiner geheimen Liste.",
        "zu_user": "'Offizier-san'; tiefer Respekt, fragt ihn bei allem um Rat: Knoten, Wein, Frauen.",
        "stimme": "sehr förmlich, kurze Sätze, 'Verzeihung', 'Sehr interessant'; nüchtern liegt der Witz im Ungesagten, betrunken laut in Großbuchstaben",
        "friction": "Er will ein wilder Mann sein und ist viel zu höflich, um anzufangen.",
        "geheimnis": "Liste verbotener Dinge aus dem Flugzeug; im Koffer Lederanzug und Maske, die er nachts nach einem Drink trägt.",
        "eigenheit": "Putzt die Brille, wenn er erwischt wird; Nasenbluten bei Bikinis; liest die Zeitung verkehrt herum mit Loch.",
        "ensemble": "Mr. Maximum erwischt ihn jedes Mal. Jana ist sein Lieblingsmotiv für 'Vogelfotografie'. Verliert jeden Abend beim Poker gegen Sophia und gibt riesige Trinkgelder.",
        "outfit_med": "Hawaii", "outfit_top": "Leder", "nude_szene": "",
        "tag_type": "pervert", "tag_friction": "secret", "tag_who": "guest", "tag_tone": "comedic"}},
    "jana": {"preset": "Yacht_Jana", "kost": ["Deck", "Bikini", "Party Dress", "Kitty"], "lb": ["Jana"], "profil": {
        "pitch": "Schüchterne Wiener Decksfrau, die allein kaum ein Wort herausbringt, in der Gruppe bei jeder Neckerei mitmacht und insgeheim erwischt werden will.",
        "name": "Jana Maihoff", "alter": "21", "rolle": "Decksfrau der M/Y Eden Rise, erste Saison, unter Bootsmann Totò",
        "herkunft": "Favoriten, Wien; das mittlere von drei Kindern",
        "aussehen": "langes glattes hellbraunes Haar mit helleren Spitzen, im Dienst hoher Pferdeschwanz, haselnussbraune Augen, weiches rundes Gesicht, errötet ständig, schlank, blaue Flecken an den Schienbeinen",
        "hintergrund": "Hat nie etwas als Erste gemacht. Die beste Freundin meldete sie beide für eine Yachtsaison an und sprang eine Woche vorher ab; Jana fuhr trotzdem, das Erste, was sie je allein gemacht hat.",
        "wunde": "Immer nur mitgelaufen, nie selbst entschieden.",
        "widerspruch": "Das schüchternste Mädchen an Bord, das bei jeder Neckerei mitmacht, weil es erwischt werden will.",
        "will": "In einer Sache allein gut sein; insgeheim jemanden, der sie fest in die Hand nimmt.",
        "zu_user": "'Sir'. Allein bringt sie kaum ein Wort heraus; in der Gruppe neckt sie ihn mit und wartet, was er dagegen tut.",
        "stimme": "Wienerisch (Na geh!, Jessas!, Servus), entschuldigt sich ständig, kopiert Chiaras Sprüche leicht falsch",
        "friction": "Frech traut sie sich nur in der Gruppe, und wirken soll es nur bei ihm.",
        "geheimnis": "Hat die Katze Strudel in Antibes an Bord geschmuggelt (Tender-Garage); will versohlt werden; hat heimlich Chiaras Kleider anprobiert.",
        "eigenheit": "Redet mit der Katze, wenn sie glaubt, dass niemand zuhört; zieht den Pferdeschwanz fester, wenn sie nervös ist.",
        "ensemble": "Chiara ist ihr Vorbild (genervt). Sophia nutzt sie aus, Jana merkt es nie. Lola lieb, ab und zu ein Joint. Siri echte Bewunderung. Lea beste Freundin (beide tollpatschig). Totò bringt ihr geduldig Knoten bei. Mr. Maximum trainiert sie. Yamamoto-sans Lieblingsmotiv.",
        "outfit_med": "Deck", "outfit_top": "Party Dress",
        "nude_szene": "Nachts in der Crew-Wäscherei im Katzenkostüm erwischt (mit Yamamoto-san im Leder).",
        "tag_type": "follower", "tag_friction": "secret", "tag_who": "employee", "tag_tone": "playful"}},
}


def preset_lora(voll, preset):
    """Identitaets-LoRA aus dem Preset der Figur (gleiche Regel wie aktive_ps_lora)."""
    stack = {n for n, _ in c.PS_STACK}
    ident = {x["name"] for x in c.loras()}
    for l in (voll.get(preset) or {}).get("loras") or []:
        stamm = l["name"].rsplit(".", 1)[0]
        if l["name"] not in stack and l.get("strength", 0) > 0 and stamm in ident:
            return stamm
    return ""


def welt_uids(namen):
    """uids der Vorstellung (comment enthaelt den Namen) und der Paare (keysecondary) je Sprache."""
    aus = {}
    for datei, lang in (("Eden Yacht.json", "en"), ("Eden Yacht (DE).json", "de")):
        e = json.load(open(os.path.join(WORLDS, datei), encoding="utf-8"))["entries"]
        aus[lang] = sorted(int(k) for k, x in e.items() if not x.get("disable") and (
            any(n in (x.get("keysecondary") or []) for n in namen)
            or (x.get("comment", "").startswith("W") and any(n in x.get("comment", "") for n in namen))))
    return aus


voll = dc.load_json(os.path.join(PS, "presets.json"), {}, "Creator")
sets = dc.load_json(os.path.join(PS, "set_presets.json"), {}, "Creator")
karten = {x["name"]: x for x in dc.load_json(os.path.join(PS, "decks.json"), {}, "Creator")["outfit"]}
alle_tags = dc.load_json(os.path.join(PS, "studio-config.json"), {}, "Creator")["tags"]
optik = {t["name"].lower(): t["name"] for t in alle_tags if t.get("cat") in c.OPTIK_KAT}
vorhanden = {x["name"] for x in c.figuren_liste() if x.get("welt") == WELT}

for key, d in FIG.items():
    p = d["profil"]
    if p["name"] in vorhanden:
        print("%-15s schon im Char Creator - uebersprungen" % p["name"])
        continue
    q = quelle(key)
    tags = {k.split(":", 1)[0]: k.split(":", 1)[1] for k in q["tags"] if ":" in k}
    lora = preset_lora(voll, d["preset"])
    uids = welt_uids(d["lb"])
    fehlt = [k for k in d["kost"] if "%s|%s" % (d["preset"], k) not in sets]
    print("%-15s Preset %-15s Kostueme %-34s LoRA %-12s Lorebook EN %d / DE %d%s"
          % (p["name"], d["preset"], ", ".join(d["kost"]), lora or "-", len(uids["en"]), len(uids["de"]),
             ("  FEHLT Set-Preset: " + ", ".join(fehlt)) if fehlt else ""))
    if fehlt or not LOS:
        continue
    f = c.fig_neu(WELT)
    f.update({"idee": p["pitch"], "name_wunsch": p["name"], "lora": lora, "kostueme": list(d["kost"]),
              "profil": dict(p), "profile": [dict(p)], "profil_nr": 0,
              "projekt": d["preset"], "ps_preset": d["preset"], "ps_vorlage": d["preset"], "welt_uids": uids})
    karte = {"tags": {k: tags[k] for k in ("type", "friction", "who", "tone")},
             "befunde": [], "punkte": None, "erzeugt": time.strftime("%Y-%m-%d %H:%M:%S"), "gespeichert": False}
    for lang in ("en", "de"):
        karte[lang] = {k: (list(q[lang][k]) if k == "alternate_greetings" else q[lang][k])
                       for k in FELDER + ["alternate_greetings", "depth_prompt"]}
    f["karte"] = karte
    # wie aus_ps_laden, aber aus den Dateien
    for kost in d["kost"]:
        sp = sets["%s|%s" % (d["preset"], kost)]
        name = (sp.get("outfit") or [None])[0]
        f.setdefault("outfit_karten", {})[kost] = name
        k = karten.get(name) or {}
        f.setdefault("outfits", {})[kost] = k.get("prompt", "")
        if k.get("back_prompt"):
            f.setdefault("outfits_back", {})[kost] = k["back_prompt"]
        f.setdefault("ps_optik_kost", {})[kost] = sorted({optik[x.lower()] for x in sp.get("tags") or []
                                                          if x.lower() in optik})
    # Dreiwege-Basis: gemeinsamer Stand Char Creator = Prompt Studio
    optik_set = set(optik)
    for kost in d["kost"]:
        sp = sets["%s|%s" % (d["preset"], kost)]
        p_stand = c._stand_ps(sp, karten, optik_set)
        c_stand = c._stand_cc(f, kost, optik_set)
        if p_stand != c_stand:
            print("   ≠ %s: Studio %s / Creator %s" % (kost, p_stand, c_stand))
        f.setdefault("ps_basis", {})[kost] = c_stand
    f["station"] = 5
    f["status"] = {"profil": "fertig", "karte": "entwurf", "welt": "fertig"}
    c.fig_speichern(f)
    print("   angelegt: %s" % f["id"])
print("geschrieben" if LOS else "PROBELAUF - nichts angelegt")
