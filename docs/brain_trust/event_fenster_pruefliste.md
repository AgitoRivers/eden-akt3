# Pruefliste Event-Fenster (Akt 1 -> Akt 2)

> Erzeugt von `werkzeuge/eden_rise/event_fenster_pruefen.py` (29.10.2026). Nur Vorschlag: aendert keine Events.
> Hintergrund: Fast alle Events enden an Tag 6. Ab Tag 7 findet die Engine keinen Kandidaten mehr, Akt 2 bleibt
> ohne Selfies, Abende, Funken, Flirts und Bordraete (Bot-Messung Seed 7, Diagnose im Chat 29.10.).

**Toepfe:** `zeitlos` = kein Akt-1-Wort gefunden -> kurz lesen, dann Fenster auf Tag 21 (`WANN((a, 21), ...)`). `anpassen` = Akt-1-Bezug im Text -> Zeile umschreiben oder bei Tag 6 lassen. `bleibt_akt1` = Pflicht/Prolog oder Strom/Diesel (Mechanik weg, E-082). Die Woerter sind eine Heuristik: "zeitlos" heisst "kein Treffer", nicht "geprueft". Bedingung = das Event haengt zusaetzlich an Vertrauen/Flags.

| Topf | Anzahl |
|---|---|
| zeitlos | 272 |
| anpassen | 38 |
| bleibt_akt1 | 33 |

| Gruppe | zeitlos | anpassen | bleibt_akt1 |
|---|---|---|---|
| Selfie | 85 | 2 | 0 |
| Gag | 46 | 9 | 24 |
| Handy | 59 | 1 | 6 |
| Gag (versus) | 23 | 9 | 1 |
| Bordrat | 17 | 11 | 2 |
| Flirt | 26 | 1 | 0 |
| Abend/Funke | 10 | 2 | 0 |
| Duell | 5 | 1 | 0 |
| Auftritt | 1 | 2 | 0 |

## Anpassen (Akt-1-Bezug im Text)

| ID | Gruppe | Fenster | Wer | Bed. | Titel | Treffer |
|---|---|---|---|---|---|---|
| `ab_lola_klopft` | Abend/Funke | 3–6 | lola | ja | A Knock at the Cabin | Feuer/Blackout frisch (smoke) |
| `fk_rosi_schicht` | Abend/Funke | 3–6 | rosi | ja | Night Shift | Strom/Diesel (generator) |
| `auf_gitarre` | Auftritt | 2–6 |  |  | Guitar on Deck | Strom/Diesel (power) |
| `auf_herkunft` | Auftritt | 3–6 |  |  | Where You Come From | Strom/Diesel (power); festgesetzt (stranded) |
| `br_crew_kasse` | Bordrat | 3–6 | sophia, toto, chiara |  | Yacht Stuff for the Crew Fund? | Ultimatum/Frist (a week) |
| `br_dorfkinder` | Bordrat | 2–6 | lea, chiara, siri |  | The Village Kids | Strom/Diesel (power) |
| `br_ein_tisch` | Bordrat | 2–5 | sophia, chiara, lola |  | One Table for Everyone | festgesetzt (stranded); Ultimatum/Frist (a week) |
| `br_elsas_kontrolle` | Bordrat | 2–6 | sophia, toto, chiara |  | Elsa Comes Tomorrow | Inspektion (comes tomorrow, ferrandi inspects us tomorrow, inspection) |
| `br_investoren_dinner` | Bordrat | 5–5 | sophia, megan, chiara | ja | Megan's Investor Dinner | festgesetzt (stranded) |
| `br_lola_krank` | Bordrat | 2–6 | chiara, rosi, sophia |  | Who Cooks Tomorrow? | Feuer/Blackout frisch (burnt) |
| `br_lolas_notvorrat` | Bordrat | 2–2 | rosi, chiara, toto |  | Lola's Emergency Stash | Strom/Diesel (power) |
| `br_nachtwache` | Bordrat | 2–6 | chiara, rosi, lea |  | Who Keeps Watch? | erste Tage (since we got here) |
| `br_satellit_sonntag` | Bordrat | 3–6 | rosi, lola, jana |  | Forty Minutes | Strom/Diesel (power) |
| `br_singen_ohne_strom` | Bordrat | 2–6 | lola, siri, yasin |  | Singing Without Power | Strom/Diesel (power) |
| `br_yasins_angebot` | Bordrat | 2–5 | sophia, yasin, chiara | ja | Yasin's Offer | festgesetzt (stranded) |
| `du_koch_lola` | Duell | 2–6 | lola |  | Cook-Off: The Galley | Ultimatum/Frist (a week) |
| `fl_rosi_pfand` | Flirt | 2–6 | rosi |  | Loser Does What Winner Says | Strom/Diesel (generator) |
| `bk_rosi_fleck` | Gag | 3–6 | rosi | ja | Grease | Inspektion (inspection); Strom/Diesel (generator) |
| `g1_chiara_inspektion` | Gag | 2–6 | chiara |  | White Glove Inspection | Inspektion (inspection) |
| `g1_chiara_tender` | Gag | 2–3 | chiara |  | Chiara's Tender Test | erste Tage (first day) |
| `g1_drohne` | Gag | 3–4 | megan | ja | Megan's Drone | Inspektion (inspection) |
| `g1_lea_nachttauchen` | Gag | 2–6 | lea | ja | Six Metres | Ultimatum/Frist (a week) |
| `g1_petru_netze` | Gag | 2–6 | petru |  | The Most Mended Net in Corsica | erste Tage (arrived) |
| `g1_pfannkuchen` | Gag | 2–5 | lola |  | Pancake Portraits | Feuer/Blackout frisch (burnt) |
| `g1_reissverschluss` | Gag | 3–6 | rosi | ja | The Zip | Strom/Diesel (generator) |
| `g1_sophia_liest_vor` | Gag | 3–6 | sophia |  | A Page from Sophia's Notebook | festgesetzt (stranded) |
| `gv_dienstplan` | Gag (versus) | 3–6 | chiara, sophia |  | The Rota | Inspektion (inspection); Anhörung (hearing); Ultimatum/Frist (a week) |
| `gv_holm_baer` | Gag (versus) | 2–6 | toto, maxwell |  | One Kilometre, One Shot | Ultimatum/Frist (a week) |
| `gv_kaffee_rosi` | Gag (versus) | 2–6 | siri, rosi |  | Seven O'Clock Coffee | Strom/Diesel (generator, power); erste Tage (day one) |
| `gv_megan_chiara` | Gag (versus) | 5–6 | megan, chiara | ja | Megan's Inspection | Inspektion (inspection); Strom/Diesel (power) |
| `gv_ruhetag` | Gag (versus) | 4–6 | rosi, lea |  | Sunday | Strom/Diesel (batteries, generator) |
| `gv_strip_poker` | Gag (versus) | 4–6 | alva, sophia | ja | Strip Poker for a Canister | Strom/Diesel (diesel) |
| `gv_trinkgeld_topf` | Gag (versus) | 3–6 | lola, rosi |  | The Tip Jar | Strom/Diesel (fuel) |
| `gv_unit01_bild` | Gag (versus) | 2–6 | lea, rosi |  | Portrait of a Lady | Strom/Diesel (generator) |
| `gv_wer_fuehrt` | Gag (versus) | 2–6 | chiara, rosi |  | Who's in Charge Below Deck? | Strom/Diesel (charge) |
| `hy_holm_letzter_anruf` | Handy | 6–6 | holm | ja | “She's Your Boat.” | Anhörung (hearing) |
| `sf_megan_5_hubschrauber` | Selfie | 2–6 | megan | ja | No Conditions | Strom/Diesel (fuel) |
| `sf_rosi_5_werkstatt` | Selfie | 2–6 | rosi | ja | Tactical Surrender | Ultimatum/Frist (a week) |

## Zeitlos (kein Treffer)

| ID | Gruppe | Fenster | Wer | Bed. | Titel | Treffer |
|---|---|---|---|---|---|---|
| `ab_alva_barabend` | Abend/Funke | 4–6 | alva | ja | After Hours at Alva's |  |
| `ab_alva_handy` | Abend/Funke | 5–6 | alva | ja | Alva Calls: “Come Over.” |  |
| `ab_jana_handy` | Abend/Funke | 4–6 | jana | ja | Jana Texts: “Sorry. Again?” |  |
| `ab_jana_nacht` | Abend/Funke | 3–6 | jana | ja | Nobody Has to Know |  |
| `ab_lola_handy` | Abend/Funke | 4–6 | lola | ja | Lola Texts: “You Awake?” |  |
| `ab_megan_nacht` | Abend/Funke | 5–6 | megan | ja | Off the Record |  |
| `fk_chiara_frage` | Abend/Funke | 3–6 | chiara | ja | What Would You Do? |  |
| `fk_lea_schulter` | Abend/Funke | 3–6 | lea | ja | Glow |  |
| `fk_siri_foto` | Abend/Funke | 3–6 | siri | ja | Unposted |  |
| `fk_sophia_wette` | Abend/Funke | 3–6 | sophia | ja | Ten Euros |  |
| `auf_karaoke` | Auftritt | 3–6 |  |  | Karaoke at Alva's |  |
| `br_abschiedsfest` | Bordrat | 6–6 | lola, chiara |  | One Last Night |  |
| `br_drei_minuten` | Bordrat | 2–5 | sophia, chiara, siri | ja | Three Minutes of Water |  |
| `br_festa_auftritt` | Bordrat | 3–4 | rosi, lea, chiara |  | The Crew as a Festa Attraction |  |
| `br_fish_pie` | Bordrat | 2–6 | lola, toto, chiara |  | Marie's Pie |  |
| `br_gaestekabinen` | Bordrat | 2–4 | chiara, sophia, siri |  | The Guest Cabins |  |
| `br_handtuecher` | Bordrat | 3–6 | chiara, jana, siri |  | Jenna |  |
| `br_holm_paket` | Bordrat | 3–6 | siri, lola, chiara |  | A Parcel for the Captain |  |
| `br_jana_tender` | Bordrat | 2–6 | toto, jana, chiara |  | Four Hundred Metres |  |
| `br_megan_kommt` | Bordrat | 4–4 | chiara, rosi | ja | The Boss Is Coming |  |
| `br_nacktbaden` | Bordrat | 2–6 | sophia, lea, chiara |  | Skinny Dipping, with Consequences |  |
| `br_netze_flicken` | Bordrat | 3–6 | lea, rosi | ja | Petru's Price |  |
| `br_petrus_boot` | Bordrat | 2–5 | lea, rosi | ja | Petru's Morning Catch |  |
| `br_rosi_ueberstunden` | Bordrat | 3–6 | sophia, rosi, chiara |  | Rosi Works Too Much |  |
| `br_siri_umzug` | Bordrat | 2–6 | sophia, siri, yasin | ja | Siri Wants to Move |  |
| `br_siris_geburtstag` | Bordrat | 2–6 | lola, sophia, yasin |  | Siri's Birthday |  |
| `br_toto_stand` | Bordrat | 3–6 | toto, lola, chiara |  | A Stamp for Totò |  |
| `br_trinkgeld` | Bordrat | 2–6 | lea, toto |  | An Envelope for Lea |  |
| `du_harpune_chiara` | Duell | 2–6 | chiara |  | Speargun Assembly Against the Clock |  |
| `du_koch_alva` | Duell | 3–6 | alva |  | Cook-Off: Corsica vs. Saigon |  |
| `du_koch_toto` | Duell | 2–6 | toto |  | Cook-Off: Ragù vs. Thịt Kho |  |
| `du_poetry_sophia` | Duell | 3–6 | sophia |  | Poetry Slam: “Ode to Lola's Fridge” |  |
| `du_tiere_lea` | Duell | 2–6 | lea |  | Guess the Animal |  |
| `fl_alva_eis` | Flirt | 2–6 | alva | ja | Ice |  |
| `fl_alva_schritt` | Flirt | 3–6 | alva | ja | One Step |  |
| `fl_alva_tuer` | Flirt | 3–6 | alva | ja | Last Orders |  |
| `fl_chiara_kragen` | Flirt | 2–6 | chiara |  | The Collar |  |
| `fl_chiara_tee` | Flirt | 3–6 | chiara | ja | Two Cups |  |
| `fl_chiara_zehn` | Flirt | 3–6 | chiara | ja | Out of Ten |  |
| `fl_elsa_strafzettel` | Flirt | 2–6 | elsa |  | A Ticket for You |  |
| `fl_jana_knoten` | Flirt | 2–6 | jana |  | Bowline for Two |  |
| `fl_lea_fakt` | Flirt | 2–6 | lea | ja | Fact of the Night |  |
| `fl_lea_neopren` | Flirt | 2–6 | lea |  | Zip Me Up |  |
| `fl_lea_salut` | Flirt | 2–5 | lea |  | At Ease |  |
| `fl_lea_seite41` | Flirt | 3–6 | lea | ja | Page Forty-One |  |
| `fl_lola_bao` | Flirt | 2–6 | lola |  | Hands-On Lesson |  |
| `fl_lola_haengematte` | Flirt | 2–6 | lola | ja | Room for Two. Ish. |  |
| `fl_lola_mehl` | Flirt | 2–6 | lola |  | Flour |  |
| `fl_lola_sonnencreme` | Flirt | 2–6 | lola |  | Backs Are Hard |  |
| `fl_megan_palstek` | Flirt | 3–4 | megan | ja | Behind Your Back |  |
| `fl_megan_privat` | Flirt | 3–5 | megan | ja | Private Number |  |
| `fl_rosi_bandana` | Flirt | 2–6 | rosi |  | The Red Bandana |  |
| `fl_rosi_schicksal` | Flirt | 3–6 | rosi | ja | This Is My Destiny |  |
| `fl_rosi_vespa` | Flirt | 3–6 | rosi | ja | First Ride |  |
| `fl_siri_blick` | Flirt | 2–5 | siri | ja | No Camera |  |
| `fl_siri_date` | Flirt | 3–6 | siri | ja | Too Soon? |  |
| `fl_siri_schulter` | Flirt | 3–6 | siri | ja | Shoulder |  |
| `fl_sophia_blick` | Flirt | 2–6 | sophia |  | Ten Seconds |  |
| `fl_sophia_ungeprobt` | Flirt | 3–6 | sophia | ja | Unscripted |  |
| `ak_chiara_brueckennock` | Gag | 4–6 | chiara | ja | The Bridge Wing at Night |  |
| `ak_chiara_herkunft` | Gag | 3–6 | chiara | ja | Who Believed in You? |  |
| `ak_chiara_sternzettel` | Gag | 3–5 | chiara |  | A Page Full of Stars |  |
| `ak_lola_service` | Gag | 5–6 | megan | ja | “Service!” |  |
| `ak_lola_vorkoster` | Gag | 3–5 | lola | ja | The Taster |  |
| `bk_rosi_tafel` | Gag | 3–6 | rosi | ja | Rosi vs. Officer |  |
| `bk_siri_goldene_stunde` | Gag | 3–6 | siri | ja | Golden Hour, Camera Off |  |
| `bk_siri_stuhl` | Gag | 3–6 | siri | ja | Talking to the Furniture |  |
| `bk_sophia_arm` | Gag | 3–6 | sophia | ja | Darling, Hold Still |  |
| `bk_sophia_buechlein` | Gag | 3–6 | sophia | ja | The Brown Notebook |  |
| `casanova_saufeder` | Gag | 2–6 | casanova | ja | Le Large |  |
| `g1_alva_tim_tams` | Gag | 3–6 | alva | ja | Contraband from Sydney |  |
| `g1_blaskapelle` | Gag | 3–5 | casanova |  | Casanova's Brass Band |  |
| `g1_casanova_nebel` | Gag | 3–5 | casanova |  | The Dress Rehearsal |  |
| `g1_chiara_pause` | Gag | 3–6 | chiara | ja | Chiara Takes a Break |  |
| `g1_cousin_schlauchboot` | Gag | 3–6 | toto | ja | The Cousin Comes at Night |  |
| `g1_elsa_schwimmwesten` | Gag | 3–6 | elsa |  | Elsa and the Life Jackets |  |
| `g1_fiona_muetze` | Gag | 2–6 | toto | ja | Fiona Eats a Cap |  |
| `g1_helikopter` | Gag | 5–5 | megan | ja | Megan Lands |  |
| `g1_holm_kaffee` | Gag | 2–2 | holm | ja | A Coffee with Holm |  |
| `g1_katerfruehstueck` | Gag | 2–6 | lola | ja | Hangover Breakfast |  |
| `g1_kevin_butter` | Gag | 2–4 | lea |  | Lea Feeds the Seagull |  |
| `g1_lola_delfin` | Gag | 2–6 | lola |  | Gerald |  |
| `g1_lola_strandkueche` | Gag | 2–6 | lola |  | The Napkin Kitchen |  |
| `g1_megan_schach` | Gag | 5–6 | megan | ja | Megan Challenges You |  |
| `g1_petru_fisch` | Gag | 3–6 | petru | ja | Petru's Tuna |  |
| `g1_petru_oktopus` | Gag | 3–6 | lola |  | Petru's Lodger |  |
| `g1_siri_pullover` | Gag | 3–6 | siri | ja | Siri in a Jumper |  |
| `g1_siri_tanz` | Gag | 2–6 | siri | ja | Siri Teaches Everyone a Dance |  |
| `g1_sophia_zweitbesetzung` | Gag | 2–6 | sophia |  | The Understudy |  |
| `g1_toto_pizza` | Gag | 2–6 | toto |  | The Pizza War |  |
| `g1_unit01_klonk` | Gag | 2–5 | rosi |  | Rosi vs. Unit-01 |  |
| `g1_unit01_staendchen` | Gag | 3–6 | rosi | ja | A Serenade for Unit-01 |  |
| `g1_yasin_geste` | Gag | 3–5 | yasin | ja | Yasin's Grand Gesture |  |
| `mt_erste` | Gag | 2–4 | maxwell |  | 06:30 with Mr. Maximum |  |
| `mt_nicht_aufhoeren` | Gag | 3–5 | maxwell | ja | Not at “I Can't” |  |
| `mt_zehn` | Gag | 4–6 | jana | ja | Ten Push-Ups |  |
| `mx_chiara_lacht` | Gag | 3–6 | chiara | ja | Chiara Was Watching |  |
| `mx_jana_bewundert` | Gag | 3–6 | jana | ja | Jana Is Watching |  |
| `yk_falle` | Gag | 3–5 | maxwell | ja | Maxwell's Trap |  |
| `yk_hana` | Gag | 3–5 | yamamoto | ja | Hana Asks About the Birds |  |
| `yk_herkunft` | Gag | 3–6 | yamamoto |  | Before the Suits |  |
| `yk_jana_merkt` | Gag | 4–6 | jana | ja | Jana Plays Along |  |
| `yk_liste` | Gag | 5–6 | yamamoto | ja | The Last Item on the List |  |
| `yk_schatten` | Gag | 2–4 | maxwell | ja | Maxwell's Shadow |  |
| `yk_vogel` | Gag | 2–3 | yamamoto |  | The Rare Bird |  |
| `gv_arancini_duell` | Gag (versus) | 3–6 | lola, alva |  | The Arancini Duel |  |
| `gv_armdruecken` | Gag (versus) | 2–6 | rosi, toto |  | Arm Wrestling in the Mess |  |
| `gv_aussenborder` | Gag (versus) | 3–6 | petru, rosi | ja | Petru vs. Rosi |  |
| `gv_casanova_alva` | Gag (versus) | 3–5 | casanova, alva |  | The VIP Lounge |  |
| `gv_casanova_chiara` | Gag (versus) | 3–4 | casanova, chiara |  | The Mayor Wants to Come Aboard |  |
| `gv_chiara_italienisch` | Gag (versus) | 3–6 | chiara, alva | ja | Olivetti |  |
| `gv_einkaufsliste` | Gag (versus) | 2–6 | lola, chiara |  | Lola's Shopping List |  |
| `gv_elsa_kiste` | Gag (versus) | 3–6 | elsa, toto |  | Potatoes That Meow |  |
| `gv_elsa_roman` | Gag (versus) | 2–6 | elsa, toto |  | The Captain's Forbidden Treasure |  |
| `gv_gute_kabine` | Gag (versus) | 3–6 | sophia, lola |  | The Good Cabin |  |
| `gv_keks` | Gag (versus) | 5–6 | lola, megan | ja | Megan and the Cookie |  |
| `gv_kevin_auktion` | Gag (versus) | 3–6 | lea, toto | ja | Who Gets Kevin? |  |
| `gv_megan_sophia` | Gag (versus) | 5–6 | sophia, megan | ja | Sophia Negotiates with Megan |  |
| `gv_musik_nachts` | Gag (versus) | 2–6 | lea, chiara |  | After Midnight |  |
| `gv_ocean_glitter` | Gag (versus) | 2–6 | chiara, lola |  | Order in the Galley |  |
| `gv_oktopus` | Gag (versus) | 2–6 | lea, siri |  | The Octopus |  |
| `gv_quiz` | Gag (versus) | 3–6 | toto, sophia |  | Quiz Night: You're the Host |  |
| `gv_seestueck` | Gag (versus) | 2–6 | lea, sophia |  | A Sky in Four Tries |  |
| `gv_siri_yasin` | Gag (versus) | 3–6 | siri, yasin | ja | Siri vs. Yasin |  |
| `gv_toto_elsa` | Gag (versus) | 3–6 | toto, elsa | ja | Totò Defends His Locker |  |
| `gv_tuersteher` | Gag (versus) | 3–6 | maxwell, yasin |  | After Closing |  |
| `gv_versoehnung` | Gag (versus) | 3–6 | lea, rosi | ja | Peace Cake |  |
| `yk_erwischt` | Gag (versus) | 4–6 | maxwell, yamamoto | ja | Maxwell Catches Him |  |
| `hy_alva_sevilla` | Handy | 3–6 | alva | ja | Thirteen Years |  |
| `hy_alva_tafel` | Handy | 3–6 | alva | ja | Forty Years of Chalk |  |
| `hy_casanova_konfetti` | Handy | 3–5 | casanova | ja | With Ceremony |  |
| `hy_chiara_jonas` | Handy | 3–6 | chiara | ja | Four Stripes |  |
| `hy_cousin_falsch` | Handy | 2–6 | toto |  | Wrong Number from Bastia |  |
| `hy_elsa_segler` | Handy | 3–6 | elsa | ja | A Drifting Sailboat |  |
| `hy_elsa_vorwarnung` | Handy | 3–6 | elsa | ja | Elsa's Warning |  |
| `hy_holm_krankenhaus` | Handy | 2–3 | holm |  | Holm Calls from the Hospital |  |
| `hy_holm_nacht` | Handy | 3–6 | holm | ja | Holm Can't Sleep |  |
| `hy_lea_plankton` | Handy | 2–6 | lea | ja | The Glowing Sea |  |
| `hy_lola_koster` | Handy | 2–6 | lola |  | Taster Wanted |  |
| `hy_lola_tresen` | Handy | 3–6 | alva | ja | Lola Dances on the Bar |  |
| `hy_lola_ziege` | Handy | 2–6 | lola |  | Lola Got Lost |  |
| `hy_megan_anime` | Handy | 3–4 | megan |  | Pollen Season |  |
| `hy_megan_dinner` | Handy | 3–4 | megan | ja | Megan Joins Dinner |  |
| `hy_megan_feuern` | Handy | 3–4 | megan |  | Megan Wants to Fire Someone |  |
| `hy_megan_foto` | Handy | 3–4 | megan |  | The Silver Tray |  |
| `hy_megan_mitternacht` | Handy | 3–4 | megan | ja | Megan at 23:40 |  |
| `hy_megan_rundgang` | Handy | 3–4 | megan |  | A Live Tour for Megan |  |
| `hy_megan_wrong_chat` | Handy | 4–6 | megan | ja | Wrong Chat |  |
| `hy_rosi_foto` | Handy | 3–6 | rosi | ja | Rosi's Photo |  |
| `hy_siri_caption` | Handy | 2–5 | yasin | ja | The Caption |  |
| `hy_siri_ungeschminkt` | Handy | 2–6 | siri | ja | Siri Without a Filter |  |
| `hy_sophia_0213` | Handy | 3–6 | sophia | ja | 02:13 |  |
| `hy_sophia_kaffee` | Handy | 2–6 | sophia |  | Sophia's Hint |  |
| `hy_toto_spind` | Handy | 2–6 | toto |  | A Break-In at Totò's Locker |  |
| `sfn_alva_3` | Handy | 2–6 | alva | ja | Alva: Last Round |  |
| `sfn_alva_4` | Handy | 2–6 | alva | ja | Alva: On the House |  |
| `sfn_alva_5` | Handy | 2–6 | alva | ja | Alva: Nobody's Mine |  |
| `sfn_chiara_3` | Handy | 2–6 | chiara | ja | Chiara: Out of Ten |  |
| `sfn_chiara_4` | Handy | 2–6 | chiara | ja | Chiara: No Number |  |
| `sfn_chiara_5` | Handy | 2–6 | chiara | ja | Chiara: Off the Scale |  |
| `sfn_elsa_3` | Handy | 2–6 | elsa | ja | Elsa: Status Report |  |
| `sfn_elsa_4` | Handy | 2–6 | elsa | ja | Elsa: For the File |  |
| `sfn_elsa_5` | Handy | 2–6 | elsa | ja | Elsa: Case Closed |  |
| `sfn_isabelle_3` | Handy | 2–6 | isabelle | ja | Isabelle: Lavender |  |
| `sfn_isabelle_4` | Handy | 2–6 | isabelle | ja | Isabelle: Patience |  |
| `sfn_isabelle_5` | Handy | 2–6 | isabelle | ja | Isabelle: Confession |  |
| `sfn_jana_3` | Handy | 2–6 | jana | ja | Jana: Wrong Photo |  |
| `sfn_jana_4` | Handy | 2–6 | jana | ja | Jana: Brave |  |
| `sfn_jana_5` | Handy | 2–6 | jana | ja | Jana: Slip Knot |  |
| `sfn_lea_3` | Handy | 2–6 | lea | ja | Lea: For Science |  |
| `sfn_lea_4` | Handy | 2–6 | lea | ja | Lea: Nervous Colours |  |
| `sfn_lea_5` | Handy | 2–6 | lea | ja | Lea: No Fact for This |  |
| `sfn_lola_3` | Handy | 2–6 | lola | ja | Lola: Rate the Chef |  |
| `sfn_lola_4` | Handy | 2–6 | lola | ja | Lola: Not the Bao |  |
| `sfn_lola_5` | Handy | 2–6 | lola | ja | Lola: Too Much |  |
| `sfn_megan_3` | Handy | 2–6 | megan | ja | Megan: Third Quarter |  |
| `sfn_megan_4` | Handy | 2–6 | megan | ja | Megan: Your Move |  |
| `sfn_megan_5` | Handy | 2–6 | megan | ja | Megan: No Conditions |  |
| `sfn_rosi_3` | Handy | 2–6 | rosi | ja | Rosi: Proof Attached |  |
| `sfn_rosi_4` | Handy | 2–6 | rosi | ja | Rosi: Draw |  |
| `sfn_rosi_5` | Handy | 2–6 | rosi | ja | Rosi: Tactical Surrender |  |
| `sfn_siri_3` | Handy | 2–6 | siri | ja | Siri: Not the Camera Voice |  |
| `sfn_siri_4` | Handy | 2–6 | siri | ja | Siri: Just for One |  |
| `sfn_siri_5` | Handy | 2–6 | siri | ja | Siri: No Filter |  |
| `sfn_sophia_3` | Handy | 2–6 | sophia | ja | Sophia: Research Material |  |
| `sfn_sophia_4` | Handy | 2–6 | sophia | ja | Sophia: The Forfeit |  |
| `sfn_sophia_5` | Handy | 2–6 | sophia | ja | Sophia: No Bet Tonight |  |
| `sf_alva_3_bar` | Selfie | 2–6 | alva | ja | Last Round |  |
| `sf_alva_3_tresen` | Selfie | 2–6 | alva | ja | Last Round |  |
| `sf_alva_3_zimmer` | Selfie | 2–6 | alva | ja | Last Round |  |
| `sf_alva_4_bar` | Selfie | 2–6 | alva | ja | On the House |  |
| `sf_alva_4_tresen` | Selfie | 2–6 | alva | ja | On the House |  |
| `sf_alva_4_zimmer` | Selfie | 2–6 | alva | ja | On the House |  |
| `sf_alva_5_bar` | Selfie | 2–6 | alva | ja | Nobody's Mine |  |
| `sf_alva_5_tresen` | Selfie | 2–6 | alva | ja | Nobody's Mine |  |
| `sf_alva_5_zimmer` | Selfie | 2–6 | alva | ja | Nobody's Mine |  |
| `sf_chiara_3_bruecke` | Selfie | 2–6 | chiara | ja | Out of Ten |  |
| `sf_chiara_3_kabine` | Selfie | 2–6 | chiara | ja | Out of Ten |  |
| `sf_chiara_3_nock` | Selfie | 2–6 | chiara | ja | Out of Ten |  |
| `sf_chiara_4_bruecke` | Selfie | 2–6 | chiara | ja | No Number |  |
| `sf_chiara_4_kabine` | Selfie | 2–6 | chiara | ja | No Number |  |
| `sf_chiara_4_nock` | Selfie | 2–6 | chiara | ja | No Number |  |
| `sf_chiara_5_bruecke` | Selfie | 2–6 | chiara | ja | Off the Scale |  |
| `sf_chiara_5_kabine` | Selfie | 2–6 | chiara | ja | Off the Scale |  |
| `sf_chiara_5_nock` | Selfie | 2–6 | chiara | ja | Off the Scale |  |
| `sf_elsa_3_posten` | Selfie | 2–6 | elsa | ja | Status Report |  |
| `sf_elsa_3_verhoerzelle` | Selfie | 2–6 | elsa | ja | Status Report |  |
| `sf_elsa_4_posten` | Selfie | 2–6 | elsa | ja | For the File |  |
| `sf_elsa_4_verhoerzelle` | Selfie | 2–6 | elsa | ja | For the File |  |
| `sf_elsa_5_posten` | Selfie | 2–6 | elsa | ja | Case Closed |  |
| `sf_elsa_5_verhoerzelle` | Selfie | 2–6 | elsa | ja | Case Closed |  |
| `sf_isabelle_3_apotheke` | Selfie | 2–6 | isabelle | ja | Lavender |  |
| `sf_isabelle_3_lavendelbad` | Selfie | 2–6 | isabelle | ja | Lavender |  |
| `sf_isabelle_4_lavendelbad` | Selfie | 2–6 | isabelle | ja | Patience |  |
| `sf_isabelle_4_zelle` | Selfie | 2–6 | isabelle | ja | Patience |  |
| `sf_isabelle_5_lavendelbad` | Selfie | 2–6 | isabelle | ja | Confession |  |
| `sf_isabelle_5_zelle` | Selfie | 2–6 | isabelle | ja | Confession |  |
| `sf_jana_3_dusche` | Selfie | 2–6 | jana | ja | Wrong Photo |  |
| `sf_jana_3_koje` | Selfie | 2–6 | jana | ja | Wrong Photo |  |
| `sf_jana_3_shibari` | Selfie | 2–6 | jana | ja | Wrong Photo |  |
| `sf_jana_4_koje` | Selfie | 2–6 | jana | ja | Brave |  |
| `sf_jana_4_shibari` | Selfie | 2–6 | jana | ja | Brave |  |
| `sf_jana_5_dusche` | Selfie | 2–6 | jana | ja | Slip Knot |  |
| `sf_jana_5_shibari` | Selfie | 2–6 | jana | ja | Slip Knot |  |
| `sf_lea_3_beach` | Selfie | 2–6 | lea | ja | For Science |  |
| `sf_lea_3_garage` | Selfie | 2–6 | lea | ja | For Science |  |
| `sf_lea_3_plankton` | Selfie | 2–6 | lea | ja | For Science |  |
| `sf_lea_4_garage` | Selfie | 2–6 | lea | ja | Nervous Colours |  |
| `sf_lea_4_plankton` | Selfie | 2–6 | lea | ja | Nervous Colours |  |
| `sf_lea_5_beach` | Selfie | 2–6 | lea | ja | No Fact for This |  |
| `sf_lea_5_garage` | Selfie | 2–6 | lea | ja | No Fact for This |  |
| `sf_lea_5_plankton` | Selfie | 2–6 | lea | ja | No Fact for This |  |
| `sf_lola_3_koje` | Selfie | 2–6 | lola | ja | Rate the Chef |  |
| `sf_lola_3_kombuese` | Selfie | 2–6 | lola | ja | Rate the Chef |  |
| `sf_lola_3_sahne` | Selfie | 2–6 | lola | ja | Rate the Chef |  |
| `sf_lola_4_koje` | Selfie | 2–6 | lola | ja | Not the Bao |  |
| `sf_lola_4_kombuese` | Selfie | 2–6 | lola | ja | Not the Bao |  |
| `sf_lola_4_sahne` | Selfie | 2–6 | lola | ja | Not the Bao |  |
| `sf_lola_5_koje` | Selfie | 2–6 | lola | ja | Too Much |  |
| `sf_lola_5_kombuese` | Selfie | 2–6 | lola | ja | Too Much |  |
| `sf_lola_5_sahne` | Selfie | 2–6 | lola | ja | Too Much |  |
| `sf_megan_3_buero` | Selfie | 2–6 | megan | ja | Third Quarter |  |
| `sf_megan_3_hubschrauber` | Selfie | 2–6 | megan | ja | Third Quarter |  |
| `sf_megan_4_buero` | Selfie | 2–6 | megan | ja | Your Move |  |
| `sf_megan_4_hubschrauber` | Selfie | 2–6 | megan | ja | Your Move |  |
| `sf_megan_5_buero` | Selfie | 2–6 | megan | ja | No Conditions |  |
| `sf_rosi_3_generatorraum` | Selfie | 2–6 | rosi | ja | Proof Attached |  |
| `sf_rosi_3_strand` | Selfie | 2–6 | rosi | ja | Proof Attached |  |
| `sf_rosi_3_werkstatt` | Selfie | 2–6 | rosi | ja | Proof Attached |  |
| `sf_rosi_4_generatorraum` | Selfie | 2–6 | rosi | ja | Draw |  |
| `sf_rosi_4_strand` | Selfie | 2–6 | rosi | ja | Draw |  |
| `sf_rosi_4_werkstatt` | Selfie | 2–6 | rosi | ja | Draw |  |
| `sf_rosi_5_generatorraum` | Selfie | 2–6 | rosi | ja | Tactical Surrender |  |
| `sf_rosi_5_strand` | Selfie | 2–6 | rosi | ja | Tactical Surrender |  |
| `sf_siri_3_dessous` | Selfie | 2–6 | siri | ja | Not the Camera Voice |  |
| `sf_siri_3_vip` | Selfie | 2–6 | siri | ja | Not the Camera Voice |  |
| `sf_siri_3_vordeck` | Selfie | 2–6 | siri | ja | Not the Camera Voice |  |
| `sf_siri_4_dessous` | Selfie | 2–6 | siri | ja | Just for One |  |
| `sf_siri_4_vip` | Selfie | 2–6 | siri | ja | Just for One |  |
| `sf_siri_4_vordeck` | Selfie | 2–6 | siri | ja | Just for One |  |
| `sf_siri_5_dessous` | Selfie | 2–6 | siri | ja | No Filter |  |
| `sf_siri_5_vip` | Selfie | 2–6 | siri | ja | No Filter |  |
| `sf_siri_5_vordeck` | Selfie | 2–6 | siri | ja | No Filter |  |
| `sf_sophia_3_achterdeck` | Selfie | 2–6 | sophia | ja | Research Material |  |
| `sf_sophia_3_koje` | Selfie | 2–6 | sophia | ja | Research Material |  |
| `sf_sophia_3_noir` | Selfie | 2–6 | sophia | ja | Research Material |  |
| `sf_sophia_4_achterdeck` | Selfie | 2–6 | sophia | ja | The Forfeit |  |
| `sf_sophia_4_koje` | Selfie | 2–6 | sophia | ja | The Forfeit |  |
| `sf_sophia_4_noir` | Selfie | 2–6 | sophia | ja | The Forfeit |  |
| `sf_sophia_5_achterdeck` | Selfie | 2–6 | sophia | ja | No Bet Tonight |  |
| `sf_sophia_5_koje` | Selfie | 2–6 | sophia | ja | No Bet Tonight |  |
| `sf_sophia_5_noir` | Selfie | 2–6 | sophia | ja | No Bet Tonight |  |

## Bleibt in Akt 1

| ID | Gruppe | Fenster | Wer | Bed. | Titel | Treffer |
|---|---|---|---|---|---|---|
| `br_kevin_nest` | Bordrat | 3–6 | rosi, lea, toto | ja | Kevin Builds a Nest | Strom/Diesel in den Folgen |
| `br_lola_flach` | Bordrat | 2–6 | chiara, rosi, sophia |  | Lola's Down: You Cook for Thirteen | Strom/Diesel in den Folgen |
| `g1_kalte_dusche` | Gag | 2–6 | rosi |  | The Cold Shower | Strom/Diesel in den Folgen |
| `mx_tutorial` | Gag | 2–2 | maxwell |  | Lesson One | Pflicht/Prolog |
| `t0_abschied_flirt` | Gag | 1–1 | megan | ja | Don't Sink My Boat | Pflicht/Prolog |
| `t0_abschied_foermlich` | Gag | 1–1 | megan | ja | Don't Sink My Boat | Pflicht/Prolog |
| `t0_abschied_frech` | Gag | 1–1 | megan | ja | Don't Sink My Boat | Pflicht/Prolog |
| `t0_abschied_herzlich` | Gag | 1–1 | megan | ja | Don't Sink My Boat | Pflicht/Prolog |
| `t0_chiara` | Gag | 1–1 | chiara |  | The Chief Stew | Pflicht/Prolog |
| `t0_holm` | Gag | 1–1 | holm |  | The Captain | Pflicht/Prolog |
| `t0_jana` | Gag | 1–1 | jana | ja | Jana | Pflicht/Prolog |
| `t0_lea` | Gag | 1–1 | lea | ja | Lea | Pflicht/Prolog |
| `t0_limousine` | Gag | 1–1 | maxwell |  | Antibes, 06:10 | Pflicht/Prolog |
| `t0_lola` | Gag | 1–1 | lola |  | The Cook | Pflicht/Prolog |
| `t0_maxwell` | Gag | 1–1 | maxwell |  | Mr. Maximum | Pflicht/Prolog |
| `t0_megan` | Gag | 1–1 | megan |  | Mac | Pflicht/Prolog |
| `t0_rosi` | Gag | 1–1 | rosi |  | The Engineer | Pflicht/Prolog |
| `t0_siri` | Gag | 1–1 | siri | ja | Siri and Yasin | Pflicht/Prolog |
| `t0_sophia` | Gag | 1–1 | sophia | ja | Sophia | Pflicht/Prolog |
| `t0_toto` | Gag | 1–1 | toto |  | The Bosun | Pflicht/Prolog |
| `t0_wahl` | Gag | 1–1 | megan |  | Where to First? | Pflicht/Prolog |
| `t0_wahl2_jana` | Gag | 1–1 | megan | ja | And Then? | Pflicht/Prolog |
| `t0_wahl2_moore` | Gag | 1–1 | megan | ja | And Then? | Pflicht/Prolog |
| `t0_wahl2_siri` | Gag | 1–1 | megan | ja | And Then? | Pflicht/Prolog |
| `t0_wahl2_yamamoto` | Gag | 1–1 | megan | ja | And Then? | Pflicht/Prolog |
| `t0_yamamoto` | Gag | 1–1 | yamamoto | ja | Yamamoto-san | Pflicht/Prolog |
| `gv_elsa_alva` | Gag (versus) | 3–6 | elsa, alva |  | Diesel Under the Bar | Strom/Diesel in den Folgen |
| `hy_alva_diesel_tanz` | Handy | 3–6 | alva | ja | A Canister for a Dance | Strom/Diesel in den Folgen |
| `mg_tag2` | Handy | 2–2 | megan |  | Voice Message from Megan (1) | Pflicht/Prolog |
| `mg_tag3` | Handy | 3–3 | megan |  | Voice Message from Megan (2) | Pflicht/Prolog |
| `mg_tag4` | Handy | 4–4 | megan |  | Voice Message from Megan (3) | Pflicht/Prolog |
| `mg_tag5` | Handy | 5–5 | megan |  | Voice Message from Megan (4) | Pflicht/Prolog |
| `mg_tag6` | Handy | 6–6 | megan | ja | Voice Message from Megan (5) | Pflicht/Prolog |
