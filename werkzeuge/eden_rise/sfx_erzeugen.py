# -*- coding: utf-8 -*-
r"""Sound-Effekte bei ElevenLabs erzeugen und speichern (18.10.2026) - einmalig, nicht live.

    Sfx_EdenRise.bat                     alles, was noch fehlt (vorhandene Dateien werden uebersprungen)
    Sfx_EdenRise.bat --nur wuerfel_rollen   nur diese Effekte (mehrere mit Komma), vorhandene ueberschreiben
    Sfx_EdenRise.bat --liste             nur anzeigen, was erzeugt wuerde (kein Aufruf, kein Guthaben)

Quelle: module\eden_rise\sfx.json (werkzeuge\eden_rise\sfx_eden_rise.py). Ablage: module\eden_rise\sfx\<id>_<n>.mp3
plus sfx\index.json (welcher Prompt zu welcher Datei gehoert - ein geaenderter Prompt wird neu erzeugt) und
sfx\vorhoeren.html zum Anhoeren im Browser. Schluessel: eden-config.json -> elevenlabs_config (Voice Studio);
er wird nie ausgegeben."""
import json, os, re, sys, time, urllib.error, urllib.request

HIER = os.path.dirname(os.path.abspath(__file__))
EDEN = os.path.dirname(os.path.dirname(HIER))
MOD = os.path.join(EDEN, "module", "eden_rise")
ORDNER = os.path.join(MOD, "sfx")
INDEX = os.path.join(ORDNER, "index.json")
API = "https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128"


def arg(name, std=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv and sys.argv.index(name) + 1 < len(sys.argv) else std


def schluessel():
    cfg = json.load(open(os.path.join(EDEN, "eden-config.json"), encoding="utf-8-sig"))
    pfad = cfg.get("elevenlabs_config") or r"X:\AI\VoiceStudio\voice-studio.json"
    key = (json.load(open(pfad, encoding="utf-8-sig")).get("api_key") or "").strip()
    if not key:
        sys.exit("Kein ElevenLabs-Schluessel gefunden (Voice Studio: voice-studio.json).")
    return key


def erzeugen(key, s):
    body = json.dumps({"text": s["prompt"], "duration_seconds": s["dauer"], "prompt_influence": s["einfluss"],
                       "loop": False, "model_id": "eleven_text_to_sound_v2"}).encode()
    req = urllib.request.Request(API, data=body, headers={"xi-api-key": key, "Content-Type": "application/json",
                                                          "Accept": "audio/mpeg"})
    for versuch in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            text = e.read().decode("utf-8", "replace")[:300]
            if e.code in (429, 500, 502, 503) and versuch < 2:
                time.sleep(5 * (versuch + 1))
                continue
            raise RuntimeError("HTTP %d: %s" % (e.code, text))
        except urllib.error.URLError as e:
            if versuch < 2:
                time.sleep(5)
                continue
            raise RuntimeError(str(e))


GRUPPEN = [("ui", "Oberfläche & Fortschritt"), ("wuerfel", "Würfel"), ("effekt", "Story & Orte"),
           ("mehr", "Weitere Anlässe")]


def vorhoerseite(sfx, index):
    esc = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    teile, nav, vorhanden = [], [], 0
    # Nummer bleibt die aus dem ganzen Katalog (wie im Spiel), gezeigt werden nur offene Effekte: gewaehlte sind eingebaut.
    nummer = {s["id"]: i for i, s in enumerate([s for gid, _ in GRUPPEN for s in sfx if s["gruppe"] == gid], 1)}
    ausgeblendet = sum(1 for s in sfx if s.get("wahl"))
    for gid, gname in GRUPPEN:
        liste = [s for s in sfx if s["gruppe"] == gid and not s.get("wahl")]
        if not liste:
            continue
        nav.append('<a href="#g_%s">%s <span>%d</span></a>' % (gid, gname, len(liste)))
        teile.append('<h2 class="g" id="g_%s">%s</h2>' % (gid, gname))
        for s in liste:
            nr = nummer[s["id"]]
            wahl = s.get("wahl")
            konzepte = s.get("konzepte") or []
            dateien = sorted((k for k in index if re.fullmatch(re.escape(s["id"]) + r"_\d+\.mp3", k)
                              and os.path.exists(os.path.join(ORDNER, k))), key=lambda k: int(k[:-4].rsplit("_", 1)[1]))
            vorhanden += len(dateien)
            # Checkbox je Variante: data-v = Erzeugungszeit, damit eine im Browser gemerkte Wahl nach dem Neu-Erzeugen
            # nicht an einer anderen Datei haengen bleibt.
            zeilen = "".join('<label class="var"><input type="checkbox" class="wahl" data-n="%d" data-v="%s"%s>'
                             '<b>Variante %d</b><audio controls preload="none" src="%s"></audio>%s</label>'
                             % (n, esc((index.get(f) or {}).get("erzeugt", "")),
                                " checked" if n == wahl or (isinstance(wahl, list) and n in wahl) else "", n, f,
                                ('<span class="konzept">%s</span>' % esc(konzepte[n - 1]["name"])) if n <= len(konzepte) else "")
                             for n, f in enumerate(dateien, 1))
            if konzepte:   # eigener Prompt je Variante: Liste statt eines Prompts
                s = dict(s, prompt=" · ".join("%d %s: %s" % (i, k["name"], k["prompt"].split(", single very short")[0])
                                              for i, k in enumerate(konzepte, 1)))
            alle = ('<button class="alle" onclick="alle(this)">▶ alle %d nacheinander</button>' % len(dateien)) if dateien else ""
            teile.append('<section id="%s" data-nr="%d"' % (s["id"], nr) + (' data-mehrfach="1"' if s.get("mehrfach") else "")
                         + '><div class="kopf"><h3><span class="nr">%d</span>%s '
                         '<span class="st"></span><small>%.1f s · %d/%d Varianten</small></h3>%s</div>'
                         '<p class="w">%s</p>%s<input class="notiz" placeholder="Notiz (z. B. „mehr klirren“) – optional">'
                         '<p class="p">%s</p></section>'
                         % (nr, s["id"], s["dauer"], len(dateien), s["varianten"], alle,
                            esc(s["wofuer"]), zeilen or "<i>noch nicht erzeugt</i>", esc(s["prompt"])))
    # Musik-Bereich (20.10.2026): offene Song-Takes aus ComfyUI - fehlt der Ordner, bleibt die Seite reine SFX-Seite
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import musik_auswahl
        m_nav, m_teile, m_takes = musik_auswahl.abschnitt(esc)
    except Exception as e:                                           # Musik darf die SFX-Seite nie verhindern
        m_nav, m_teile, m_takes = "", "<p class='leer'>Musik nicht lesbar: %s</p>" % esc(str(e)), 0
    css = ('body{background:#0f1115;color:#ece6da;font:15px/1.5 "Segoe UI",sans-serif;max-width:900px;margin:24px auto;padding:0 16px}'
           'h1{color:#d8bd86;margin-bottom:4px}h2.g{color:#d8bd86;font-size:19px;margin:30px 0 4px;border-bottom:1px solid #2b3039;padding-bottom:4px}'
           'section{border:1px solid #2b3039;border-radius:14px;padding:12px 16px;margin:12px 0}'
           '.kopf{display:flex;align-items:center;justify-content:space-between;gap:10px}h3{margin:0;font-size:17px}'
           'h3 small{color:#a3a8b1;font-weight:400;font-size:13px}.w{margin:4px 0 8px}'
           '.var{display:flex;align-items:center;gap:12px;margin:4px 0}.var b{width:90px;font-weight:500;color:#a3a8b1}'
           '.p{color:#7d828b;font-size:12px;margin:8px 0 0}'
           'nav{position:sticky;top:0;background:#0f1115ee;padding:8px 0;display:flex;gap:8px;flex-wrap:wrap;z-index:2}'
           'nav a{color:#ece6da;text-decoration:none;border:1px solid #2b3039;border-radius:999px;padding:3px 12px;font-size:13px}'
           'nav a:hover{border-color:#d8bd86}nav a span{color:#a3a8b1}'
           'button.alle{background:#1a1d24;color:#d8bd86;border:1px solid #2b3039;border-radius:8px;padding:4px 10px;cursor:pointer;font-size:13px}'
           'button.alle:hover{border-color:#d8bd86}section.spielt{border-color:#d8bd86}'
           '.nr{display:inline-block;min-width:30px;margin-right:8px;padding:1px 7px;border-radius:8px;background:#d8bd86;'
           'color:#0f1115;text-align:center;font-size:14px}'
           '.st{font-size:12px;font-weight:500;border-radius:999px;padding:1px 9px;margin:0 6px}'
           '.st.ok{background:#1f3a2a;color:#8fd6a5}.st.neu{background:#3a2f1a;color:#e6c27a}'
           'section.fertig .var{opacity:.45}section.fertig .var.gewaehlt{opacity:1}'
           '.var{border-radius:8px;padding:2px 6px;margin-left:-6px;cursor:pointer}'
           '.var.gewaehlt{background:#1f3a2a}.var.gewaehlt b{color:#8fd6a5}'
           '.konzept{color:#d8bd86;font-size:14px}'
           'input.wahl{width:20px;height:20px;accent-color:#8fd6a5;cursor:pointer;flex:none}'
           'input.notiz{width:100%;box-sizing:border-box;margin-top:8px;background:#1a1d24;color:#ece6da;'
           'border:1px solid #2b3039;border-radius:8px;padding:6px 10px;font:inherit;font-size:14px}'
           'input.notiz:focus{outline:none;border-color:#d8bd86}'
           'audio{max-width:100%}body{padding-bottom:90px}'
           '#leiste{position:fixed;left:0;right:0;bottom:0;background:#161a21f2;border-top:1px solid #2b3039;z-index:3}'
           '#leiste div{max-width:900px;margin:0 auto;padding:10px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}'
           '#leiste span{flex:1;color:#a3a8b1;font-size:14px}#leiste b{color:#ece6da}'
           '#leiste button{background:#d8bd86;color:#0f1115;border:0;border-radius:8px;padding:7px 14px;font:inherit;'
           'font-weight:600;cursor:pointer}#leiste button.zweit{background:#1a1d24;color:#a3a8b1;border:1px solid #2b3039;font-weight:400}'
           '.reiter{display:flex;gap:8px;margin:14px 0 4px}.reiter button{background:#1a1d24;color:#ece6da;border:1px solid #2b3039;'
           'border-radius:10px;padding:8px 16px;font:inherit;font-weight:600;cursor:pointer}'
           '.reiter button[aria-pressed=true]{background:#d8bd86;color:#0f1115;border-color:#d8bd86}.reiter span{font-weight:400;opacity:.75}'
           'body[data-bereich=sfx] #b_musik,body[data-bereich=musik] #b_sfx{display:none}'
           'details.spiel{margin-top:8px;color:#a3a8b1;font-size:14px}details.spiel summary{cursor:pointer}'
           'details.spiel .var b{width:auto;min-width:200px;font-size:13px}.leer{color:#7d828b;font-size:13px;margin:8px 0 0}')
    js = ('document.addEventListener("play",e=>{document.querySelectorAll("audio").forEach(a=>{if(a!==e.target)a.pause()});},true);'
          'function alle(b){const s=b.closest("section"),l=[...s.querySelectorAll("label.var audio")];let i=0;'
          'const n=()=>{if(i>=l.length){s.classList.remove("spielt");return}s.classList.add("spielt");const a=l[i++];'
          'a.onended=n;a.currentTime=0;a.play()};n()}'
          # Wahl: je Effekt eine Checkbox, bei data-mehrfach beliebig viele (Abwechslung im Spiel); im Browser gemerkt
          # (localStorage, je Datei mit Erzeugungszeit), Kopieren liefert den Text fuer Claude.
          'const KEY="eden_sfx_wahl2",secs=[...document.querySelectorAll("section[data-nr],section[data-mnr]")];'
          'const sS=secs.filter(s=>s.dataset.nr),sM=secs.filter(s=>s.dataset.mnr);'
          # Bereich SFX/Musik umschalten, gemerkt
          'function bereich(b){document.body.dataset.bereich=b;document.querySelectorAll(".reiter button").forEach(x=>'
          'x.setAttribute("aria-pressed",String(x.dataset.b===b)));try{localStorage.setItem("eden_vorhoer_bereich",b)}catch(e){}}'
          'let _b="sfx";try{_b=localStorage.getItem("eden_vorhoer_bereich")||(sS.length?"sfx":"musik")}catch(e){}bereich(_b);'
          'let mem={};try{mem=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){}'
          'const an=s=>[...s.querySelectorAll("input.wahl:checked")];'
          # Nummer als Text merken: Musik-Takes heissen "082" (fuehrende Null)
          'function merken(){const m={};secs.forEach(s=>{m[s.id]={sel:an(s).map(c=>[c.dataset.n,c.dataset.v]),'
          'notiz:s.querySelector(".notiz").value.trim()}});try{localStorage.setItem(KEY,JSON.stringify(m))}catch(e){}}'
          'function zeigen(s){const c=an(s),st=s.querySelector(".st");'
          's.classList.toggle("fertig",!!c.length);s.querySelectorAll(".var").forEach(v=>v.classList.toggle("gewaehlt",c.some(x=>v.contains(x))));'
          'st.className="st "+(c.length?"ok":"neu");'
          'st.textContent=c.length?"✓ "+(s.dataset.art||"Variante")+" "+c.map(x=>x.dataset.n).join(", ")+" gewählt":(s.dataset.mehrfach?"offen · mehrere möglich":"offen");'
          'const z=l=>l.filter(x=>an(x).length).length;'
          'document.getElementById("zahl").textContent="SFX "+z(sS)+"/"+sS.length+" · Musik "+z(sM)+"/"+sM.length}'
          'secs.forEach(s=>{const g=mem[s.id];if(g&&Array.isArray(g.sel)){const gut=g.sel.filter(([n,v])=>{'
          'const b=s.querySelector("input.wahl[data-n=\'"+n+"\']");return b&&b.dataset.v===v}).map(([n])=>String(n));'
          'if(gut.length||!g.sel.length)s.querySelectorAll("input.wahl").forEach(b=>b.checked=gut.includes(b.dataset.n));'
          's.querySelector(".notiz").value=g.notiz||""}'
          's.querySelectorAll("input.wahl").forEach(b=>b.addEventListener("change",()=>{'
          'if(b.checked&&!s.dataset.mehrfach)s.querySelectorAll("input.wahl").forEach(x=>{if(x!==b)x.checked=false});zeigen(s);merken()}));'
          's.querySelector(".notiz").addEventListener("input",merken);zeigen(s)});'
          'function zeile(s,kopf){const c=an(s),t=s.querySelector(".notiz").value.trim();'
          'return kopf+": "+(c.length?(s.dataset.art||"Variante")+" "+c.map(x=>x.dataset.n).join(", "):"offen")+(t?" – "+t:"")}'
          # Musik: nur Songs mit Haekchen oder Notiz (84 Takes "offen" waeren nur Rauschen)
          'function text(){const m=sM.filter(s=>an(s).length||s.querySelector(".notiz").value.trim());'
          'return "SFX-Auswahl (vorhoeren.html)\\n"+sS.map(s=>zeile(s,s.dataset.nr+". "+s.id)).join("\\n")'
          '+(m.length?"\\n\\nMusik-Auswahl\\n"+m.map(s=>zeile(s,"M"+s.dataset.mnr+". "+s.dataset.titel)).join("\\n"):"")}'
          'function kopieren(b){const t=text(),ok=()=>{b.textContent="✓ kopiert";setTimeout(()=>b.textContent="📋 Auswahl kopieren",1500)};'
          'if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(ok,()=>zeigText(t))}else zeigText(t)}'
          'function zeigText(t){const a=document.createElement("textarea");a.value=t;document.body.appendChild(a);a.select();'
          'try{document.execCommand("copy")}catch(e){}a.remove();alert(t)}'
          'function zuruecksetzen(){if(!confirm("Alle Häkchen und Notizen auf den gespeicherten Stand zurücksetzen?"))return;'
          'try{localStorage.removeItem(KEY)}catch(e){}location.reload()}')
    offen = sum(1 for s in sfx if not s.get("wahl"))
    html = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>Eden Vorhören</title>'
            '<meta name="viewport" content="width=device-width, initial-scale=1"><style>' + css +
            '</style></head><body data-bereich="sfx"><h1>Eden Rise · Vorhören</h1>'
            '<p>Häkchen = diese Variante bzw. diesen Take nehmen. Unten „Auswahl kopieren“ und den Text an Claude geben – '
            'SFX und Musik in einem Text. Die Seite verschiebt und löscht nichts.</p>'
            '<div class="reiter"><button type="button" data-b="sfx" onclick="bereich(\'sfx\')">Sound-Effekte <span>%d offen</span></button>'
            '<button type="button" data-b="musik" onclick="bereich(\'musik\')">Musik <span>%d Takes</span></button></div>'
            '<div id="b_sfx"><p>%d Effekte im Katalog. Hier stehen nur die offenen; <b>%d gewählte sind ausgeblendet</b>, '
            'weil sie schon im Spiel eingebaut sind (Nummern bleiben wie im Katalog). %d Dateien gesamt.</p>'
            '<nav>%s</nav>%s</div>'
            '<div id="b_musik"><p>Offene Takes aus der Musikwerkstatt (ComfyUI, Ordner <code>eden_music\\drafts</code>), '
            'mehrere Häkchen je Song möglich – ein Musik-Slot spielt im Spiel als Playlist. „Schon im Spiel“ zeigt die '
            'freigegebenen Tracks desselben Songs zum Vergleich.</p><nav>%s</nav>%s</div>'
            '<div id="leiste"><div><span>Gewählt: <b id="zahl"></b></span>'
            '<button class="zweit" onclick="zuruecksetzen()">↺ Zurücksetzen</button>'
            '<button onclick="kopieren(this)">📋 Auswahl kopieren</button></div></div>'
            '<script>%s</script></body></html>'
            % (offen, m_takes, len(sfx), ausgeblendet, len(index), "".join(nav), "".join(teile), m_nav, m_teile, js))
    open(os.path.join(ORDNER, "vorhoeren.html"), "w", encoding="utf-8").write(html)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sfx = json.load(open(os.path.join(MOD, "sfx.json"), encoding="utf-8"))["sfx"]
    os.makedirs(ORDNER, exist_ok=True)
    index = json.load(open(INDEX, encoding="utf-8")) if os.path.exists(INDEX) else {}
    nur = set((arg("--nur") or "").split(",")) - {""}
    auftraege = []
    for s in sfx:
        if s.get("quelle") == "pixabay":           # Ducs Pixabay-Auswahl (27.10.2026): fertige Dateien, nie neu erzeugen
            continue
        if nur and s["id"] not in nur:
            continue
        for n in range(1, s["varianten"] + 1):
            datei = "%s_%d.mp3" % (s["id"], n)
            k = s["konzepte"][n - 1] if s.get("konzepte") else None                          # je Variante eigener Prompt
            v = dict(s, prompt=k["prompt"], dauer=k.get("dauer", s["dauer"])) if k else s
            fertig = os.path.exists(os.path.join(ORDNER, datei)) and (index.get(datei) or {}).get("prompt") == v["prompt"]
            if nur or not fertig:
                auftraege.append((v, datei))
    print("%d Effekte im Katalog, %d Dateien zu erzeugen (%.1f Sekunden Audio)." % (
        len(sfx), len(auftraege), sum(s["dauer"] for s, _ in auftraege)))
    if "--liste" in sys.argv:
        for s, datei in auftraege:
            print("  %-26s %5.1f s  %s" % (datei, s["dauer"], s["wofuer"]))
        vorhoerseite(sfx, index)
        return
    key = schluessel() if auftraege else None
    fehler = 0
    for i, (s, datei) in enumerate(auftraege, 1):
        try:
            daten = erzeugen(key, s)
        except Exception as e:
            fehler += 1
            print("  FEHLER %s: %s" % (datei, e))
            continue
        open(os.path.join(ORDNER, datei), "wb").write(daten)
        index[datei] = {"id": s["id"], "prompt": s["prompt"], "dauer": s["dauer"], "bytes": len(daten),
                        "erzeugt": time.strftime("%Y-%m-%d %H:%M")}
        json.dump(index, open(INDEX, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  [%d/%d] %s (%d KB)" % (i, len(auftraege), datei, len(daten) // 1024))
    vorhoerseite(sfx, index)
    print("Fertig. %d Fehler. Anhoeren: %s" % (fehler, os.path.join(ORDNER, "vorhoeren.html")))


if __name__ == "__main__":
    main()
