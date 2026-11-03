# -*- coding: utf-8 -*-
r"""Eden cookbook (21.10.2026): every combination of 2 or 3 DIFFERENT ingredients is a concrete dish.
Breaking the golden rule (1 ingredient, a duplicate, more than 3) gives brown slime.

    python kochbuch.py          writes kochbuch.csv and kochbuch.html next to this script and prints a summary

Ingredients have a role that decides the dish name:
  base   (Basis: Mehl, Reis, Nudeln, Kartoffeln, Kohl)        -> the dish form ("Pasta", "Reispfanne" ...)
  main   (Haupt: meat, fish, seafood, eggs, mushrooms ...)     -> what the dish is "mit"
  accent (Akzent: sauces, herbs, chili, honey, sepia ...)      -> the finish ("in Tomatensoße", "mit Chili")
Favourite recipes (one per person) override the generated name. Effects add up; quality stars are applied in game.
"""
import csv, html, itertools, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))

# id: (label, role, source, effect, numbers for the name: noun / dative after "mit" / stem for compounds)
INGREDIENTS = {
    # bought
    "mehl": ("Mehl", "base", "kaufen: Nonna, Alva", "heilt 3 LP", {"noun": "Pfannkuchen", "stem": "Teig"}),
    "reis": ("Reis", "base", "kaufen: Nonna, Alva", "+1 Ausdauer im ersten Kampf", {"noun": "Reispfanne", "stem": "Reis"}),
    "nudeln": ("Nudeln", "base", "kaufen: Nonna, Alva", "Moral +1", {"noun": "Pasta", "stem": "Nudel"}),
    "kartoffeln": ("Kartoffeln", "base", "kaufen: Nonna, Alva", "Max-LP +3", {"noun": "Kartoffelgratin", "stem": "Kartoffel"}),
    "tomaten": ("Tomaten", "accent", "kaufen: Nonna, Alva", "+1 Vertrauen bei allen am Tisch",
                {"post": "in Tomatensoße", "mit": "Tomaten", "stem": "Tomaten"}),
    "eier": ("Eier", "main", "kaufen: Nonna", "Schutz +1 im ersten Kampf", {"noun": "Rührei", "dat": "Ei", "stem": "Ei"}),
    "milch": ("Milch", "accent", "kaufen: Nonna", "Zustände 1 Runde kürzer",
              {"post": "in Rahmsoße", "mit": "Rahm", "stem": "Rahm"}),
    "sojasauce": ("Sojasauce", "accent", "kaufen: Totò", "Preise −10 %",
                  {"post": "mit Sojaglasur", "mit": "Soja", "stem": "Soja"}),
    "fischsauce": ("Fischsauce", "accent", "kaufen: Totò", "List +1",
                   {"post": "nach Saigoner Art", "mit": "Fischsauce", "stem": "Fischsaucen"}),
    "dashi": ("Dashi", "accent", "kaufen: Totò", "Empathie +1",
              {"post": "in Dashi-Brühe", "mit": "Dashi", "stem": "Dashi"}),
    # grown at Nonna's
    "kohl": ("Kohl", "base", "anbauen: Nonna (1 Tag)", "Charisma +1", {"noun": "Kohlroulade", "stem": "Kohl"}),
    "wildkraeuter": ("Wildkräuter", "accent", "anbauen: Nonna · sammeln: Macchia", "Erfahrung +10 %",
                     {"post": "mit Kräutern der Macchia", "mit": "Kräutern", "stem": "Kräuter"}),
    "chilis": ("Chilis", "accent", "anbauen: Nonna (1 Tag)", "Krit +5 %",
               {"post": "mit Chili", "mit": "Chili", "stem": "Chili"}),
    # Nonna's animals (investments)
    "wachteleier": ("Wachteleier", "main", "Wachtelstall bei Nonna (täglich)", "Mut +1",
                    {"noun": "Wachteleier", "dat": "Wachteleiern", "stem": "Wachtelei"}),
    "huehnchen": ("Hühnchen", "main", "Hühnerstall bei Nonna (täglich)", "heilt 6 LP",
                  {"noun": "Brathähnchen", "dat": "Hähnchen", "stem": "Hähnchen"}),
    "schweinefleisch": ("Schweinefleisch", "main", "Schweine bei Nonna (alle 2 Tage)", "Max-LP +4",
                        {"noun": "Schweinebraten", "dat": "Schweinefleisch", "stem": "Schweine"}),
    "rindfleisch": ("Rindfleisch", "main", "Rinder bei Nonna (alle 3 Tage)", "Schutz +1 in jedem Kampf",
                    {"noun": "Rindersteak", "dat": "Rind", "stem": "Rinder"}),
    # fetched
    "wildschwein": ("Wildschwein", "main", "Gegner Wildschwein (Macchia)", "Kraft +1",
                    {"noun": "Wildschweinbraten", "dat": "Wildschwein", "stem": "Wildschwein"}),
    "flussfisch": ("Flussfisch", "main", "angeln: Fluss, Bergsee", "Wahrnehmung +1",
                   {"noun": "Forellenfilet", "dat": "Forelle", "stem": "Forellen"}),
    "meeresfisch": ("Meeresfisch", "main", "angeln: Boot, Strand", "heilt 10 LP",
                    {"noun": "Doradenfilet", "dat": "Dorade", "stem": "Doraden"}),
    "krabben": ("Krabben", "main", "sammeln: Strand, Grotte", "+1 Taschenplatz bei Erkundungen",
                {"noun": "Krabbenpfanne", "dat": "Krabben", "stem": "Krabben"}),
    "tintenfisch": ("Tintenfisch", "main", "angeln: Strand", "Krit +5 %",
                    {"noun": "Calamari", "dat": "Calamari", "stem": "Calamari"}),
    "steinpilze": ("Steinpilze", "main", "sammeln: Berge", "+1 Fund pro Erkundung",
                   {"noun": "Steinpilzpfanne", "dat": "Steinpilzen", "stem": "Steinpilz"}),
    "kastanien": ("Kastanien", "main", "sammeln: Berge", "+1 Ausdauer in jedem Kampf",
                  {"noun": "Maronen", "dat": "Maronen", "stem": "Maronen"}),
    "honig": ("Wilder Honig", "accent", "sammeln: Berge", "Begehren-Gesten +1",
              {"post": "mit Honigglasur", "mit": "Honig", "stem": "Honig"}),
    "thunfisch": ("Thunfisch ✦", "main", "angeln: Boot (selten)", "Schaden +2",
                  {"noun": "Thunfischsteak", "dat": "Thunfisch", "stem": "Thunfisch"}),
    "sepia": ("Sepia-Tinte ✦", "accent", "Gegner Seeungeheuer · selten beim Tintenfisch", "Krit +8 %",
              {"post": "al nero", "mit": "Sepia", "stem": "Sepia"}),
}

FAVOURITES = {  # person: (dish, ingredients)
    "Lea": ("Bún riêu", {"reis", "tomaten", "krabben"}),
    "Totò": ("Thịt kho", {"eier", "fischsauce", "wildschwein"}),
    "Yasin": ("Bibimbap", {"reis", "chilis", "wachteleier"}),
    "Sophia": ("Sommerrollen", {"reis", "fischsauce", "tintenfisch"}),
    "Rosi": ("Ramen", {"nudeln", "dashi", "steinpilze"}),
    "Lola": ("Bao Buns", {"mehl", "sojasauce", "wildschwein"}),
    "Alva": ("Chili Noodles", {"nudeln", "sojasauce", "chilis"}),
    "Madame Casanova": ("Bouillabaisse", {"tomaten", "kartoffeln", "meeresfisch"}),
    "Petru": ("Fish Pie", {"kartoffeln", "milch", "flussfisch"}),
    "Chiara": ("Spaghetti Bolognese", {"nudeln", "tomaten", "wildschwein"}),
    "Holm": ("Pytt i panna", {"kartoffeln", "eier", "wildschwein"}),
    "Siri": ("Fiskesuppe", {"meeresfisch", "milch", "wildkraeuter"}),
    "Megan": ("Kartoffel-Kräuter-Suppe", {"kartoffeln", "milch", "wildkraeuter"}),
    "Elsa": ("Kräuter-Baguettes", {"mehl", "milch", "wildkraeuter"}),
    "Maxwell": ("Braai", {"kartoffeln", "sojasauce", "wildschwein"}),
    "Yamamoto": ("Tamagoyaki", {"dashi", "eier", "wachteleier"}),
    "Jana": ("Kaiserschmarrn", {"mehl", "milch", "honig"}),
    "Isabelle": ("Galette de châtaigne", {"eier", "milch", "kastanien"}),
}
SLIME = {"name": "Brauner Schleim", "effect": "heilt 1 LP", "sell": 5, "trust": -6}


def n(i, key):
    return INGREDIENTS[i][4][key]


def dish_name(combo):
    for person, (dish, ings) in FAVOURITES.items():
        if set(combo) == ings:
            return dish, person
    b = [i for i in combo if INGREDIENTS[i][1] == "base"]
    m = [i for i in combo if INGREDIENTS[i][1] == "main"]
    a = [i for i in combo if INGREDIENTS[i][1] == "accent"]
    if len(b) >= 2:
        head = "-".join(n(i, "stem") for i in b) + "-Auflauf"
        rest = m + a
    elif b:
        head, rest = n(b[0], "noun"), m + a
    elif len(m) >= 2:
        head = "-".join(n(i, "stem") for i in m) + "-Spieß"
        rest = a
        m = []
    elif m:
        head, rest = n(m[0], "noun"), a
        m = []
    else:
        return "-".join(n(i, "stem") for i in a) + "-Dip", None
    mains = [i for i in rest if INGREDIENTS[i][1] == "main"]
    accents = [i for i in rest if INGREDIENTS[i][1] == "accent"]
    if mains and accents:
        post = n(accents[0], "post")
        post = "und " + post[4:] if post.startswith("mit ") else post      # no "mit ... mit ..."
        return "%s mit %s %s" % (head, n(mains[0], "dat"), post), None
    if len(mains) == 2:
        return "%s mit %s und %s" % (head, n(mains[0], "dat"), n(mains[1], "dat")), None
    if len(mains) == 1:
        return "%s mit %s" % (head, n(mains[0], "dat")), None
    if len(accents) == 2:
        return "%s mit %s und %s" % (head, n(accents[0], "mit"), n(accents[1], "mit")), None
    if len(accents) == 1:
        return "%s %s" % (head, n(accents[0], "post")), None
    return head, None


def main():
    ids = list(INGREDIENTS)
    rows = []
    for k in (2, 3):
        for combo in itertools.combinations(ids, k):
            name, person = dish_name(combo)
            rows.append({"gericht": name, "lieblingsgericht_von": person or "", "zutaten": " + ".join(INGREDIENTS[i][0] for i in combo),
                         "wirkung": " · ".join(INGREDIENTS[i][3] for i in combo), "anzahl": k})
    names = [r["gericht"] for r in rows]
    dupes = len(names) - len(set(names))
    with open(os.path.join(HERE, "kochbuch.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter=";")
        w.writeheader()
        w.writerows(rows)
    ing_rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        html.escape(v[0]), {"base": "Basis", "main": "Haupt", "accent": "Akzent"}[v[1]], html.escape(v[2]), html.escape(v[3]))
        for v in INGREDIENTS.values())
    page = TEMPLATE.replace("__ROWS__", json.dumps(rows, ensure_ascii=False)).replace("__ING__", ing_rows) \
        .replace("__COUNT__", str(len(rows)))
    with open(os.path.join(HERE, "kochbuch.html"), "w", encoding="utf-8") as fh:
        fh.write(page)
    print("%d Zutaten, %d Gerichte (%d aus 2, %d aus 3), %d Lieblingsgerichte, doppelte Namen: %d" % (
        len(ids), len(rows), sum(r["anzahl"] == 2 for r in rows), sum(r["anzahl"] == 3 for r in rows),
        sum(bool(r["lieblingsgericht_von"]) for r in rows), dupes))
    for r in rows[::400]:
        print("  ", r["gericht"], "|", r["zutaten"])


TEMPLATE = r"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Eden Kochbuch</title>
<style>
:root{--bg:#121318;--card:#1b1d24;--text:#f3eee4;--muted:#a8a294;--gold:#d8bd86}
@media (prefers-color-scheme: light){:root:not([data-theme="dark"]){--bg:#f4f1ea;--card:#fff;--text:#1d1c1a;--muted:#6b665c;--gold:#9a7b3c}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.4 system-ui,Segoe UI,sans-serif;padding:16px}
h1,h2{color:var(--gold);font-weight:600}h1{font-size:20px;margin:0 0 8px}h2{font-size:16px;margin:20px 0 8px}
.box{background:var(--card);border-radius:10px;padding:12px;overflow-x:auto}
table{border-collapse:collapse;width:100%}td,th{padding:5px 8px;border-bottom:1px solid #ffffff14;text-align:left;vertical-align:top}
th{color:var(--muted);font-weight:500}input,select{background:var(--card);color:var(--text);border:1px solid #ffffff30;border-radius:8px;padding:8px;font:inherit}
.fav{color:var(--gold);font-weight:600}.muted{color:var(--muted)}.bar{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
</style></head><body>
<h1>Eden Kochbuch</h1>
<p class="muted">Goldene Regel: 2 oder 3 <b>verschiedene</b> Zutaten. Sonst entsteht <b>Brauner Schleim</b>: heilt 1 LP, Verkauf 5 €, niemand mag ihn, −6 Vertrauen bei allen am Tisch.</p>
<h2>Zutaten</h2><div class="box"><table><tr><th>Zutat</th><th>Rolle</th><th>Quelle</th><th>Wirkung</th></tr>__ING__</table></div>
<h2>Alle __COUNT__ Gerichte</h2>
<div class="bar"><input id="q" placeholder="Suchen: Gericht oder Zutat …" style="flex:1;min-width:200px">
<select id="f"><option value="">alle</option><option value="fav">nur Lieblingsgerichte</option><option value="2">2 Zutaten</option><option value="3">3 Zutaten</option></select></div>
<div class="box"><table id="t"><thead><tr><th>Gericht</th><th>Zutaten</th><th>Wirkung (★)</th></tr></thead><tbody></tbody></table></div>
<p class="muted" id="info"></p>
<script>
const ROWS = __ROWS__;
const tb = document.querySelector("#t tbody"), q = document.getElementById("q"), f = document.getElementById("f");
function draw(){
  const s = q.value.toLowerCase(), mode = f.value;
  const hits = ROWS.filter(r => (!s || (r.gericht + " " + r.zutaten).toLowerCase().includes(s)) &&
    (!mode || (mode === "fav" ? r.lieblingsgericht_von : String(r.anzahl) === mode)));
  tb.innerHTML = hits.slice(0, 400).map(r => `<tr><td class="${r.lieblingsgericht_von ? "fav" : ""}">${r.gericht}${r.lieblingsgericht_von ? " ♥ " + r.lieblingsgericht_von : ""}</td><td>${r.zutaten}</td><td class="muted">${r.wirkung}</td></tr>`).join("");
  document.getElementById("info").textContent = hits.length + " Treffer" + (hits.length > 400 ? " (erste 400 angezeigt, Suche eingrenzen)" : "");
}
q.oninput = draw; f.onchange = draw; draw();
</script></body></html>"""

if __name__ == "__main__":
    main()
