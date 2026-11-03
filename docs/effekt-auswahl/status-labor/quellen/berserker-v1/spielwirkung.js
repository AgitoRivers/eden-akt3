/* Spoiler-free combat reminders from balance v3 with the v4 Schuetze overrides.
 * Vendetta direct damage intent follows the user clarification; its numeric balance is open.
 * Reference only: this visual preview does not execute combat rules. */
window.EdenAttackRules={
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
