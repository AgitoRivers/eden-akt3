# -*- coding: utf-8 -*-
"""Icon-Woerterbuch der Oberflaeche (Duc 30.10.2026, docs/wiki/systeme/ui_stil.md): ein Begriff, ein Icon.

Baut aus den Phosphor-Icons (Duotone, MIT) den Sprite client/plugins/eden-ui/icons.svg. Neues Icon: Zeile in ICONS ergaenzen,
Skript laufen lassen, im Spiel per EdenUI.icon("name") nutzen. Die SVGs kommen in fester Version vom npm-Paket.

  python werkzeuge\\ui_icons.py
"""
import os
import re
import urllib.request

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZIEL = os.path.join(EDEN, "client", "plugins", "eden-ui")
VERSION = "2.1.1"
QUELLE = "https://cdn.jsdelivr.net/npm/@phosphor-icons/core@%s/" % VERSION

# Begriff im Spiel -> Phosphor-Name. Jeder Begriff steht nur einmal hier; "energy" ist nur Ducs Energie, Strom ist "power".
ICONS = {
    "mood-buzzing": "smiley-wink",
    "mood-good": "smiley",
    "mood-calm": "smiley-meh",
    "mood-tense": "smiley-nervous",
    "mood-mutinous": "smiley-angry",
    "reputation": "star",
    "wind": "arrow-right",
    "energy": "lightning",
    "power": "plug",
    "diesel": "gas-pump",
    "money": "coins",
    "deadline": "hourglass-medium",
    "phone": "phone",
    "investigate": "magnifying-glass",
    "backpack": "backpack",
    "locked": "lock",
    "done": "check-circle",
    "failed": "x-circle",
    "talk": "chat-circle-dots",
    "love": "heart",
    "map": "map-trifold",
    "character": "user",
    "journal": "notebook",
    "codex": "book-open",
    "menu": "list",
    "dice": "dice-five",
    "place": "map-pin",
    "declined": "minus-circle",
    "expand": "caret-down",
    "collapse": "caret-up",
    "gag": "mask-happy",
    "gestures": "hand-heart",
    "send": "paper-plane-right",
    "voice-on": "speaker-high",
    "voice-off": "speaker-slash",
    "collapse-side": "caret-right",
    "ideas": "lightbulb",
    "close": "x",
    "back": "caret-left",
    "time": "clock",
    "confront": "scales",
    "secure": "push-pin",
    "order": "megaphone",
    "compare": "puzzle-piece",
    "memory": "brain",
    "trade": "handshake",
    "date": "sun-horizon",
    "desire": "fire",
    "special": "diamond",
    "quality": "star-four",
    "dislike": "heart-break",
    "chest": "treasure-chest",
    "gear": "t-shirt",
    "bunk": "bed",
    "training": "boxing-glove",
    "photo": "camera",
    "tender": "sailboat",
    "calendar": "calendar-dots",
    "strength": "hand-fist",
    "charm": "sparkle",
    "empathy": "heart-half",
    "perception": "eye",
    "cunning": "spade",
    "courage": "shield-star",
    "animal": "paw-print",
    "animal-chicken": "bird",
    "animal-pig": "piggy-bank",
    "animal-cow": "cow",
    "female": "gender-female",
    "male": "gender-male",
    "timber": "tree",
    "slate": "stack",
    "granite": "mountains",
    "steel": "link",
    "iron": "wrench",
    "cork": "wine",
    "feather": "feather",
    "leaf": "leaf",
    "cart": "shopping-cart",
    "axe": "axe",
    "pick": "hammer",
    "fish": "fish",
    "bite": "waves",
    "snap": "scissors",
    "letgo": "arrow-u-up-left",
    "package": "package",
    "water": "drop",
    "burn": "flame",
    "earth": "plant",
    "air": "wind",
    "shock": "lightning-slash",
    "bleed": "drop-half",
    "dazed": "spiral",
    "exhausted": "battery-empty",
    "mud": "drop-half-bottom",
    "blinded": "eye-slash",
    "weakened": "trend-down",
    "exposed": "shield-slash",
    "stunned": "smiley-x-eyes",
    "silenced": "microphone-slash",
    "guard": "shield",
    "wall": "wall",
    "dodge": "person-simple-run",
    "skip": "pause",
    "stamina": "battery-charging",
    "hp": "heartbeat",
    "warning": "warning",
    "target": "crosshair",
    "partial": "circle-half",
    "sprint": "sneaker-move",
    "fight": "sword",
    "campfire": "campfire",
    "travel": "flag",
    "onfoot": "boot",
    "rule": "scroll",
    "gift": "gift",
    "listen": "ear",
    "music": "music-notes",
    "cooking": "cooking-pot",
    "cloth": "dress",
    "wool": "cloud",
    "leather": "pants",
    "coral": "flower",
}


def laden(pfad):
    with urllib.request.urlopen(QUELLE + pfad, timeout=30) as antwort:
        return antwort.read().decode("utf-8")


def bauen():
    os.makedirs(ZIEL, exist_ok=True)
    teile = ['<svg xmlns="http://www.w3.org/2000/svg">',
             "<!-- Phosphor Icons %s (MIT, siehe LICENSE-phosphor.txt). Erzeugt von werkzeuge/ui_icons.py, nicht von Hand aendern. -->" % VERSION]
    for begriff, name in sorted(ICONS.items()):
        svg = laden("assets/duotone/%s-duotone.svg" % name)
        innen = re.fullmatch(r"\s*<svg[^>]*>(.*)</svg>\s*", svg, re.S)
        if not innen or "<path" not in innen.group(1):
            raise SystemExit("Unerwartetes SVG: " + name)
        teile.append('<symbol id="%s" viewBox="0 0 256 256" fill="currentColor">%s</symbol>' % (begriff, innen.group(1)))
    teile.append("</svg>\n")
    with open(os.path.join(ZIEL, "icons.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(teile))
    with open(os.path.join(ZIEL, "LICENSE-phosphor.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(laden("LICENSE"))
    print("%d Icons, %d Byte" % (len(ICONS), os.path.getsize(os.path.join(ZIEL, "icons.svg"))))


if __name__ == "__main__":
    bauen()
