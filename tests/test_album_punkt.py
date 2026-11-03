# -*- coding: utf-8 -*-
"""Leuchtender Punkt bei neuen Selfies (Duc 02.11.2026, docs/wiki/systeme/beziehungen.md). Echter Client in Headless-Chrome, Aufbau wie test_ui_kopfzeile.

  python tests\\test_album_punkt.py
"""
import os, shutil, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import test_ui_kopfzeile as K  # noqa: E402

PRUEFUNG = r"""<script>window.addEventListener("load", async () => {
  const warte = ms => new Promise(r => setTimeout(r, ms)), e = {}, $$ = s => document.querySelector(s), $$$ = s => [...document.querySelectorAll(s)];
  await warte(1500);
  const herz = () => !!$$('#dock button[aria-label="Relationships (B)"] .dock-punkt');
  const eintrag = (bild, titel) => ({art: "selfie", tag: 11, titel, notiz: null, bild});
  zeichnen(); await warte(30);           // ohne Netz war der erste Aufruf schneller als das Menue-Plugin
  e.alte_still = !herz();
  V.z.album.find(p => p.id === "rosi").eintraege.push(eintrag("/selfie/neu_rosi.webp", "New Rosi"));
  V.z.album.push({id: "lea", name: "Lea", eintraege: [eintrag("/selfie/neu_lea.webp", "New Lea")]});
  zeichnen(); await warte(30);
  e.herz = herz();
  EdenMenu.tab("inventory"); await warte(30);
  e.reiter = !!$$$(".em-tab").find(b => b.textContent.includes("Relationships")).querySelector(".em-dot");
  EdenMenu.tab("bez"); await warte(30);
  zeichnen(); await warte(30);
  e.knopf = !!$$$(".em-knopf").find(b => b.textContent.includes("Open album")).querySelector(".em-licht");
  EdenMenu.ansicht("album"); await warte(30);
  const seite = () => $$(".em-album-wer .gold").textContent.trim();
  const erste = seite();
  e.seite_neu = erste === "Rosi" || erste === "Lea";
  e.neu_marke = $$$(".em-polaroid .em-neu").length === 1;
  e.andere_punkt = $$$(".em-album-wer .em-licht").length === 1;
  zeichnen(); await warte(30);
  e.neu_bleibt = $$$(".em-polaroid .em-neu").length === 1;
  EdenMenu.albumWer(erste === "Rosi" ? "lea" : "rosi"); await warte(30);
  e.andere_aus = !$$(".em-album-wer .em-licht");
  EdenMenu.ansicht("overview"); await warte(30);
  e.knopf_aus = !$$$(".em-knopf").find(b => b.textContent.includes("Open album")).querySelector(".em-licht");
  EdenMenu.zu(); await warte(30);
  e.herz_aus = !herz();
  document.body.insertAdjacentHTML("beforeend", `<pre id="ergebnis">${JSON.stringify(e)}</pre>`);
});</script>"""


def main():
    if not K.CHROME:
        print("Uebersprungen: Chrome nicht gefunden")
        return
    ordner = tempfile.mkdtemp(prefix="eden_album_")
    try:
        v = K.stand(11, 0)
        ziel = v.get("z", v)
        ziel["album"] = [{"id": "rosi", "name": "Rosi", "eintraege": [{"art": "selfie", "tag": 5, "titel": "Grease", "notiz": None, "bild": "/selfie/alt_rosi.webp"}]}]
        e = K.lesen(K.chrome(os.path.join(ordner, "profil"), "--virtual-time-budget=6000", "--window-size=1366,768", "--dump-dom",
                             K.seite(ordner, "album.html", v, PRUEFUNG)))
        print(e)
        K.pruefen(e["alte_still"], "was schon im Album liegt, gilt beim ersten Lauf als gesehen")
        K.pruefen(e["herz"] and e["reiter"] and e["knopf"], "neues Selfie: Punkt auf Herz, Reiter und Open album")
        K.pruefen(e["seite_neu"] and e["neu_marke"], "der Knopf zeigt die Frau mit dem neuen Foto, dort steht NEW")
        K.pruefen(e["andere_punkt"], "die andere Frau mit neuem Foto traegt im Album einen Punkt")
        K.pruefen(e["neu_bleibt"], "NEW bleibt beim Neuzeichnen stehen")
        K.pruefen(e["andere_aus"] and e["knopf_aus"] and e["herz_aus"], "alle Seiten gesehen: alle Punkte sind aus")
    finally:
        shutil.rmtree(ordner, ignore_errors=True)


if __name__ == "__main__":
    main()
