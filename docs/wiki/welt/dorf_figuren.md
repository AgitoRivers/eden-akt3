# Die neuen Dorf-Figuren und das Geflecht von Cala d'Orsu

> Stand 30.10.2026 · Besitz: Hauptsitzung · Register E-089, E-093 · **Entwurf nach Ducs Notizen, nichts davon ist gebaut.**
> Die Story-Sitzung hat Pascal und Sandru am 30.10. gegen die Fälle geprüft: kein Widerspruch, ihre Auflagen sind eingearbeitet.
> Character Design übernimmt die Fakten auf die Figurenseiten, sobald Sprites und Stimmen anstehen. Beispielzeilen sind Entwürfe in einfachem Englisch.

**Quelle gilt so:** Ducs Notizen gehen vor. Was er nicht umgeschrieben hat, bleibt aus den Brain-Trust-Runden und ist so
angepasst, dass es dazu passt.

**Festa und Ehrenbürger bleiben ohne festes Datum (Duc 30.10.), sind aber die Schlussszene von Akt 3 (E-100).** Die Events im Code bleiben unverändert, nichts in dieser
Seite darf an einem Festa-Tag hängen. Die Belagerung bleibt Tag 21. Akt 3 hat zwei Wochen (Tag 22–35).

## Überblick

| Figur | Rolle | Kommt | Grauton |
|---|---|---|---|
| **Pascal Leca** (bisher „Tomà“) | stellvertretender Bürgermeister | Tag 2 | echter Verräter, von Anfang an von Alon gekauft |
| **Mina Orsoni** | Post und Pakete auf der Vespa | Tag 3 | keiner, trägt unwissentlich die Spur |
| **Bà Tư** („Auntie Tu“) | Asia-Laden | Tag 8–9 | verkauft an alle und steht dazu |
| **Sandru** (Iskander Amrani, Namensschild „ALEX“) | Filialleiter A.V. Market, korsisch-marokkanisch | Tag 10 | gekauft, weil er sonst nicht mehr laufen kann; flieht vor seiner Herkunft |
| **Don Anghjulu** (Padre Ângelo) | Pfarrer aus Portugal, Trunkenbold | Tag 12–14 | liebenswerter Opportunist, Dach von A.V.-Geld |

**Namen:** „Tomà“ liest sich fast wie „Totò“, darum Pascal. Alex, Alva und Alon sehen sich zu ähnlich, darum zeigt das Spiel
Sandru an. Nur A.V. nennt ihn Alex. So hat A.V. schon zwei Menschen umbenannt oder falsch benannt, und das zahlt auf Pascals
Ende ein.

## Akt 1 im Spiel (Phase 2, Texte in `docs/abnahme/dorf_akt1_texte.json`)

| Wann | Szene | Was Duc bekommt |
|---|---|---|
| Tag 2 | `hk_pascal`, nach dem Abend am Hafen | 2 Bandagen, keine Rechnung |
| Tag 3 nachmittags | `g1_mina_post` | Mina, sie nennt Duc „Yacht“ |
| Tag 4 morgens | `hy_pascal_holm` (Handy) | Moral +1 |
| Tag 4 nachmittags | `g1_pascal_gebuehren` | Americano, 120 € |
| Tag 5 nachmittags, Megan an Bord | `gv_casanova_megan` | Vertrauen, Ruf |
| Tag 6 morgens | `g1_casanova_morgen` | Vertrauen Casanova |
| Tag 6 nachmittags, wenn „Forty Minutes“ lief | `g1_pascal_telefon` | Moral +1 |
| nach Ricci Stufe 3, frühestens Tag 8 (Riccis ab Tag 3, je 2 Tage Abstand, 5 % je Ladenbesuch), bis Tag 21 | `g1_pascal_ricci` | Jade für Terremoto, Ruf +1 |
| nach dem Kloster-Auftrag | `kl_pascal_tuer`, `kl_mina_post` | Bandage, Espresso, Item `kl_post` (Flag `kl_post_dabei`, wirkt in Phase 3) |

Geändert: `hk_abend` (führt zu Pascal), `hy_casanova_konfetti`, `g1_casanova_nebel`, `gv_casanova_alva`, `kl_casanova_auftrag`, `br_satellit_sonntag` (Flag `br_satellit`).
Bilder der Figuren fehlen bis zur Abnahme, im Spiel erscheint so lange ein Platzhalter.

## Aussehen (Duc 30.10., E-099)

Grundsatz: Wir sind auf Korsika, alle sind sonnengebräunt, nicht weiß.

| Figur | Look |
|---|---|
| **Pascal** | doppelreihiger Nadelstreifenanzug, Einstecktuch, Halbglatze, freundliches Gesicht. Der Anzug ist etwas zu gut für das Gehalt eines stellvertretenden Bürgermeisters: eine stille Spur, die niemand im Spiel ausspricht |
| **Mina** | pinke Regenjacke, enge beige Hot Pants, oversized Bluse, pinker Helm |
| **Bà Tư** | hochgestecktes Haar, vietnamesische Seidenbluse, luftige schwarze Hose mit gelben Blumen, **kein Kochlöffel** (sonst Kopie von Nonna) |
| **Sandru** | korsisch-marokkanisch, weißes A.V.-Poloshirt, Namensschild ALEX, schwarze Beinschienen |
| **Don Anghjulu** | braun gebrannter Portugiese, rundlich, schwarze Soutane mit aufgekrempelten Ärmeln, Flachmann |

**Adrien Morel (Berge, schon im Spiel):** Ein gutaussehender Inder, 28. Geburtsname **Arjun**, „Adrien Morel“ hat ihm die Fremdenlegion gegeben. Das spiegelt Sandru:
Beiden hat ein System den Namen genommen. Nur Laetitia kennt den echten, später sagt er ihn Petru. *“Hm.”* Wolff nennt ihn weiter Morel. Kostet 10 neu vertonte Zeilen,
eine neue Stimme und ein neues Sprite-Set.

## Bauplan und Stand

| Phase | Was | Stand |
|---|---|---|
| **0. Casting** | Aussehen und vier Hintergründe (Character Design), Stimmen (`docs/abnahme/stimmen_dorf/`) | Stimmen gewählt. Sets bei Duc zur Abnahme, Mina macht Duc selbst, Hintergründe offen |
| **1. Fundament** | Figuren im Modul, je 3–4 Legenden-Zeilen, `ereignisse_dorf.py`, `tests/test_dorf_figuren.py` | fertig 30.10. |
| **2. Akt 1** | Pascal und Mina: 6 Szenen geändert, 10 neu (siehe unten), Ruf-Regel. Danach Ducs Akt-1-Spieltest | Texte von Duc abgenommen, gebaut 30.10. |
| **3. Woche 2** | Bà Tư mit Laden (Tag 9, `g1_batu_intro`, ohne Lola `g1_batu_intro_allein`), „Have You Called Your Mother?“ (Tag 12), Sandru (Tag 10), Die Tafel (Tag 13), Totenfeier und Minas Frage direkt nach Le Large, Don hinter Kevins Dächern (`kv_don`), Messe (Tag 14), sechs Szenen im Vorbeigehen (`g1_vb_*`), Orte `batu_shop`, `av_market`, `church` | Texte von Duc abgenommen, gebaut 30.10. Die Szene „The Back Seat“ kommt später, weil Nonna und Isabelle nur in Orts-Ketten auftreten dürfen. Die Fischsauce ist vorerst ein Geschenk-Item, als Kochzutat offen |
| **4. Woche 3** | Restliche Sandru-Szenen, Pascals Verrat, zusammen mit der Belagerung und Story | offen |
| **5. Akt 3** | Schublade, Nonna, Rädchen, Kommission, Villa, Netz, Epilog, zusammen mit Story | offen |

IDs: `pascal`, `mina`, `batu`, `sandru`, `anghjulu`. Die Figuren werden erst durch ihre erste Szene „bekannt“; bis dahin tauchen sie
weder im Handy noch im Menü auf. Neue Szenen kommen nach `ereignisse_dorf.py`.

---

## Pascal Leca: „Leave it with me.“

**Kurz:** 52, stellvertretender Bürgermeister seit vielen Jahren. Wohnt über dem Rathaus, isst im Stehen, kennt jeden im
Dorf und jeden in der Crew beim Namen. Casanova ist die Bühne, er ist alles dahinter. Vorbild: Long Feng in Avatar, in der
Wärme eher Cait Sith. Er muss wirklich witzig und wirklich nützlich sein. Gegenvorbild: Kai Leng, ein Verräter ohne Würde.

**Aussehen (Duc 30.10., E-099):** trägt einen **weißen Fedora**. Der Nadelstreifenanzug bleibt bewusst farbig (dunkel, kein Weiß), weil Weiß Mr. Whites Erkennungsfarbe ist.

**Will:** das Dorf am Leben halten, egal mit wessen Geld. **Widerspruch:** wirklich gütig und wirklich ein Verräter, seine Hilfe ist
nie gespielt. **Erkennbar an:** „Leave it with me.“, kennt jeden Namen, isst im Stehen.

**Stimme:** freundlich, leise, ganze Sätze, macht sich gern über sich selbst lustig. Sagt immer den Namen der anderen. Nennt
Duc „Duc“, vom ersten Abend an. Der Einzige im Dorf, der klatscht, wenn Casanova ihre Pause macht.

**Warum er gekauft ist:** Das Dorf starb. Keine Schule mehr, kein Arzt, junge Leute weg. Alons Geld kam über Pascal: das
Kirchendach, der Schulbus, das Festa-Budget, auch die Konfettikanone. Er glaubt bis fast zuletzt, dass er das Dorf rettet.
*“Nine years I kept this place alive. Who else was paying?”* Er riet Casanova zum Verkauf des Ladenhauses. Sie hält das für
allein ihre Schuld. Sein Argument muss gut genug sein, dass Spieler danach streiten, ob er recht hatte. Sein erster Handel war vor
neun Jahren der Verkauf der Villa von Casanovas Vater. Daher kommt „nine years“, und auf Casanovas Schweigen zum Elternhaus gibt es eine
Antwort, die sie nie erfahren wollte.

**Grenze seines Wissens (Story-Sitzung):** Pascal und Don wissen nichts von dem, was vor Tag 0 auf der Yacht geschah. Ihr Wissen beginnt
beim Geld fürs Dorf.

**Die Schublade (die Spur aller Fäden):** In seinem Schreibtisch liegen Dinge, die nie abgeschickt wurden:
- **Elsas Antennen-Formular.** Ihre Antenne wartet laut Kanon seit elf Monaten darauf. Jetzt wissen wir, warum.
- **Elsas Berichte an die Bürgermeisterin.** Elsa ist ihm direkt unterstellt, weil er „ihr den Rücken frei hält“. Sie hasst
  es, Casanova nicht direkt sprechen zu können.
- **Casanovas EU-Förderanträge,** unterschrieben und nie verschickt. Ein Dorf mit EU-Geld bräuchte Alons Geld nicht.
- **Die unterschriebenen Aussagen aus dem Red Trio,** falls Elsa sie bekommen hat (`rt_ende_alle`, `ark_aussagen_3`). Sie hat sie
  pflichtgemäß weitergereicht, also liegen sie hier.
- **Die Durchschläge seiner Monatsberichte nach Ajaccio:** „All quiet“, mit seiner Unterschrift.

### Wo Pascal Duc hilft (damit man ihn mag)

| Wann | Hilfe | Woran es hängt |
|---|---|---|
| Tag 2, `hk_abend` | Hat das Fass gerollt. Seine Schadensliste für Elsa nennt die Crew „defended the quay“. Keine Rechnung, keine Probleme | Text ändern |
| Tag 2 und danach | Täglicher Anruf im Krankenhaus wegen Holm. *“She threw a yoghurt at a doctor. I think that's a good sign, Duc.”* Fragt nach ihr, wenn alle anderen vergessen | neue kurze Handy-Zeilen |
| Tag 3–6 | Die Liegegebühren. Sophia flieht vor dem Hafenmeister (`bk_sophia_arm`), Pascal klärt es in einem Satz: keine Gebühr, solange die Yacht nicht fahren kann. Echtes Geld gespart | neu, klein |
| Tag 3–6 | `br_satellit_sonntag`: Lola und Jana streiten um 40 Minuten Satellit. Am Tag danach öffnet Pascal ihnen das Rathaus-Telefon. Die Crew liebt ihn | Nachklang |
| Fehlschlag | Geht bei Casanova etwas schief (Nebelmaschine, Probe verloren), nimmt er es auf sich. *“My fault, Madame. I ordered the wrong fog.”* | `g1_casanova_nebel` |
| Ruf im Dorf | Er erzählt Ducs Taten weiter. Das erste Verblassen des Rufs fällt aus. *“I told them about the boar again. It's bigger now.”* Mechanik verwoben mit [`dorf_redet.md`](../systeme/dorf_redet.md) | kleine Regel |
| Nach dem Kloster | Er organisiert die Totenfeier der Mönche und zahlt alles. Steht neben Duc. Bringt Nonna danach jede Woche Setzlinge. Kein Witz in dieser Szene | neu, ernst |

Die letzte Hilfe ist die wichtigste: Sie ist echt und zugleich sein schlechtes Gewissen. Er hat dem Pfarrer geraten, nicht
hochzugehen (*“Stay, Don. Leave it with me.”*). **Er wusste dabei nur die Ansage von oben, niemand solle den Berg betreten, und
hielt das für Sicherheit.** Von Toten und vom Löwen wusste er nichts. Das Gewissen kommt erst mit der Totenfeier, und in Akt 3
ist es sein schlimmstes Wissen, kein Plan.

**Totenfeier, Auflagen der Story-Sitzung:**
- Zwei Fassungen, weil `kl_garten` und `kl_garten_ohne` sehr verschieden sind. Ohne Frederico hat Nonna die Tür geschlossen, und
  in dieser Fassung gilt die Feier auch dem Kind.
- Ohne Zahl von Särgen und ohne dass Duc Tote birgt: Das Lager zeigt nur gefaltete Kutten.
- Am besten vor Nonnas langem Tisch im Red Trio (Tag 11–14), sie muss aber in beiden Reihenfolgen funktionieren.

**Faire Spuren:** Post aus Monaco (Mina, als Witz) · er misst Alvas Bar aus, „für die Samtkordel“ · „Pascal knows everything“
in Casanovas Büro · Elsas Formular ist immer „fast durch“.

**Regeln für die Spuren (Story-Sitzung):**
- **Pascal und Sandru bleiben außerhalb der Fälle:** nicht in `verdaechtige` oder `glieder`, kein Codex-Eintrag, kein Beweisstück,
  keine Aussage in der Anhörung. Pascal wird auch nicht die namenlose Mittelsperson aus `zweite_wahrheit`.
- **Monaco-Witz:** Mina macht ihn nur vor Megans Telefonat (`z_05`), danach nicht mehr. *“He gets more post from Monaco than your boss.”*
  Monaco passt auch zu Megans Büro, das ist die Tarnung.
- **Maßband:** Pascal kommt in `gv_casanova_alva` zu `PV` dazu, das Maßband steht nur im Text, ohne eigenen Hinweis. Der Boden unter
  der Bar gehört zum Hafenviertel, er misst also die Ware aus.
- **Megan:** Beim Bündnis mit Casanova begegnet sie Pascal nie direkt. Sie saß den Leuten in Monaco gegenüber und müsste ihn sonst
  erkennen oder nicht erkennen.
- **Casanovas Büro** (`kl_casanova_auftrag`, Zeile 93): *“Nobody. Pascal, of course, Pascal knows everything. Nobody else I trust.
  Petru says the mountain will speak when it wants to. I'm tired of waiting for mountains.”* Sie schließt die Tür selbst, und wenn
  Duc herauskommt, steht Pascal stumm davor.

### Auffliegen und Ende

- **Tag 21, Belagerung:** Pascal gibt Alon den Weg frei. Davor hält Casanova ihre Rede ans Dorf und macht ihre Pause. Er klatscht
  nicht. Das hängt nicht an der Festa. Er öffnet die Barrikade vor aller Augen (Duc 31.10.), Akt 3 zeigt nur noch das Ausmaß.
- **Der Moment der Wahrheit (Duc 01.11.2026):** Pascal hat darum gebeten, dass niemand verletzt wird. Minicu hält ihn fest, White schlägt Minicu mit einem Schlag KO und lacht höhnisch: *“You didn't really think we'd hold back?”* Bei Minicu, den brennenden Häusern und den zerstörten Bauten begreift Pascal zum ersten Mal, was hier passiert. Das wollte er nicht, aber es ist zu spät. Er ist nicht dumm: Jetzt muss er die Rolle weiterspielen, um das Dorf als Ganzes zu retten. Er bleibt ein Verräter, es ist keine Erlösung, und das Dorf erfährt davon nichts.
  - **Warum er den Norden öffnet:** Alon hat ihm gesagt: Piraten greifen an, A.V. kommt als Retter, niemand wird verletzt. Pascal öffnet, um das Feuer aus Welle 2 zu beenden, er glaubt also dieselbe Lüge, die Alon danach der Welt erzählt. Die toten Mönche hat er sich als Unfall zurechtgelegt (*“An accident. Nobody meant that.”*), das geht an Tag 21 nicht mehr.
  - **Die Szene:** Pascal: *“You gave me your word. Nobody gets hurt.”* White: *“You didn't really think we'd hold back?”* Pascal kniet sich zu Minicu und prüft, ob er noch atmet, schaut auf die brennende Bar und das Dach der Post, steht auf, zieht sein Sakko gerade und geht neben White her. *Then it ends quickly. Then it has to end quickly.* Der Spieler sieht das, das Dorf nicht.
  - **Die Rolle, Tag 21:** Nur Pascal kann White sagen: *“If the church burns, you have no signature.”* Deshalb bleibt die Kirche stehen, bis Duc da ist.
  - **Die Rolle, Akt 3:** Der Brief an Nonna und der Kellerschlüssel in der Kiste sind seine stille Hilfe. Im Finale dankt Alon ihm unter falschem Namen, und Pascal lächelt.
  - **Die Grenze:** Neun Jahre Geld und falsche Berichte bleiben wahr, Nonnas *“You have a bad conscience”* bleibt das letzte Wort über ihn. Es darf nie so aussehen, als sei er eigentlich ein Held gewesen.
- **Er verschwindet (Duc 31.10., Figur getauscht 01.11.2026):** Als alle wieder aufstehen, ist Pascal weg ([`belagerung.md`](belagerung.md)). Akt 3 spielt ohne ihn im Dorf,
  sein Zimmer über dem Rathaus steht leer, der Schreibtisch ist noch verschlossen. **Im Finale steht er neben Alon** (siehe „Das Rädchen“).
- **Keine Polizei (Duc 30.10., früh in Akt 3):** Elsa findet es komisch, dass nach allem, was in Akt 2 passiert ist, noch immer niemand aus
  der Hauptstadt ermittelt. *“A private army attacked this bay. I wrote it all down and sent it. And nobody from Ajaccio has called me.
  Not one person. Isn't that strange?”* Das schließt die Logiklücke, die jeder Spieler sieht. **Regel (gebaut):** Funk, Schlepper und Pakete
  laufen direkt, ihr Boot fährt selbst nach Ajaccio. Nur **förmliche Meldungen** gehen nach Vorschrift mit Gemeindestempel über das Rathaus.
  Sie hält sich daran, weil sie sich immer daran hält. Dann fährt sie hin und fragt am Schalter nach. *“They said, what report? They said
  Cala d'Orsu writes every month. All quiet.”* Es gab also nicht nur Stille, sondern falsche Berichte mit Pascals Unterschrift. Darum bricht
  sie seinen Schreibtisch auf.
- **Die Antwort aus Ajaccio (Duc 30.10., E-096):** Meldet sie danach direkt, kommt nach etwa zwei Tagen eine höfliche,
  aber langsame Antwort: Eine Kommission kommt zum Ende von Akt 3 (Tag 35), Beweise sichern. Das ist die Uhr für Akt 3 und der Grund,
  warum Duc selbst handeln muss. **Alon hat Beziehungen, und das wird nur angedeutet, nie bewiesen.** Der Beamte am Telefon: *“We're very busy here,
  Lieutenant. And we have the feeling you have this under control. Don't you?”* Elsa danach: *“Five years on this post, and they have never been
  this polite to me.”* A.V. sitzt in Monaco und seine Anwälte verlangen Beschlüsse, ohne Beschluss darf niemand in die Villa. Was die
  Kommission vorfindet (Aussagen des Trios, Ducs Wahl beim Kassenbuch), entscheidet im Epilog, ob sie Anklage erheben kann. Sie erfährt
  nichts über die Yacht von Tag 0, das bleibt Ducs Aufdeckung.
- **Die Schublade (Akt 3):** Elsa bricht sie auf. Eine ernste Szene, in der Elsa zum ersten Mal keinen Witz hat. *“Eleven
  months.”* Zwischen den Blättern findet sie auch die Aussagen, falls Duc sie ihr gebracht hat. Danach liest sie Casanova jeden
  Bericht vor, den die nie bekommen hat. Das Kassenbuch: Duc kann alles veröffentlichen
  oder nur Alons Teil (Säulen Wahrheit gegen Gemeinschaft), denn auch Pfarrer, Sandru und Casanova stehen darin.
- **Nonna (Akt 3, kurz und leise, Duc 31.10.: ohne Pascal):** Am Morgen nach der Belagerung steht wie jede Woche eine Kiste Setzlinge vor ihrer Tür, die letzte,
  mit einem Brief. Er schreibt, was er dem Pfarrer geraten hat. *“And I told him all of it, every month, for nine years. He can't say a word. That's why he drinks.”* So erfährt der Spieler
  von der Beichte, und Nonna versteht rückblickend, warum Don sich vor Pascals Tür gestellt hat. Sie liest es Duc vor und sagt es der Kiste, weil er nicht da ist:
  *“I told Isabelle that man has a good heart. You don't have a good heart, Pascal. You have a bad conscience.”* Dann pflanzt sie die Setzlinge doch ein, weil bei ihr auch die Pflanzen nicht hungrig bleiben. Das klingt bewusst an ihren Satz
  am langen Tisch an (*“I looked for the hate. … There was never anywhere to keep it.”*), wiederholt ihn aber nicht.
- **Das Rädchen (Duc 31.10.: im Finale):** Pascal steht beim letzten Auftritt neben Alon, im weißen Fedora. Alon dankt ihm vor laufendem Stream unter falschem Namen. Mr. White hat ihn nie gekannt. Der Mann, der alle Namen kannte,
  hatte für seinen Herrn keinen. Pascal wird in jedes Ende eingewoben (Duc 01.11.2026, [`enden.md`](enden.md)). Im Epilog kommt Minas Einschreiben mit der Kündigung zurück: *“Sign here.”* Niemand da. Der erste Brief, den sie nicht zustellen kann.
- **Der Preis:** Nach Pascals Sturz zahlt Alon nicht mehr, und das passiert **in jedem Durchlauf**. Der Schulbus fährt nicht mehr, das Kirchendach
  bleibt halb fertig und tropft über der ersten Reihe. Das Dorf sieht es, und einige geben Duc die Schuld. Die Wahl beim Kassenbuch entscheidet
  nur, wer zusätzlich die Rechnung trägt: Wer alles veröffentlicht, setzt auch Pfarrer, Sandru und Casanova dem Dorf aus. Kinder werden nur
  erwähnt (leere Haltestelle, schimpfende Eltern), Frederico bleibt das einzige Kind im Bild. Die Szene darf nicht auf ihn anspielen, falls er tot ist.
- **Die letzte Hilfe (die Villa ist Schauplatz in Akt 3, Duc 30.10.):** Pascal hat noch den Schlüssel zur alten Kellertür von Casanovas Elternhaus, die beim
  Umbau niemand ernst genommen hat. Er liegt unter den Setzlingen in Nonnas Kiste, sie gibt ihn Duc (Duc 31.10.). Auf dem Zettel steht, ohne Bitte um Vergebung: *“Leave it with—no. You do it. I just have the
  key.”* Duc darf ablehnen. Dann führt Casanova ihn selbst, sie kennt den Keller aus ihrer Kindheit. Das ist teurer und gibt ihr den Moment,
  ihr Elternhaus wieder zu betreten. Elsa darf davon nichts wissen. *“I don't want to know where you got that.”* Es ist keine Erlösung und auch kein
  Heldentod.

---

## Mina Orsoni: „I don't read them. I just know.“

**Kurz:** 24, fährt auf einer alten Vespa Post und Pakete durchs Dorf, nach Bastia und jede Woche hoch zum Kloster und zurück.
Frech, schnell, gut gelaunt, die frische Luft im Dorf. Einfach eine junge Frau, die hier gern lebt. Keine Pflicht-Romanze,
kein Mechanik-Erklärer.

**Will:** alles zuerst wissen und schnell fahren. **Widerspruch:** kennt die Geheimnisse aller, aber niemand fragt nach ihren.
**Erkennbar an:** „I don't read them. I just know.“ und „Not agaaaain!“

**Familie:** Bruder Dumè ist von Korsika ausgewandert. Er war mit Elsa zusammen, bevor er ging. Deshalb kennt Elsa Mina, seit
sie eine kleine Göre war.

**Ihr Brief:** Seit einem Jahr steckt in ihrer Tasche ein ungeöffneter Brief von Dumè aus Montréal, adressiert an sie selbst. „I don't
read them“ gilt also auch für ihre eigene Post. Das trägt ihr Gespräch mit Isabelle über den Mut. Am Ende öffnet sie ihn und entscheidet
selbst, ob sie bleibt. Beides ist in Ordnung, keine Tragik. Dass Dumè in Kanada lebt, hat nichts mit Alon zu tun und wird nie als Spur benutzt.

**Laufgags:** Der Strafzettel von Elsa (*“Not agaaaain!”*) · Casanova will keine Rechnungen mehr · Sie und Alva wetten, wer
etwas zuerst weiß · Ein Schwein auf Nonnas Farm heißt auch Mina (*“Who named a pig after me? …Is she fast?”*).

**Tag 21 (Duc 01.11.2026):** Sie kann nicht kämpfen, aber sie ruft bei hohem Ruf das Dorf zusammen und fährt mit Petru und Lea hinaus ([`belagerung.md`](belagerung.md)).

**Die Briefe:** Beim Kloster-Auftrag gibt sie Duc drei Wochen Post mit, weil sie nicht an den Tieren vorbeikommt. Ein Teil davon
ist an Mönche, die tot sind. Danach fragt sie Duc einmal: *“Did they read them?”* Das ist ihr einziger ernster Moment in Akt 2.

**Frederico (Duc: „traurig, aber gut“):** Stirbt er, übernimmt Mina die Ernte-Fahrt vom namenlosen Boten. Sie sagt nichts dazu
und grüßt jede Stewardess mit Namen, so wie er es getan hätte.

**Mina und Isabelle:** Beim Paket-Abholen sitzen sie manchmal oben am Berg und fragen sich, ob sie ein anderes Leben hätten,
wären sie nur mutiger. Mina: *“You could have left.”* Isabelle: *“So could you.”*

**Epilog:** Elsa kann Casanovas EU-Anträge aus der Schublade nun direkt schicken. Der erste echte Brief aus Brüssel kommt, Mina bringt ihn selbst zu
Casanova. *“I read this one.”* Er bezahlt den Bus wieder, sofern die Bucht nicht verloren ist.

---

## Bà Tư: „Eat. You're too thin.“

**Kurz:** um die 75, in Saigon geboren, kam 1975 nach Frankreich und vor Jahrzehnten nach Korsika, Katholikin, erste Reihe.
Führt den Asia-Laden hinter dem Hafen. **Sie kocht immer viel zu viel** und bringt es den Leuten nach Hause.
**Korrektur:** Sie kann kochen. Das alte „kann selbst nicht kochen“ ist gestrichen.

**Duc und sie:** Ducs Eltern sind nach dem Vietnamkrieg nach Deutschland geflohen (E-067). Sie ist die Erste auf der Insel, die
weiß, was das heißt, und fragt nicht danach. Sie nennt ihn „con“ (Kind), schimpft, dass er zu dünn ist, und fragt, wer seine
Mutter ist. Mit Ducs südostasiatischer Küche (Stärke Küche) entsteht ihr Kochen-Faden: Sie korrigiert sein Thịt kho.
Fremdwörter nur „con“ und „Ăn đi“ (iss), sonst einfaches Englisch mit Akzent im Satzbau, nie als Witz.

**Will:** dass alle satt sind und jeder Cent stimmt. **Widerspruch:** die Wärmste im Dorf rechnet am härtesten ab.
**Erkennbar an:** „Eat. You're too thin.“

**Grauton:** Sie verkauft auch an Alons Arbeiter, bis sie satt sind. *“I watched three flags leave Saigon. Customers stay.”*

**„Have you called your mother?“** Wer ihr folgt, bekommt eine kleine Szene, in der Duc wirklich zu Hause anruft.

**Warum sie zu viel kocht:** Sie kocht noch immer für die Tischgröße aus Saigon. Das sagt sie nur einmal, zu Nonna im Garten, und
erklärt es nicht weiter.

**Belagerung:** Alons Leute reden beim Essen. Bei hohem Vertrauen weiß sie, wann sie abrücken, und das senkt die Prozente.

**Intro (Tag 8–9):** Lola schleppt Duc hin, weil die Fischsauce an Bord bisher keine Quelle hat. Bà Tư sieht Duc, sagt erst nichts,
stellt ihm dann einen Teller hin. Lola bekommt keinen. *“You, later. Him, now.”*

---

## Sandru: Das Namensschild sagt ALEX

**Herkunft (Duc 30.10., E-097):** Korsisch-marokkanisch, Sohn von Landarbeitern aus der Ostebene. Marokkaner sind die größte Gruppe der
Eingewanderten auf Korsika. Das tut doppelt weh: die Beine und die Herkunft. **Er hat drei Namen.** Seine Eltern nannten ihn Iskander, die
arabische Form von Alexander. Das Dorf machte daraus Sandru, und A.V. macht daraus Alex. „Alex“ ist sein Weg, seiner Herkunft zu entfliehen,
und genau das macht ihn sympathisch: Er will einfach seinen Weg gehen. Das Spiel zeigt „Sandru“, seine Stimme bleibt ohne marokkanischen Klang,
denn den hat er sich abgewöhnt.

**Wie es gezeigt wird:** Nie eine Hassszene und keine Predigt, nur kleine Stiche, die er weglacht. Ein Tourist fragt, woher er wirklich komme.
*“From here. Ha. Over there, actually, you can see the house.”* Ghjuvans Regel „Everybody drinks“ war der Grund, warum er als Kind in die Bar durfte.

**Kurz:** 30, im Dorf aufgewachsen, eine fortschreitende Krankheit in den Beinen, dieselbe wie Alons. Filialleiter des A.V. Market
im Ladenhaus von Alvas Mutter, genau gegenüber ihrer Bar. Seine Beinschienen und die Stelle sind ein Paket: Studie von A.V.
gegen Arbeit für A.V. Die Schienen surren leise.

**Will:** einmal gerade vor Alva stehen. **Widerspruch:** liebt Alva und steht unter dem Logo im Haus ihrer Mutter.

**Stimme:** höflich, schnell, zu bemüht. Lacht vor dem eigenen Satz. Wenn er müde ist, sagt er die Wahrheit.

**Warum er ja gesagt hat (der Kern):** Er liebt Alva, seit sie Kinder sind. Er hat Komplexe, nicht genug für sie zu sein. Er wollte
einmal gerade vor ihr stehen. Dafür steht er nun im Haus ihrer Mutter unter dem Logo des Mannes, der ihr alles nimmt.

**Alva:** Sie ist fünf Jahre älter, hat auf ihn aufgepasst und sieht ihn wie ihren kleinen Bruder. Heimlich will sie einen starken
Mann. Sie liebt ihn, nur nicht so. Beide wissen das, keiner sagt es. Es endet nicht mit einem Paar, auch nicht in Akt 3.

**Elsa:** Kindheitsfreunde. Elsa, ein Jahr jünger, hat die Jungs verprügelt, die ihn geneckt haben. Sie ist froh, dass etwas aus
ihm geworden ist. Jeden Tag ein Laib Brot gratis, jeden Tag dasselbe Spiel. *“That's bribery, Sandru.”* *“It's bread, Elsa.”*
*“…Figs are fine. Bread is under review.”* Beide lachen.

**Satz an Duc:** *“You leave in three weeks. I need my legs in February.”*

**Rosi:** Sie hört als Erste das Surren. Dieselbe Technik wie ihre Chips. Sie kann ihm die Beine von A.V. befreien. Ist Rosi an
Tag 8 gefeuert (`gefeuert_rosi`), übernimmt Maxwell das Hören (Muster `a2_teil_maxwell`) und sie hilft aus der Ferne.

**Nonna:** Kauft nie etwas von seinem chemischen Zeug. Über ihn selbst hat sie keine Meinung.

**Tag 21 (Duc 01.11.2026):** Fällt Alva gegen Mr. White, rettet Sandru sie aus den Trümmern und versorgt sie. In Akt 3 bekommt das eine eigene Szene, wenn sich aufklärt, dass sie nur bewusstlos war. Es bleibt dabei: kein Paar.

**Rosis Schiene (Duc 01.11.2026):** Befreit Rosi ihn von A.V., baut sie ihm eine eigene Schiene, sonst könnte er nicht gehen. Mit ihr hebt er auch die Trümmer. Ohne Rosi bleibt er bei Alons Schienen, die ihm die Kraft dafür ebenso geben; danach schaltet A.V. sie ab.

**Nicht jede Rettung klappt:** Nur wenn Duc sich kümmert, befreit Rosi seine Beine. Sonst bleibt er Alons Mann und steht am Ende auf der
anderen Seite, auf seinen eigenen Füßen. Selbst gerettet bleibt er unbequem: *“A.V. gave me six years of walking. You gave me a speech.”*

**Intro (Tag 10):** Einen Tag nach Megans Anruf hängt das Logo vom Bauteil über dem Ladenhaus. Das Dorf steht davor. Er verteilt
Kaffee-Gutscheine. Alva schaut von gegenüber zu und kommt nicht. Am Namensschild steht ALEX. Elsa liest es vor und lacht ihn aus.

---

## Minicu: „I carry.“ (Duc 01.11.2026, Entwurf, nichts gebaut)

**Kurz:** Ein sanfter, langsamer Riese, das Dorf sagt „Little Minicu“ oder „Mini“, Vorbild sind Hodor und Baymax. Er trägt im Hafen die Kisten, Pascal hat ihm vor Jahren die Stelle besorgt, und er vertraut ihm ohne jeden Vorbehalt. Er fragt jeden, ob es wehtut. Wir lachen mit ihm, nie über ihn. Keine Romanze.

**Auftritte (Brain Trust 01.11.2026):** Höchstens fünf kleine Momente: Kevin sitzt an Tag 2 auf seinem Kopf und er bewegt sich nicht, Bà Tư füttert ihn, Mina scheitert an einem Paket, das er mit einem Finger hebt, Pascal bringt ihm sonntags im Rathaus bei, seinen Namen zu schreiben, und das Manöver. Keine Rückblende, keine Geschichte um seinen Namen. Maxwell redet über seine Kraft, Minicu schweigt. Seine Waffe ist eine Holzfälleraxt, Waffenart Klinge (Duc 01.11.2026). Pascal schlägt er nicht.

**Aussehen (Duc 01.11.2026, Casting 1b):** sehr groß und breit, weich statt muskulös, lange zottelige dunkelbraune Haare, voller Bart, cremefarbenes Arbeitshemd, braune Canvas-Latzhose, Lederstiefel. Satz: `karten_neu/minicu_satz.py`, 22 Posen liegen in `module/eden_rise/figuren/Minicu` (Set `minicu_standard`). Stimme: `Minicu - ENG.wav` (Probe auf Italienisch, Duc 01.11.2026). `P["minicu"]` und die Gesichter sind eingetragen.

**Tag 19, Manöver:** Pascal sagt zu ihm: *“Hold the line, Minicu. Leave it with me.”*

**Tag 21 (Duc 01.11.2026):** Er steht am Haupttor in der Bürgerwehr (statt Petru). Als Pascal die Seite wechselt, schlägt er ihn nicht, er hält ihn nur fest und versteht nicht, wie Pascal das tun konnte. Mr. White schlägt ihn mit einem einzigen Schlag KO. Was das bei Pascal auslöst, steht unter „Auffliegen und Ende“.

**Akt 3:** Er wacht verbunden auf und geht zurück auf seinen Posten, weil Pascal es ihm gesagt hat. Frühestens an Tag 23 und freiwillig kann Duc ihm sagen, dass er nach Hause gehen darf: *“Is Pascal coming?”* Danach hilft er beim Wiederaufbau, zerstörte Häuser stehen früher wieder; keine Szene nennt das als Belohnung. Im Ende „Neu geschrieben“ schreibt er seinen Namen selbst ins Netz, schief und langsam, neben Pascals leerem Knoten.

> **Vermerk (Duc, E-122, 04.11.):** Minicu ist schwer verletzt, der Spieler erfährt sein Überleben erst auf der Festa (Tag 35), er überlebt in allen Enden. Bis dahin bleibt die Tür zum Hinterzimmer der Kirche zu, *“Is Pascal coming?”* fragt er erst auf der Festa, beim Wiederaufbau hilft er nicht. Der Absatz oben gilt nur noch für das Netz im Ende „Neu geschrieben“. Umsetzung: `drehbuch_akt3.md` 5.27.

---

## Don Anghjulu: „God sees everything. Cut the cards.“

**Herkunft (Duc 30.10., E-097):** Portugiese, eigentlich Padre Ângelo. Portugiesen sind die zweitgrößte Gruppe der Eingewanderten auf Korsika, katholisch und
aus einem Weinland. Er kam vor 14 Jahren für die portugiesischen Landarbeiter und blieb. Das Dorf machte aus ihm „Don Anghjulu“.

**Kurz:** um die 60, Pfarrer von Cala d'Orsu, Trunkenbold und genau deshalb geliebt. Vorbild ist **Heiter aus Frieren**: warm, faul,
betrunken, und in dem einen Moment, in dem es zählt, plötzlich klüger als alle. Liebenswerter Opportunist. Sein neues Kirchendach
kommt aus A.V.-Geld, und er predigt trotzdem gegen Alon. *“The Lord provides. I don't ask which account.”*

**Tag 2:** Die Glocke läutet beim Hafenkampf „wrong, far too fast“, weil er seinen Rausch ausschlief und Pascal ziehen musste. An
Tag 14 hat er das nicht vergessen.

**Will:** Wein, Ruhe und ein dichtes Dach. **Widerspruch:** predigt gegen Alon und betet unter Alons Dach.

**Sein Geheimnis:** Pascal beichtet ihm seit neun Jahren. Don weiß **nur vom Geld** und ungefähr, von wem es kommt, und darf nichts sagen,
deshalb trinkt er. Von den Tieren und der Gefahr für die Mönche weiß er nichts, sonst wäre er nicht mehr liebenswert. Der Trunkenbold ist
in Wahrheit der einsamste Mann im Dorf. Der Spieler erfährt es aus Pascals Brief in der Nonna-Szene, nie aus Dons Mund, denn das Beichtgeheimnis
hält. Dazu wollte er zu den Mönchen hoch und ließ sich von Pascal abraten. Es bleibt bei wenigen Zeilen, keine Tragödie. *“The Lord provides.
I don't ask which account.”* wird im Rückblick bitter und bleibt, wie sie ist.

**Heiter-Moment (Akt 3):** Pascal ist fort, das Dorf will sein Zimmer über dem Rathaus ausräumen und alles ins Hafenbecken werfen. Don stellt sich nüchtern vor die Tür, ohne zu erklären warum. Nonna
begreift es erst später, durch Pascals Brief, und dann auch, warum sie ihm immer vergeben hat.

**Epilog (Duc 30.10.):** Eden Consulting sponsert das Kirchendach, ein kleiner, warmer Abschluss ohne große Geste. Don liest die Rechnung und
fragt diesmal doch: *“The Lord provides. …This time I asked which account.”* Im schlechten Ende nimmt Duc das Geld und vergisst das Dorf, dann wird das Dach nicht repariert (Duc 01.11.2026).

**Tag 21:** Pascal beichtet am Abend davor, ohne Einzelheiten. Das gibt Don einen Grund, nüchtern zu sein, ohne das Siegel zu brechen. Ob er
etwas ahnte, wird nie aufgelöst.

**Intro:** Wer Kevin jagt, trifft ihn am Fuß des Turms (`kv_ende`). *“Fourteen years I fight that bird.”* Sonst bei der Messe an Tag 14.

**Pay-off Belagerung:** Er läutet die Glocke. Nüchtern, im richtigen Takt, zum ersten Mal. Aufgabe für [`belagerung.md`](belagerung.md).

---

## Madame Casanova: was dazukommt

Der Ausbau läuft über das, was schon da ist, nicht über mehr Reden.

- **Bürgermeisterin für alle:** Sie schaut ab und zu bei Bà Tư vorbei, nennt sie „Auntie Tu“. Bà Tư kocht dann viel zu viel, und
  Casanova isst alles. Hier ist sie leise. Das ist neben dem Büro der zweite Ort, an dem sie keine Bühne braucht.
- **Mit dem Pfarrer:** Sie neckt ihn wegen des Messweins. *“Father. Was that the blood of Christ, or the good Patrimonio?”* Dazu der
  alte Streit „my bell tower“ gegen „God's bell tower“ (die Zeile `My Bell Tower` in `ereignisse_legenden.py` steht schon).
- **Mit Mina:** Mina soll bloß nicht wieder mit Rechnungen und Edikten der Zentralverwaltung kommen. Casanova will endlich ihre
  EU-Förderung. *“If that is another bill, throw it in the sea! Where is my European money?”* Mina: *“Brussels says hi. Also,
  you owe the water company.”* Ein Gag bis zur Schublade, dann nicht mehr.
- **Mit Pascal:** Er klatscht, und **sie weiß, dass er der Einzige ist** (Duc 30.10., `g1_casanova_morgen`: *“He thinks I don't know that he's the only one.”*). Darum trifft es sie an Tag 21 so hart, als er nicht klatscht.
- **Mit Megan:** Sie wollen dieselbe Bucht als Bühne, ein komisches Bündnis bei Megans Besuch (Pascal hält sich dabei fern). Als sie
  vom Hafenverkauf erfährt, sagt sie zum ersten Mal nichts.
- **Allein:** Morgens auf der Piazza übt sie eine Rede, Kevin hört zu. *“Was that too much?”*
- **Am Ende:** Keiner klatscht, dann fängt Alva langsam an. Ende der Fehde. Der Zeitpunkt ist bewusst nicht an die Festa gebunden.

---

## Was das Dorf zur 5 macht

Einzelne gute Figuren reichen nicht. Das Dorf muss auch ohne Duc leben.

| Baustein | Was es ist | Vorbild |
|---|---|---|
| **Das Dorf lebt ohne dich** | Kleine Szenen im Vorbeigehen, ohne Wahl und ohne Belohnung: Elsa und das Brot, Bà Tư kneift in Wangen, der Strafzettel. Etwa 60 kurze Zeilen | Stardew Valley, Disco Elysium |
| **Der zweite Blick** | Pascals Sätze und Dons Trinken lesen sich beim zweiten Durchlauf völlig anders | Avatar, Fight Club |
| **Der Preis** | Bus und Dach fallen immer weg. Duc entscheidet beim Kassenbuch nur, wer zusätzlich die Rechnung trägt | The Witcher 3 |
| **Das Netz hat Lücken** | Im Genossenschafts-Ende stehen alle Namen auf dem Fischernetz. Dort fehlen sichtbar Namen, je nachdem, wie Duc gespielt hat. Selbst im besten Durchlauf fehlt mindestens einer | Mass Effect 2 |

Das Netz erfüllt Ducs Vorgabe, dass nicht alle für die Genossenschaft sein dürfen, und es ist schon Kanon (Ende 3).

---

## Das Geflecht (Ducs Notizen)

| Paar | Dynamik |
|---|---|
| **Casanova und Bà Tư** | „Auntie Tu“, sie kocht zu viel, sobald Casanova kommt |
| **Casanova und Pfarrer** | neckt ihn wegen des Messweins |
| **Casanova und Mina** | „Keine Rechnungen mehr!“, Mina antwortet immer frech |
| **Alva und Sandru** | er liebt sie seit der Kindheit, sie sieht einen kleinen Bruder |
| **Alva und Pascal** | sie mag ihn, er hat ihr jede Genehmigung besorgt |
| **Alva und Mina** | Wette, wer etwas zuerst weiß |
| **Petru und Bà Tư** | Sie besucht ihn, weil sie Angst hat, er sei einsam, und bringt Fischeintopf. Er schenkt ihr Fische und lächelt nur. Erst hat es gestunken (Fischsauce), jetzt liebt er es. Keine Romanze, Petrus späte Liebe bleibt Holm |
| **Bà Tư und Laetitia** | Kommt Laetitia zurück, fragt sie, wann das Baby kommt |
| **Elsa und Pascal** | ihm unterstellt, „er hält ihr den Rücken frei“, sie kommt nicht zu Casanova durch |
| **Elsa und Sandru** | Kindheitsfreunde, das Gratis-Brot, „Bestechung“, beide lachen |
| **Elsa und Bà Tư** | Elsa gibt immer Trinkgeld, bekommt dafür in die Wangen gekniffen. *“Such a pretty girl. Where is the husband?”* Passt zu ihrer Mutter, die im Dienst anruft |
| **Elsa und Pfarrer** | Sie riecht seine Fahne. *“You're not driving, Father.”* *“I'm walking.”* *“You're not doing that well either.”* |
| **Elsa und Mina** | wie die kleine Schwester, die sie nie hatte (Elsa ist selbst „la piccola“ und hat nur große Brüder). Drückt meist ein Auge zu, aber ab und zu kommt der Strafzettel |
| **Nonna und Pascal** | hält ihn wegen der Setzlinge für gut, versteht durch seinen Brief, warum: schlechtes Gewissen |
| **Nonna und Sandru** | kauft nie sein chemisches Zeug, keine Meinung zu ihm |
| **Nonna und Bà Tư** | Gartenarbeit zusammen. Bà Tư kommt mit Mina auf dem Rücksitz angeflitzt und Elsa fährt sie zurück, oder umgekehrt. Sie lachen über die Jungen und trauern um die, die fort sind. Bà Tư neckt Isabelle, warum sie keinen schönen jungen Mann und keine Kinder hat |
| **Nonna und Pfarrer** | Sie hat keinen Respekt vor ihm, sie ist eine Frau mit klaren Regeln, und er sollte ein Vorbild sein. Er lacht es weg und umarmt sie trotzdem. Sie hasst, dass sie ihm immer vergibt |
| **Nonna und Mina** | Mina bringt jede Woche Pakete und bekommt Kekse und Kuchen |
| **Mina und Isabelle** | sitzen am Berg: „Hätten wir ein anderes Leben, wären wir mutiger?“ |
| **Mina und Pascal** | Monaco-Post als Witz, am Ende „Sign here“ ohne Empfänger |
| **Mina und Sandru** | bringt seine Medizin-Pakete und schweigt |
| **Pfarrer und Kevin** | Krieg um den Turm |

---

## Ablauf

| Tag | Szene | Art |
|---|---|---|
| 2 | `hk_abend`: Pascal, Fass, Applaus, Liste | ändern |
| 3 | Mina kommt mit der Yacht-Post | neu |
| 3–5 | `hy_casanova_konfetti` (Besen) · `g1_casanova_nebel` · `gv_casanova_alva` (misst die Bar aus) | ändern |
| 3–6 | Liegegebühren · Rathaus-Telefon nach `br_satellit_sonntag` · erste Holm-Anrufe | neu, klein |
| 4–6 | Casanova im Morgengrauen · Casanova gegen Megan | neu |
| ab 4 | `kl_casanova_auftrag` (Tür, „Pascal knows everything“) · Minas Briefe. Der Text bleibt ohne Datum | ändern |
| 8–9 | Bà Tư | neu |
| 10 | Sandru und das Logo | neu |
| nach Kloster | Totenfeier der Mönche (zwei Fassungen) · „Did they read them?“ | neu, ernst |
| 12–14 | `kv_ende`: Pfarrer | ändern |
| 14 morgens | Die Messe: das ganze Dorf in einem Raum | neu |
| 15–21 | Ernste Sandru-Szenen, Dorf-Events der Paare oben | neu |
| 21 | Belagerung: Pascal gibt den Weg frei | in Woche 3 planen |
| früh in Akt 3 | Elsa: „Nobody from Ajaccio has called me.“ Sie fährt hin, „All quiet“, dann die Schublade | neu |
| Akt 3 (22–35) | Kiste bei Nonna (Brief, Schlüssel), Schublade, Preis (Bus, Dach), Don vor Pascals Tür, letzte Hilfe, Sandrus Beine, Minas Brief, Rädchen im Finale neben Alon, Epilog | neu |

Festa-Events (`gv_rotes_kleid`, `ab_casanova_flamenco`, `br_ehrenbuerger`) werden **nicht** angefasst.

---

## Ernste Events (Kategorie „ernst“, Entwurf)

Ernste Szene heißt ernste Pose (STIL.md). Keine dieser Szenen ist der schwere Moment des Aktes, sie bleiben leise.

### Sandrus Herkunft (Duc 30.10., zwei Szenen in Woche 3, nach „The Crate“)

**Your Own Name (ernst, Laden nach Feierabend):** Sandru zählt die Kasse, ohne Schild. Duc fragt, woher der Name Alex kommt. Sandru erzählt von
seinem Vater, der dreißig Jahre Tomaten gepflückt hat, damit sein Sohn nie gefragt wird, woher er kommt.
- Sandru: *“Alex doesn't come from anywhere. That's what I like about him.”*
- Duc erzählt seine eigene Fluchtgeschichte (E-067), passend zu „Where You Come From“: Eltern aus Vietnam geflohen, Nachtschichten, und wie er selbst
  lange so tat, als käme er von nirgendwo. Der Chip endet immer gleich: *“You can't run from it. You're carrying it anyway. So carry it with your head up.”*
- Sandru lacht nicht. *“Iskander. My mother is the only one who still says it.”* Setzt `sandru_herkunft`.
- Wer die Szene nicht spielt, verpasst die zweite und den Namen am Ende. Vorher muss Duc Sandru schon begegnet sein, ohne Pflicht.

**Not in the System (wholesome, ein paar Tage später):** Am Ende eines weißen A.V.-Regals steht ein Holzbrett mit handgeschriebenem Schild:
Pfefferminztee, Gazellenhörnchen, Chebakia, Rezepte seiner Mutter. Es ist nicht im System, er kassiert in eine Blechdose.
- Elsa nimmt eines: *“Bread is under review. These are evidence.”* Bà Tư probiert, sagt „too sweet“ und kauft sechs. Mina bringt die Bestellung zur Eden Rise.
- Sandru, zum ersten Mal ohne Lachen davor: *“It's selling. Nobody asked me where I'm from. They asked me for more.”*
- Das ist sein erster kleiner Ungehorsam gegen A.V. und ein Grund mehr, warum Alon ihm später die Beine abschalten kann.

### 1. The Chalkboard (Tag 11–13, Alvas Bar)
Sandru kommt zum ersten Mal in die Bar, im A.V.-Hemd. Das Dorf wird still. Auf Papas Kreidetafel steht neben seinem Namen noch immer
„orangeade“. Er bestellt Grappa. Sie stellt ihm Orangeade hin.
- Sandru: *“I'm thirty, Alva.”* · Alva: *“I know how old you are. I was there.”*
- Sie wischt die Tafel nicht. Sie sagt ihm, er soll das Schild von ihrem Haus abnehmen, und weiß, dass er es nicht kann.
- Chips: Duc setzt sich zu ihm · Duc bleibt bei Alva am Tresen · Duc zahlt beide Getränke und geht.

### 2. The Crate (Tag 15–19, Hinterhof der Bar)
Sandru bringt Alva eine Lieferung selbst, weil die Lieferanten nicht mehr zu ihr kommen. Eine Kiste zu viel. Die Schienen surren, setzen
aus, er fällt. Alva hebt ihn auf, ohne nachzudenken, wie früher, und das ist das Schlimmste daran.
- Sandru, danach, zu Duc: *“You saw nothing.”*
- Chips: *“I saw nothing.”* · Trägt die Kiste selbst rein und sagt kein Wort · *“How long do they work when you pay them?”* (öffnet Rosis Faden)

### 3. Someone Strong (Woche 3, nach Feierabend, Alva allein)
Alva sagt es einmal laut, am leeren Tresen. Mit Alva-Romanze spricht sie zu Duc, sonst wischt sie Gläser und redet fast mit sich selbst.
- Alva: *“I want someone who can pick me up and carry me up those stairs. Isn't that stupid? Thirty-five years old.”*
- Alva: *“And that boy has been climbing those steps on his own for ten years, and I give him orangeade.”*

### 4. Fresh Bread (Woche 3 oder Akt 3, nur mit Romanze, E-060: Gerücht über Mina)
Es hat sich herumgesprochen. Sandru gibt Duc am Morgen das Brot und nimmt kein Geld.
- Sandru: *“She laughs different now. It's good. Don't say anything, please. Just be good to her, and don't be gone by February.”*

### 5. Switched Off (Akt 3, der schwere Moment des Aktes)
Alon schaltet die Beine ab, weil Sandru redet oder einfach, weil er kann. Sandru liegt in seinem Laden unter dem Logo. Alva kommt herüber,
zum ersten Mal in das Haus ihrer Mutter, und trägt ihn über die Straße in ihre Bar und die Treppe hoch.
- Alva: *“You're my little brother, you idiot. I've carried you since you were six.”* · Sandru: *“I know. That's the whole problem.”*
- Danach, nur wenn Duc sich vorher um ihn gekümmert hat, Rosis Ausweg: dieselben Schienen ohne Leine. Er geht wieder, langsamer und auf eigene Rechnung. Kein Paar, aber auf dem
  Namensschild steht jetzt ISKANDER, wenn Duc mit ihm über die Herkunft gesprochen hat, sonst wieder SANDRU.

---

## Offene Prüfungen

- **Story-Sitzung:** erledigt 30.10., kein Widerspruch zu den Fällen, Auflagen stehen bei Pascal. Paar-Events, Stimmen und Sprites hat sie nicht geprüft.
- **Story-Sitzung, E-095:** erledigt 30.10., keine Fall-Auflösung berührt, Korrekturen eingearbeitet.
- **Beim Bau von Akt 3 abgleichen:** Kommission und Anklage mit den Enden; Eden Consulting gehört zur Eden Group, aber Ducs ESG-Arbeit hat nichts mit dem Resort zu tun; das Dach ist nur der warme Abschluss seines Bogens (Duc 01.11.2026, [`duc.md`](../figuren/duc.md)); ESG bleibt Randnotiz, nie Plot.
- **Prüfstein „ein schwerer Moment je Akt“:** Akt 2 = Tag 21, Akt 3 = „Switched Off“. Schublade und Nonna müssen kurz und leise bleiben.
- **Stimmen und Sprites:** 5 neue Figuren, Stimmproben über Voice Design (ohne NPC-Stimmen im ElevenLabs-Konto). Gewählt: Pascal 2, Mina süß 2, Bà Tư 2, Sandru 2, Don Anghjulu portugiesisch 2.
- **Modul nachziehen (Phase 2):** Sandrus Name und Ordner, Beschreibungen von Sandru und Don Anghjulu.
- **Adrien:** Stimme wählen, seine 10 Zeilen neu vertonen, `P["adrien"]` ohne „from Lyon“.
- **Legenden-Familie:** alle fünf eintragen, sonst schlägt `test_legenden` fehl.
- **Character Design:** Elsa-Seite (Pascal als Vorgesetzter, Dumè, Sandru), Alva, Petru, Casanova, Kloster, README-Tabelle nachziehen.
