/* Spoiler-free combat reminders from balance v3 with the v4 Schuetze overrides.
 * Vendetta direct damage intent follows the user clarification; its numeric balance is open.
 * Reference only: this visual preview does not execute combat rules. */
window.EdenAttackRules={
 scirocco:{type:'M3 · Glutschlag',level:3,cost:3,effect:'Treffer +4 und +1 Brandstufe am Gegner. Danach ungedeckt.'},
 retour:{type:'M5 · Rachefeuer',level:5,cost:2,effect:'Antwort auf einen Spezialangriff: Gegenschlag ×2, bei schwachem Spezialangriff ×1; Gegner +1 Brandstufe. Keine Parade: Duc nimmt den vollen Treffer und erhält ebenfalls +1 Brandstufe.'},
 furia:{type:'M7 · Flammenrausch',level:7,cost:3,effect:'Du brennst 3 Runden. Beim Angriff entlädt sich eine Feuerpeitsche; jeder Treffer setzt +1 Brandstufe. Während des Flammenrauschs ×1,3 Schaden und kein Verteidigen.'},
 vulcano:{type:'M9 · Feuersturm',level:9,cost:4,effect:'Jederzeit startbar: ein Schlag je Brandstufe am Gegner mit jeweils 60 % Schaden, ignoriert Schutz und verbraucht alle Stufen. Danach 1 Runde aussetzen. Das Labor zeigt 1–5 Stufen; ohne Stufen gibt es keinen Schlag.'},
 mistral:{type:'K3 · Wuchtschlag',level:3,cost:3,effect:'Angriff mit +4 Schaden. Das Ziel wird für 2 Runden erschüttert.'},
 wave:{type:'K5 · Konterwelle',level:5,cost:3,effect:'Schwächt den nächsten Angriff des Ziels. Gegen ein nasses Ziel verursacht der Treffer doppelten Schaden.'},
 wind:{type:'K7 · Windrüstung',level:7,cost:2,effect:'Für 2 Runden +4 Angriff. Du bist zunächst ungedeckt. Brennt das Ziel bereits, wird sein Brennen um eine Runde verlängert.'},
 tidal:{type:'K9 · Riesenwelle',level:9,cost:4,effect:'Doppelter Schaden, gegen erschütterte Ziele dreifacher Schaden. Benötigt ein erschöpftes oder blutendes Ziel, alternativ nass plus Schlamm.'},
 doubleSlash:{type:'L3 · Doppelschnitt',level:3,cost:3,effect:'Zwei getrennte Treffer mit jeweils 70 % des normalen Schadens.'},
 blur:{type:'L5 · Abtauchen',level:5,cost:2,effect:'Halbiert den nächsten eingehenden Treffer. Dein nächster Angriff wird garantiert kritisch.'},
 vendetta:{type:'L7 · Blutschnitt',level:7,cost:3,effect:'Wuchtiger Schnitt mit direktem Schaden und Blutung. Wirkt nicht gegen Maschinen.'},
 blackSlash:{type:'L9 · Gnadenstoß',level:9,cost:4,effect:'Garantiert kritischer Treffer mit 2,5-fachem Krit-Faktor; jeder negative Zustand am Ziel verstärkt den Angriff zusätzlich um 25 %. Benötigt erschöpft, blutend oder nass plus Schlamm.'},
 reticle:{type:'W3 · Zielmarke',level:3,cost:2,effect:'Erschöpft das Ziel für 3 Runden und bereitet Folgeangriffe vor. Verursacht selbst keinen direkten Schaden.'},
 calm:{type:'W5 · Ruhepuls',level:5,cost:2,effect:'Vergrößert das nächste Paradefenster um 50 %; ein nasses Ziel verstärkt den Vorteil zusätzlich. Ein perfekter Konter verursacht doppelten Schaden.'},
 beam:{type:'W7 · Leuchtfeuer',level:7,cost:3,effect:'Das Ziel setzt einen Zug aus. Steht es unter Strom, setzt es zwei Züge aus.'},
 rain:{type:'W9 · Sternsalve',level:9,cost:4,effect:'Drei Treffer mit jeweils 85 % Schaden. Gegen fliegende Ziele trifft jeder mit 100 % Schaden.'}
};

Object.assign(window.EdenAttackRules,{
  "balm": {
    "type": "H3 · Heilöl",
    "level": 3,
    "cost": 3,
    "effect": "Heals 30 % of your HP and soothes a burn or a bleeding wound."
  },
  "westWind": {
    "type": "H5 · Westwind",
    "level": 5,
    "cost": 3,
    "effect": "For 3 rounds you heal 10 % of your HP every round, and your parry window is 10 % wider."
  },
  "awaken": {
    "type": "H7 · Erwachen",
    "level": 7,
    "cost": 4,
    "effect": "Heals 80 % of your HP. Once per fight."
  },
  "archangel": {
    "type": "H9 · Erzengel",
    "level": 9,
    "cost": 4,
    "effect": "If you fall in this fight, you rise again with half your HP. Once per fight."
  }
});
