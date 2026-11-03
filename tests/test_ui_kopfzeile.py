# -*- coding: utf-8 -*-
"""Kopfzeile mit Status-Knoepfen (Duc 30.10.2026, docs/wiki/systeme/ui_stil.md). Laedt den echten Client mit dem echten
Spielstand aus eden.ansicht in Headless-Chrome, ohne Server: fetch ist ersetzt, Plugins kommen von der Platte.

  python tests\\test_ui_kopfzeile.py [--bild ordner]
"""
import json, os, re, shutil, subprocess, sys, tempfile

EDEN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, EDEN)
import eden  # noqa: E402
from kern import zustand  # noqa: E402

CHROME = next((p for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                           r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                           os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")) if os.path.exists(p)), None)
CLIENT = os.path.join(EDEN, "client").replace("\\", "/")


def stand(tag, moral):
    modul = eden.modul_laden()
    z = zustand.neu(modul, "entspannt")
    zustand.persona_setzen(z, modul, modul["personas"][0])
    z["tag"] = tag
    z["werte"]["moral"] = moral
    return json.loads(json.dumps(eden.ansicht(z), default=str))


def seite(ordner, name, v, pruefung=""):
    html = open(os.path.join(CLIENT, "index.html"), encoding="utf-8").read()
    html = re.sub(r'(href|src)="/plugins/', r'\1="file:///%s/plugins/' % CLIENT, html)
    stub = """<script>window.EDEN_UI_SPRITE="file:///%s/plugins/eden-ui/icons.svg";
const STAND=%s;window.fetch=async u=>({ok:true,status:200,json:async()=>String(u).includes("/api/stand")?STAND:{}});</script>""" % (
        CLIENT, json.dumps(v))
    html = html.replace("<title>Eden</title>", "<title>Eden</title>" + stub, 1).replace("</body>", pruefung + "</body>")
    pfad = os.path.join(ordner, name)
    open(pfad, "w", encoding="utf-8").write(html)
    return "file:///" + pfad.replace("\\", "/")


def chrome(profil, *args):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-first-run", "--hide-scrollbars", "--allow-file-access-from-files",
                           "--user-data-dir=" + profil, *args], capture_output=True, timeout=120, encoding="utf-8", errors="replace")


PRUEFUNG = r"""<script>window.addEventListener("load", async () => {
  const warte = ms => new Promise(r => setTimeout(r, ms)), e = {}, $$ = s => document.querySelector(s);
  await warte(1500);
  const knopf = k => $$(`#hudstatus .ui-status[data-k="${k}"]`), karte = () => $$("#hudstatus .ui-infokarte");
  e.schiff_weg = !$$("#schiff");
  e.pille = !$$("#zeitpille").hidden;
  e.knoepfe = [...document.querySelectorAll("#hudstatus .ui-status")].map(b => b.dataset.k);
  e.labels = [...document.querySelectorAll("#hudstatus .ui-status")].map(b => b.getAttribute("aria-label"));
  e.icon_moral = knopf("moral").querySelector("use").getAttribute("href").split("#")[1];
  e.niedrig = knopf("moral").classList.contains("niedrig");
  e.ruf_niedrig = knopf("ruf").classList.contains("niedrig");
  e.namen_tag11 = getComputedStyle(knopf("ruf").querySelector(".ui-name")).display;
  e.sprite_sichtbar = !!knopf("ruf").querySelector("use").getBBox().width;
  e.breite = $$("#zeitpille").offsetWidth;
  e.hoehe = $$("#zeitpille").offsetHeight;
  knopf("ruf").click(); await warte(30);
  e.karte_auf = !!karte() && karte().querySelectorAll(".ui-mehr").length === 1;
  e.karte_text = karte().querySelector(".ui-mehr p").textContent.slice(0, 30);
  karte().querySelector('.ui-zeile[data-k="moral"]').click(); await warte(30);
  e.karte_wechsel = knopf("moral").getAttribute("aria-expanded") === "true" && karte().querySelectorAll(".ui-mehr").length === 1;
  hud(V.z); await warte(30);
  e.karte_bleibt = !!karte();
  document.dispatchEvent(new KeyboardEvent("keydown", {key: "Escape", bubbles: true})); await warte(30);
  e.esc_zu = !karte();
  e.esc_kein_menue = overlay === null;
  knopf("energie").click(); await warte(30); document.body.click(); await warte(30);
  e.klick_daneben_zu = !karte();
  knopf("energie").click(); await warte(30); knopf("energie").click(); await warte(30);
  e.zweiter_klick_zu = !karte();
  // Aenderung: gleiche Werte melden nichts, eine neue Stimmung meldet Puls, Zahl, Name
  hud(V.z); e.keine_meldung = !$$("#hudstatus .ui-delta");
  const moral = V.z.sonst.find(s => s.key === "moral");
  moral.wert = -3; hud(V.z); await warte(30);
  e.delta = $$('#hudstatus .ui-status[data-k="moral"] .ui-delta')?.textContent;
  e.meldung = $$("#hudstatus .ui-wertmeldung")?.textContent;
  // Neues Spiel: keine Meldung, obwohl sich Werte unterscheiden
  document.querySelectorAll("#hudstatus .ui-delta,#hudstatus .ui-wertmeldung").forEach(x => x.remove());
  V.z.id = "anderes"; moral.wert = 3; hud(V.z); await warte(30);
  e.neues_spiel_still = !$$("#hudstatus .ui-delta");
  // Menue-Leiste: acht Knoepfe, alle aus dem Woerterbuch, die alten Symbole sind weg
  const dock = [...document.querySelectorAll("#dock button")];
  e.dock = dock.map(b => (b.querySelector("use")?.getAttribute("href") || "").split("#")[1]);
  e.dock_sichtbar = dock.every(b => b.querySelector("use").getBBox().width > 0);
  e.alte_symbole = !!document.getElementById("i-handy");
  // Hinweise auf Karten und Antworten
  const symbol = /[☀-➿⬀-⯿]|[\ud83c-\ud83e][\udc00-\udfff]/;
  const hinw = hinweisHtml([{wert: "diesel", kostet: 1, label: "diesel", hat: 3}, {wert: "strom", bringt: 1, label: "power", hat: 2}]);
  e.hinweis_icons = (hinw.match(/#(\w+)"/g) || []).join();
  e.hinweis_rein = !symbol.test(hinw);
  const opt = evOpt({text: "x", probe: {attribut: "charm", sg: 12}, energie: 1, orte: [{id: "a", name: "Bar", liebling: true}]}, 0);
  e.option_icons = (opt.match(/#(\w+)"/g) || []).join();
  e.option_rein = !symbol.test(opt);
  // Chat-Knoepfe: feste und gezeichnete, alle aus dem Woerterbuch
  V.z.status = "szene";
  V.z.szene = {titel: "T", log: [], buehne: [], max: 5, zug: 1, gesten: {liste: []}, ermittlung: {aktionen: [{}, {}], widersprueche: [], konfrontation: []}};
  document.getElementById("app").dataset.status = "szene";
  document.getElementById("app").classList.remove("chat-zu");
  chat(V.z); await warte(200);
  const ids = s => [...document.querySelectorAll(s + " use")].map(u => u.getAttribute("href").split("#")[1]);
  e.chat_icons = ["#gestenknopf", "#ermknopf", "#senden", "#chatauf", "#chatkopf", "#chips", "#ermhinweis"].map(s => ids(s).join("+"));
  e.chat_rein = !symbol.test(["#eingabe", "#chatkopf", "#chips", "#chatauf"].map(s => $$(s).textContent).join(""));
  e.senden_sichtbar = $$("#senden use").getBBox().width > 0;
  const sb = $$("#senden").getBoundingClientRect(), si = $$("#senden svg").getBoundingClientRect();
  e.senden_mittig = Math.abs((sb.left + sb.right) - (si.left + si.right)) < 2;
  e.toast_unter_leiste = parseFloat(getComputedStyle($$("#toast")).top) >= $$("#zeitpille").getBoundingClientRect().bottom;
  e.alte_chat_symbole = ["i-senden", "i-chat", "i-aus", "i-ton", "i-stumm"].some(i => document.getElementById(i));
  // Ein Icon im Text bleibt im Fluss: keine fremde Klasse darf es aus dem Platz heben (.em des Menues, 30.10.2026)
  const probe = document.createElement("div");
  probe.style.cssText = "position:fixed;left:300px;top:300px;font-size:40px";
  probe.innerHTML = uiIc("done", "imtext");
  document.body.appendChild(probe);
  const ps = probe.querySelector("svg"), pc = getComputedStyle(ps), pr = ps.getBoundingClientRect();
  e.icon_im_fluss = pc.position === "static" && pr.width === 40 && Math.abs(pr.left - 300) < 2 && pc.backgroundImage === "none";
  probe.remove();
  // Emoji aus Servertexten werden zentral zu Icons, der Handy-Chat bleibt
  const sv = document.createElement("div"); sv.textContent = "📱 Message <b> from Lea";
  const hg = document.createElement("div"); hg.className = "geraet"; hg.style.display = "none"; hg.textContent = "📱 bleibt";
  document.body.append(sv, hg); await warte(60);
  e.emoji_icon = sv.querySelector("use")?.getAttribute("href").split("#")[1];
  e.emoji_text_weg = !sv.textContent.includes("📱") && sv.textContent.includes("<b>");   // nur Ja/Nein: das Ergebnis selbst durchlaeuft auch den Beobachter
  e.emoji_handy_bleibt = hg.textContent.includes("📱");
  sv.remove(); hg.remove();
  // Pillen und Karten kommen aus den Tokens: Aenderung an einer Stelle wirkt ueberall
  const pl = document.createElement("span"); pl.className = "mm"; document.body.append(pl);
  e.pille_vorher = getComputedStyle(pl).paddingLeft;
  document.documentElement.style.setProperty("--pille", "1px 33px");
  e.pille_nachher = getComputedStyle(pl).paddingLeft;
  document.documentElement.style.removeProperty("--pille"); pl.remove();
  // Fenster schliessen und zurueck: Handy mit und ohne Faden, Fenster-Kopf, Toast
  V.z.status = "wahl"; ebeneOeffnen("handy"); await warte(150);
  const hk = () => [...document.querySelectorAll(".hkopf button")].map(b => [b.getAttribute("aria-label"), b.querySelector("use")?.getAttribute("href").split("#")[1], b.querySelector("use")?.getBBox().width > 0].join(":"));
  e.handy_kopf = hk();
  e.handy_rund = parseFloat(getComputedStyle($$(".geraet")).borderTopLeftRadius);
  overlay = null; zeichnen();
  // Journal: Auftrag offen und zugeklappt, Favour mit allen Ausgaengen
  V.z.status = "wahl";
  const auftrag = (id, neben) => ({id, titel: "T " + id, von_name: "Lea", status: "aktiv", neben, ort: "Harbour", zeiten: ["nacht"], frist: V.z.tag + 1, text: "t", naechster: "n",
    schritte: [{text: "a", erledigt: true}, {text: "b", erledigt: false}]});
  V.z.auftraege = [auftrag("eins", false), auftrag("zwei", true)];
  V.z.journal = V.z.auftraege;
  V.z.favours = [{titel: "F", von_name: "Lea", kette: "k", teile: [{titel: "1", ausgang: "ok"}, {titel: "2", ausgang: "daneben"}, {titel: "3", ausgang: "abgelehnt"}]}];
  ebeneOeffnen("journal"); await warte(120);
  EdenMenu.auf("zwei", true); await warte(60);           // neu = offen; einmal zuklappen, damit auch die Zeile geprueft wird
  const j = $$(".em-journal") || $$('.em[data-tab="journal"]') || document.body;
  e.journal_da = !!$$('.em[data-tab="journal"]');
  e.journal_auftraege = document.querySelectorAll(".em-auftrag").length;
  e.journal_rein = !symbol.test(j.textContent) && !/[▴▾]/.test(j.textContent);
  e.journal_icons = [...new Set([...j.querySelectorAll("use")].map(u => u.getAttribute("href").split("#")[1]))].sort().join();
  document.body.insertAdjacentHTML("beforeend", `<pre id="ergebnis">${JSON.stringify(e).replace(/</g, "&lt;")}</pre>`);
});</script>"""

PRUEFUNG_TAG1 = r"""<script>window.addEventListener("load", async () => {
  await new Promise(r => setTimeout(r, 1500));
  const n = document.querySelector('#hudstatus .ui-status[data-k="ruf"] .ui-name');
  document.body.insertAdjacentHTML("beforeend", `<pre id="ergebnis">${JSON.stringify({name: n.textContent, sichtbar: getComputedStyle(n).display})}</pre>`);
});</script>"""


def lesen(r):
    treffer = [t for t in re.findall(r'<pre id="ergebnis">(.*?)</pre>', r.stdout, re.S) if t.startswith("{")]   # nicht der Text im Skript
    if not treffer:
        raise AssertionError("kein Ergebnis: " + r.stderr[-600:])
    return json.loads(treffer[-1].replace("&lt;", "<"))


def pruefen(bed, text):
    if not bed:
        raise AssertionError(text)
    print("OK", text)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if not CHROME:
        print("Uebersprungen: Chrome nicht gefunden")
        return
    bild = sys.argv[sys.argv.index("--bild") + 1] if "--bild" in sys.argv else None
    ordner = tempfile.mkdtemp(prefix="eden_ui_")
    try:
        profil = os.path.join(ordner, "profil")
        e = lesen(chrome(profil, "--virtual-time-budget=6000", "--window-size=1366,768", "--dump-dom",
                         seite(ordner, "tag11.html", stand(11, -2), PRUEFUNG)))
        print(json.dumps(e, ensure_ascii=False))
        pruefen(e["schiff_weg"] and e["pille"], "eine Leiste, die zweite ist weg")
        pruefen(e["knoepfe"] == ["moral", "ruf", "energie"], "Stimmung, Ruf, Energie als Knoepfe")
        pruefen("Crew Mood: Tense" in e["labels"] and "Village Reputation: barely known" in e["labels"], "Name und Zustand fuer Screenreader")
        pruefen(e["icon_moral"] == "mood-tense", "Gesicht folgt der Stimmung")
        pruefen(e["niedrig"] and not e["ruf_niedrig"], "niedrig nur bei Tense")
        pruefen(e["namen_tag11"] == "none", "ab Tag 3 nur Icons")
        pruefen(e["karte_auf"] and e["karte_text"].startswith("What the village"), "Klick oeffnet die Infokarte mit dem echten Text")
        pruefen(e["karte_wechsel"] and e["karte_bleibt"], "Zeile wechselt, Neuzeichnen schliesst nicht")
        pruefen(e["esc_zu"] and e["esc_kein_menue"], "Esc schliesst nur die Karte, nicht ins Menue")
        pruefen(e["klick_daneben_zu"] and e["zweiter_klick_zu"], "Klick daneben und zweiter Klick schliessen")
        pruefen(e["keine_meldung"], "ohne Aenderung keine Meldung")
        pruefen(e["delta"] == "−1" and e["meldung"] == "Crew Mood: Tense", "Aenderung meldet Zahl, Name und Zustand")
        pruefen(e["neues_spiel_still"], "neues Spiel meldet nichts")
        pruefen(e["dock"] == ["phone", "map", "backpack", "character", "love", "journal", "codex", "menu"] and e["dock_sichtbar"] and not e["alte_symbole"],
                "Menue-Leiste kommt aus dem Woerterbuch")
        pruefen(e["hinweis_rein"] and "#diesel" in e["hinweis_icons"] and "#power" in e["hinweis_icons"], "Hinweise ohne Emoji, Diesel und Strom als Icons")
        pruefen(e["option_rein"] and "#dice" in e["option_icons"] and "#energy" in e["option_icons"], "Antworten: Wuerfel und Energie als Icons")
        pruefen(e["chat_icons"][:4] == ["gestures", "investigate", "send", "talk"] and e["chat_icons"][4] in ("voice-on+collapse-side", "voice-off+collapse-side")
                and e["chat_icons"][5] == "ideas" and e["chat_icons"][6] == "investigate", "Chat-Knoepfe kommen aus dem Woerterbuch")
        pruefen(e["chat_rein"] and not e["alte_chat_symbole"], "Chat ohne Emoji, alte Symbole weg")
        pruefen(e["senden_sichtbar"] and e["senden_mittig"], "Senden-Icon sichtbar und mittig")
        pruefen(e["toast_unter_leiste"], "Toast liegt unter der Kopfzeile, nicht darauf")
        pruefen("Close phone:close:true" in e["handy_kopf"], "Handy schliesst mit dem Kreuz aus dem Woerterbuch")
        pruefen(e["handy_rund"] == 46, "Handy bleibt ein Handy, kein Kreis")
        pruefen(e["icon_im_fluss"], "Icon im Text bleibt an seinem Platz und waechst mit der Schrift")
        pruefen(e["emoji_icon"] == "phone" and e["emoji_text_weg"] and e["emoji_handy_bleibt"], "Server-Emoji werden zu Icons, Text bleibt Text, der Handy-Chat bleibt")
        pruefen(e["pille_nachher"] == "33px" and e["pille_vorher"] != "33px", "Token --pille steuert die Pillen zentral")
        pruefen(e["journal_da"] and e["journal_auftraege"] >= 2, "Journal zeigt die Auftraege")
        pruefen(e["journal_rein"], "Journal ohne Emoji und Pfeilzeichen")
        pruefen(all(i in e["journal_icons"] for i in ("done", "failed", "declined", "place", "deadline", "collapse", "expand")), "Journal nutzt die Icons fuer Schritte, Ort, Frist und Klappen")
        t = lesen(chrome(profil, "--virtual-time-budget=4000", "--window-size=1366,768", "--dump-dom",
                         seite(ordner, "tag1.html", stand(1, 0), PRUEFUNG_TAG1)))
        pruefen(t["sichtbar"] != "none" and t["name"] == "Reputation", "an Tag 1-2 stehen die Namen dabei")
        if bild:
            os.makedirs(bild, exist_ok=True)
            karte = '<script>window.addEventListener("load",()=>setTimeout(()=>document.querySelector(\'#hudstatus .ui-status[data-k="moral"]\').click(),1200));</script>'
            for name, v, zusatz, breite in (("tag11", stand(11, -2), "", 1366), ("tag11_karte", stand(11, -2), karte, 1366), ("tag1", stand(1, 0), "", 1366), ("tag11_gross", stand(11, 4), "", 1920)):
                chrome(profil, "--virtual-time-budget=4000", "--force-device-scale-factor=1", "--window-size=%d,768" % breite,
                       "--screenshot=" + os.path.join(bild, name + ".png"), seite(ordner, name + ".html", v, zusatz))
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


if __name__ == "__main__":
    main()
