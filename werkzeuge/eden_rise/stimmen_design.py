# -*- coding: utf-8 -*-
r"""Neue Figurenstimmen fuer das Ortskapitel Berge per ElevenLabs Voice Design (Duc 27.10.2026).

    python werkzeuge\eden_rise\stimmen_design.py            entwirft je Figur 3 Proben (kostet ElevenLabs-Credits)
    python werkzeuge\eden_rise\stimmen_design.py --messen   nur messen und Abnahme-Seite neu bauen

Regel (Duc): Die Probe spricht die Figur in ihrer Muttersprache - das bringt den Akzent mit. Chatterbox klont daraus und
spricht die englischen Spielzeilen mit diesem Akzent. Ablage: docs\abnahme\stimmen_berge\<pid>_<n>.mp3, gemessen
(Rauschband 8-10 kHz, Pegel, Dauer), die beste wird als 24 kHz-Mono-Referenz nach X:\AI\Chatterbox\voices\<Name> - <SPR>.wav
gelegt. Der API-Schluessel kommt aus X:\AI\VoiceStudio\voice-studio.json und wird nie ausgegeben."""
import base64, json, os, re, subprocess, sys, urllib.request

EDEN = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ZIEL = os.path.join(EDEN, "docs", "abnahme", sys.argv[sys.argv.index("--ziel") + 1] if "--ziel" in sys.argv else
                    "stimmen_berge")
VOICES = r"X:\AI\Chatterbox\voices"
API = "https://api.elevenlabs.io/v1/text-to-voice/"

BIBI_PROBE = ("Ha ha ha ha! Sorry. I do that. Oh, look at him! Look at his little face! Come here, you, come here, it's okay. He is "
              "twelve kilos of pure bad decisions, and I love him already. You found him, and you didn't hurt him. So, thank you. "
              "Really. Now listen to me: there are fourteen more out there, and I have one bowl, half a roof, and a very good plan. "
              "Okay. It's not a very good plan. But you're going to help me anyway, aren't you? Yes. I can see it. Sit. There's coffee.")
ROLLEN = {
    # Alon Varenne (Duc 02.11.2026): Kanadier mit franzoesischen Wurzeln, Muttersprache Englisch, darum englische Probe
    "alon": ("Alon Varenne", "ENG",
             "A Canadian man in his early fifties from Toronto, a tech billionaire. A smooth, warm, friendly baritone with a "
             "clear standard Canadian English accent, very confident, a little too fast when he gets excited. He smiles while "
             "he talks and laughs lightly at his own jokes. Never loud, never angry. Recorded very close to the microphone in a "
             "dry vocal booth, intimate and present, no room echo, no reverb, no background noise.",
             "Okay. Okay, everybody, sit down, sit down. Thank you. So. Here is a number I love. Forty. Forty minutes. "
             "That is how long it took our team to reach a small village that most of you have never heard of. "
             "Forty minutes, and nobody died. Nobody. Think about that. Violence is not human nature, guys. It's a bug. "
             "And bugs, we patch. Ha. I know, I know, I say that every year. But this year, we shipped it."),
    "mrwhite": ("Mr. White", "ENG",
                "A silver-haired Scandinavian man in his fifties, the chief of a private security force. A quiet, smooth, "
                "cultured baritone, courteous and completely cold, never raises his voice and is never in a hurry. Native "
                "Swedish speaker. Close microphone, clean studio recording, no background noise.",
                "God kväll. Nej, ni behöver inte resa er. Jag ber om ursäkt för den sena timmen, och för mina medarbetare, "
                "de är inte så väluppfostrade som jag skulle önska. Ni har något som tillhör min arbetsgivare. Det är "
                "ingen fara. Jag är en mycket tålmodig man, och det brukar sluta på samma sätt. Så vackert ni har det här. "
                "Rosmarin, eller hur? Det vore synd om något hände den."),
    "laetitia": ("Laetitia Albertini", "FR",
                 "A 24-year-old Corsican woman with a low, slightly husky voice, guarded, sharp and proud, warm only "
                 "underneath. Native French speaker from Corsica with a southern Corsican lilt. Close microphone, clean "
                 "studio recording, no background noise.",
                 "Je ne suis plus une enfant. Mon père croit encore que je vais rentrer à la maison dès que le vent tourne. "
                 "Mais je ne rentrerai pas, pas cette fois. Là-haut, il y a quelqu'un qui a besoin de moi, et personne ne "
                 "va me le prendre. Ni la Légion, ni ces hommes en costume noir. Alors baissez votre arme. Ou partez."),
    "adrien": ("Adrien Morel", "FR",
               "A 28-year-old French soldier, wounded and exhausted, a soft-spoken but tense baritone that tries to stay "
               "calm. Native French speaker from Lyon. Close microphone, clean studio recording, no background noise.",
               "Caporal Adrien Morel, Légion étrangère. Enfin, je l'étais. On nous a envoyés garder une propriété dans la "
               "montagne, soi-disant pour la sécurité. J'ai vu des cages. Des animaux avec des colliers qui clignotent. "
               "Ils les testaient, vous comprenez ? Alors j'ai pris des photos, et j'ai couru. Je cours depuis neuf jours."),
    "wolff": ("Kaspar Wolff", "DE",
              "A German Foreign Legion sergeant in his late forties, a gravelly, firm bass voice, dry, precise and "
              "unhurried, with a hidden soft spot. Native German speaker. Close microphone, clean studio recording, no "
              "background noise.",
              "Sergent Kaspar Wolff, Fremdenlegion. Ich suche einen Deserteur, Caporal Adrien Morel, verwundet, "
              "vermutlich irgendwo in diesen Bergen. Die Dienstvorschrift ist da sehr eindeutig: Wer ihn versteckt, macht "
              "sich mitschuldig. Ich frage Sie also nur einmal, und ich frage höflich. Haben Sie ihn gesehen? Moment. Ist "
              "das eine Ziege? Im Einsatz? Darf ich?"),
    "ghjuvan": ("Ghjuvan Santucci", "IT",
                "A weathered Corsican shepherd in his late fifties, a deep, rough, tired voice on the edge of despair, "
                "speaking Italian with a strong rural Corsican accent. Close microphone, clean studio recording, no "
                "background noise.",
                "Cinque generazioni, signore. Mio nonno, mio padre, e adesso io. Questa terra non l'abbiamo mai venduta. "
                "Ma la banca non aspetta, e quella bestia mi prende una pecora ogni notte. Me ne sono rimaste quaranta. "
                "Quaranta! Se ne perdo altre dieci, firmo. Firmo per quegli uomini in nero. La prego. Non mi è rimasto "
                "più niente."),
    "dumenica": ("Dumenica", "IT",
                 "An old Corsican woman in her late seventies, a thin, cracked but steady voice, slow and quiet, a little "
                 "eerie, speaking Italian with a heavy rural Corsican accent. Close microphone, clean studio recording, "
                 "no background noise.",
                 "Io caccio quando dormo, figliolo. Tutte le notti. E la bestia che uccido nel sogno ha sempre una faccia. "
                 "Stanotte aveva la faccia della figlia di Petru. In paese nessuno mi guarda più negli occhi. Ma io l'ho "
                 "già visto succedere. Ho sognato mio figlio, vent'anni fa. E una settimana dopo, la montagna non me l'ha "
                 "più restituito."),
    # Strand-Grotte, Akt 2 Woche 2 (Duc 27.10.2026, ereignisse_grotte.py)
    "gennaro": ("Gennaro Esposito", "IT",
                "A Corsican-Italian man in his early forties from Bastia, a fast, nervous, charming tenor that cracks "
                "when he is scared, speaking Italian with a southern accent. Close microphone, clean studio recording, "
                "no background noise.",
                "Lo so, lo so, ho fatto un casino. Un altro. Mio cugino mi ammazza, se esco vivo da qui. Ma ascoltami: "
                "quella cassa non e mia, io la dovevo solo portare. Tre notti, mille euro, niente domande. Poi quelli di "
                "Bastia hanno detto che il debito era raddoppiato. Raddoppiato! E io ho una figlia, capisci? Ha sette anni."),
    "matteu": ("Matteu Pinelli", "IT",
               "A 19-year-old Corsican fisherman's son, a young, soft, earnest voice, shy and stubborn at once, speaking "
               "Italian with a rural Corsican accent. Close microphone, clean studio recording, no background noise.",
               "Mio fratello nuotava meglio di tutti, in paese. Meglio di me. Dicono che e annegato qui sotto, l'anno "
               "scorso. Io non ci credo. Lui conosceva ogni corrente di questa grotta. Per questo mi immergo per loro: "
               "mi hanno promesso che un giorno mi diranno dov'e. Lo voglio solo riportare a casa. A nostra madre."),
    "chloe": ("Chloe Marchal", "FR",
              "A 30-year-old French treasure hunter, a bright, quick, slightly breathless alto that turns desperate, "
              "native French speaker from Marseille. Close microphone, clean studio recording, no background noise.",
              "Aidez-moi, je vous en supplie! Le plafond s'est effondre, Bastien est coince sous les pierres. Sa jambe, "
              "je ne peux pas la degager toute seule. La maree remonte, dans vingt minutes tout sera sous l'eau. Je vous "
              "donnerai tout, nos cartes, nos notes, tout ce que vous voulez. Mais ne le laissez pas ici."),
    "riscossore": ("U Riscossore", "IT",
                   "A Corsican debt collector in his sixties, a slow, low, smoky, very calm bass voice, polite and "
                   "terrifying, speaking Italian with a Bastia accent. Close microphone, clean studio recording, no "
                   "background noise.",
                   "Si sieda, signore. Non ho fretta. La marea, invece, ha sempre fretta. Il ragazzo mi deve dei soldi, e "
                   "io sono un uomo paziente. Ma la pazienza, vede, e come il vino buono: quando finisce, finisce. Allora "
                   "parliamo da persone civili. Lei mi lascia la cassa, e io le lascio il cugino. Quasi intero."),
    # Taschendiebe am Hafen (Duc 29.10.2026: "nervige Maennerstimme", je eine fuer die zwei Sprite-Varianten) -
    # die Brueder Ricci aus Ajaccio, Zufallskampf vor Alvas Bar und Petrus Werkstatt (kern/taschendieb.py)
    "fabbiu": ("Fabbiu Ricci", "FR",
               "A cocky 19-year-old Corsican street kid, a thin, nasal, whiny tenor that cracks into a smug giggle, fast "
               "and mocking, the kind of voice that makes you want to punch him. Native French speaker from Ajaccio "
               "with a Corsican lilt. Close microphone, clean studio recording, no background noise.",
               "Oh là là, regardez-moi ça, le touriste en veste de cuir! Tu cherches ton portefeuille, mon grand? Il est "
               "là, dans ma poche. Viens le chercher, si t'es un homme. Non? Ah, t'as peur de te salir les mains? "
               "Hé hé hé. Mon frère dit que t'es lent. Moi je dis que t'es très, très lent."),
    "santu": ("Santu Ricci", "FR",
              "A 22-year-old Corsican petty thief, a sly, sing-song, sneering voice, slightly hoarse and drawling, lazy "
              "and condescending, always grinning while he talks. Native French speaker from Ajaccio with a Corsican "
              "accent. Close microphone, clean studio recording, no background noise.",
              "Tranquille, tranquille, on discute, c'est tout. Joli sac. Vraiment joli. Ce serait dommage qu'il "
              "disparaisse, non? Allez, frappe, je t'attends. Ma grand-mère frappe plus fort que toi, et elle a "
              "quatre-vingt-dix ans. Tu sais quoi? Garde tes sous. Je reviendrai demain. Et après-demain. Et le jour "
              "d'après."),
    # Matte, der Cousin der Riccis (Duc 29.10.2026: "tiefes Bass") - Sprite ThiefAlpha, der Schlaeger der Bande
    "matte": ("Mattè Ricci", "FR",
              "A huge Corsican bruiser in his mid-thirties, a very deep, slow, rumbling bass voice, few words, flat and "
              "heavy, almost bored, quietly menacing with a dry hint of humour. Native French speaker from Ajaccio with a "
              "Corsican accent. Close microphone, clean studio recording, no background noise.",
              "Le sac. Maintenant. Non, je ne crie pas. Je ne crie jamais. Mes cousins parlent, moi je porte les "
              "choses. Les sacs, les caisses, les gens. Tu veux te battre? D'accord. Mais après, tu ne te plains pas. "
              "Merci. Reviens quand tu veux."),
    # Flut-Nacht (Duc 28.10.2026): "wirklich ethereal, soll sich echt besonders anhoeren", walisischer Akzent
    "sirene": ("The Siren", "ENG",
               "An ethereal, otherworldly woman's voice, an ancient sea spirit who sounds young and very old at once: "
               "soft, breathy, airy and luminous, slow and melodic, almost singing as she speaks, hypnotic and a little "
               "sad, with a gentle lilting Welsh accent from the Welsh coast. Close microphone, clean dry studio "
               "recording, no reverb, no background noise, no music.",
               "Shh. Don't be frightened, cariad. The sea remembers everyone who sleeps in her, and so do I. Every "
               "sailor who ever sang to me, and the ones who only listened. You came down at high tide, on purpose. "
               "That was brave. Or foolish, isn't it? Sit with me a while, then. And I'll tell you where the old boat "
               "lies."),
    # Ligeia (Duc 29.10.2026: "Waliser ist raus", die Sirene ist Ligeia aus der Odyssee): Probe auf Griechisch bringt den
    # Akzent mit, dazu eine neapolitanisch-italienische Gegenprobe. python stimmen_design.py ligeia_gr1 ligeia_gr2
    # ligeia_it --ziel stimmen_ligeia
    "ligeia_gr1": ("Ligeia", "GR",
                   "An ethereal, otherworldly young woman's voice, a Greek sea spirit who sounds young and three thousand "
                   "years old at once: bright, clear and luminous, soft and breathy, slow and melodic, almost singing as "
                   "she speaks, teasing and a little sad. Native Greek speaker. Close microphone, clean dry studio "
                   "recording, no reverb, no background noise, no music.",
                   "Σσς. Μη φοβάσαι, ναύτη μου. Η θάλασσα θυμάται όλους όσους κοιμούνται μέσα της, κι εγώ το ίδιο. "
                   "Κάθε ναύτη που μου τραγούδησε ποτέ, κι εκείνους που μόνο άκουσαν. Κατέβηκες με την παλίρροια, "
                   "επίτηδες. Ήταν γενναίο. Ή ανόητο. Κάθισε λίγο μαζί μου, λοιπόν. Κάποτε ήμασταν τρεις. Τώρα έμεινα "
                   "μόνο εγώ."),
    "ligeia_gr2": ("Ligeia", "GR",
                   "An ethereal, ancient woman's voice, a Greek sea spirit, lower and darker, warm and husky, slow and "
                   "hypnotic, with a melodic rise and fall like a lullaby, amused, lonely and very tired underneath. "
                   "Native Greek speaker. Close microphone, clean dry studio recording, no reverb, no background noise, "
                   "no music.",
                   "Σσς. Μη φοβάσαι, ναύτη μου. Η θάλασσα θυμάται όλους όσους κοιμούνται μέσα της, κι εγώ το ίδιο. "
                   "Κάθε ναύτη που μου τραγούδησε ποτέ, κι εκείνους που μόνο άκουσαν. Κατέβηκες με την παλίρροια, "
                   "επίτηδες. Ήταν γενναίο. Ή ανόητο. Κάθισε λίγο μαζί μου, λοιπόν. Κάποτε ήμασταν τρεις. Τώρα έμεινα "
                   "μόνο εγώ."),
    "ligeia_it": ("Ligeia", "IT",
                  "An ethereal, otherworldly woman's voice, an ancient sea spirit from the bay of Naples: soft, breathy "
                  "and luminous, slow and melodic, almost singing as she speaks, with a gentle Neapolitan lilt, teasing "
                  "and a little sad. Native Italian speaker from Naples. Close microphone, clean dry studio recording, "
                  "no reverb, no background noise, no music.",
                  "Shh. Non avere paura, marinaio. Il mare si ricorda di tutti quelli che dormono dentro di lui, e anch'io. "
                  "Ogni marinaio che mi ha cantato una canzone, e quelli che hanno solo ascoltato. Sei sceso con l'alta "
                  "marea, apposta. Coraggioso. O sciocco. Siediti un po' con me, allora. Una volta eravamo in tre. "
                  "Adesso sono rimasta solo io."),
    # Red Trio, Macchia-Nebenquest (Duc 29.10.2026): Danzel Franzoesisch mit japanischem Akzent, Bibi deutsch-
    # franzoesisch, Charly trocken (--ziel stimmen_trio)
    "danzel": ("Danzel", "FR",
               "A 30-year-old Japanese-French man, a light, slightly nasal tenor that tries to sound like a cool, deep "
               "anime villain and keeps cracking upward when he gets scared. Fast, theatrical, over-dramatic. Speaks "
               "French fluently with a noticeable Japanese accent. Close microphone, clean dry studio recording, no "
               "reverb, no background noise, no music.",
               "Halte-là ! Je suis Danzel, la Lame Rouge d'A.V. Estates, et tu as volé ma plaque d'acier. Tu vas le "
               "payer, mon ami. Très cher. Bibi, Charly, à l'attaque ! ... Attends. Tu as entendu ça ? Dans les buissons. "
               "C'est un sanglier ? Non, non, non. Écoute, entre nous, moi, je veux juste ouvrir une petite épicerie "
               "asiatique. Du tofu, de la coriandre, des mangas au fond. C'est tout. Alors rends-moi la plaque, s'il te "
               "plaît. Mr. White ne pardonne jamais."),
    "bibi": ("Bibi", "FR",
             "A 25-year-old German-French woman, a bubbly, energetic, raspy voice, loud and bright with a scratchy "
             "edge, laughs a lot and rehearses an over-the-top villain laugh. Speaks French as a native with a light "
             "German touch on some consonants. Close microphone, clean dry studio recording, no reverb, no background "
             "noise, no music.",
             "Mwahaha ! Non, attends, je recommence. MWA-HA-HA ! Voilà, c'est mieux. Écoute-moi bien, toi : cette fois, "
             "on est vraiment dangereux. J'ai trois grenades, deux fumigènes et un plan. Enfin, Danzel a un plan. Plus "
             "ou moins. Charly, tu as vu ma pose ? Elle était géniale, non ? Oh ! Oh, regarde, un petit sanglier ! Il "
             "est trop mignon ! Viens là, mon chou, viens. Non, Bibi, concentre-toi. On est des méchants. Des vrais "
             "méchants."),
    # Bibi neu (Duc 01.11.2026): energisch, rauchig, sinnlich, franzoesisch, Anfang 30, nie genervt. Die Probe spricht bewusst Englisch mit
    # Akzent: aus der franzoesischen Vorlage rutschten ganze Saetze in die englischen Aufnahmen. --ziel stimmen_bibi_neu
    "bibi_warm": ("Bibi", "ENG",
                  "A French woman in her early thirties with a warm, raspy, sensual voice, full of energy and always close to "
                  "laughing, playful and delighted, never annoyed, never bored. Speaks English with a clear French accent. Close "
                  "microphone, clean dry studio recording, no reverb, no background noise, no music.",
                  BIBI_PROBE),
    "bibi_rauch": ("Bibi", "ENG",
                   "A French woman in her early thirties with a low, smoky, husky voice with a real rasp, sensual and confident, "
                   "quick and lively, with a big easy smile in every sentence, never annoyed. Speaks English with a strong Parisian "
                   "French accent. Close microphone, clean dry studio recording, no reverb, no background noise, no music.",
                   BIBI_PROBE),
    # Runde 2 (Duc 01.11.2026): Rauch 2 gefiel am besten, darum nah an ihr bleiben: gleiche Beschreibung, schneller, frecher
    "bibi_r2_gleich": ("Bibi", "ENG",
                       "A French woman in her early thirties with a low, smoky, husky voice with a real rasp, sensual and confident, "
                       "quick and lively, with a big easy smile in every sentence, never annoyed. Speaks English with a strong Parisian "
                       "French accent. Close microphone, clean dry studio recording, no reverb, no background noise, no music.",
                       BIBI_PROBE),
    "bibi_r2_schnell": ("Bibi", "ENG",
                        "A French woman in her early thirties with a low, smoky voice with a real rasp, talking fast and full of energy, "
                        "tumbling from one thought to the next, breathless with delight, sensual without trying, never annoyed. Speaks "
                        "English with a strong Parisian French accent. Close microphone, clean dry studio recording, no reverb, no "
                        "background noise, no music.",
                        BIBI_PROBE),
    "bibi_r2_frech": ("Bibi", "ENG",
                      "A French woman in her early thirties with a deep, raspy, smoker's voice, sensual and cheeky, teasing and warm, "
                      "with a real throaty laugh that breaks through her words, quick and lively, never annoyed. Speaks English with a "
                      "strong Parisian French accent. Close microphone, clean dry studio recording, no reverb, no background noise, no music.",
                      BIBI_PROBE),
    "bibi_hell": ("Bibi", "ENG",
                  "A French woman in her early thirties with a bright, energetic voice with a scratchy, raspy edge, bubbly and "
                  "fast, warm and flirty, laughing easily and full of joy, never tired or annoyed. Speaks English with a light "
                  "southern French accent. Close microphone, clean dry studio recording, no reverb, no background noise, no music.",
                  BIBI_PROBE),
    "charly": ("Charly", "FR",
               "A 26-year-old French woman, a low, calm, completely monotone voice, dry and sleepy, almost no emphasis, "
               "every sentence sounds like a quiet sigh, deadpan humour. Native French speaker. Close microphone, clean "
               "dry studio recording, no reverb, no background noise, no music.",
               "Le plan de Danzel. Sur dix. Je dirais trois. Peut-être deux et demi, parce qu'il a oublié la carte. "
               "Encore. Non, je ne cours pas. Je ne cours jamais. J'ai des chips, j'ai mon taser, et j'ai sommeil. Si je "
               "suis ici, c'est pour Bibi. Uniquement pour Bibi. Bon. On peut en finir ? Il fait chaud, et Mr. White "
               "n'attend pas. Lui non plus, d'ailleurs. Personne n'attend jamais."),
    # Dorf-Figuren (Duc 30.10.2026, docs/wiki/welt/dorf_figuren.md): --ziel stimmen_dorf
    "pascal": ("Pascal Leca", "FR",
               "A 52-year-old Corsican man, a warm, soft, slightly tired baritone, friendly and unhurried, always a small "
               "smile in the voice, modest and reassuring, the man everybody trusts. Native French speaker from Corsica with "
               "a gentle southern lilt. Close microphone, clean dry studio recording, no reverb, no background noise.",
               "Ne vous inquiétez pas, je m'en occupe. La liste des dégâts est déjà chez le lieutenant, et votre capitaine "
               "a lancé un yaourt sur un médecin ce matin, ce qui est plutôt bon signe. Madame le maire vous attend, mais "
               "prenez d'abord un café, vous avez une sale tête, si je peux me permettre. Moi ? Oh, moi, je ne fais rien. Je "
               "tiens juste le balai. Laissez-moi ça."),
    "mina": ("Mina Orsoni", "FR",
             "A 24-year-old Corsican woman, a bright, fast, cheeky voice, always a bit out of breath and about to laugh, "
             "lively and warm, teasing everyone. Native French speaker from Corsica with a light southern lilt. Close "
             "microphone, clean dry studio recording, no reverb, no background noise.",
             "Trois factures et une lettre d'amour pour vous ! Non, je ne les lis pas. Je le sais, c'est tout. Madame le "
             "maire, ne criez pas, ce n'est pas moi qui écris les factures, je les apporte seulement ! Et Bruxelles vous dit "
             "bonjour. Quoi, encore une amende ? Non, non, non, pas encore ! Elsa, je roulais à peine à quarante, je te "
             "jure ! Allez, je file, il y a des gâteaux qui m'attendent au couvent."),
    # Duc 30.10.2026: Mina zu aehnlich wie die anderen jungen Frauen, "etwas suesser und quirliger"; Gegenprobe mit
    # marokkanischen Wurzeln (python stimmen_design.py mina_suess mina_ma --ziel stimmen_dorf)
    "mina_suess": ("Mina Orsoni", "FR",
                   "A 24-year-old Corsican woman with a high, sweet, bubbly little voice, sing-song and full of giggles, "
                   "chirpy and quick like a happy bird, cute and innocent rather than sexy, never husky, never low. Native "
                   "French speaker from Corsica. Close microphone, clean dry studio recording, no reverb, no background "
                   "noise.",
                   "Trois factures et une lettre d'amour pour vous ! Non, je ne les lis pas. Je le sais, c'est tout. Hi hi ! "
                   "Madame le maire, ne criez pas, ce n'est pas moi qui écris les factures, je les apporte seulement ! Et "
                   "Bruxelles vous dit bonjour. Quoi, encore une amende ? Non, non, non, pas encore ! Elsa, je roulais à peine "
                   "à quarante, je te jure ! Allez, je file, il y a des gâteaux qui m'attendent au couvent."),
    "mina_ma": ("Mina", "FR",
                "A 24-year-old woman born in Corsica to Moroccan parents, a high, sweet, bubbly voice, sing-song and full "
                "of giggles, chirpy and quick, cute rather than sexy, never husky, never low. Native French speaker with a "
                "light, warm Moroccan lilt. Close microphone, clean dry studio recording, no reverb, no background noise.",
                "Trois factures et une lettre d'amour pour vous ! Non, je ne les lis pas. Je le sais, c'est tout. Hi hi ! "
                "Madame le maire, ne criez pas, ce n'est pas moi qui écris les factures, je les apporte seulement ! Et "
                "Bruxelles vous dit bonjour. Quoi, encore une amende ? Non, non, non, pas encore ! Elsa, je roulais à peine "
                "à quarante, je te jure ! Allez, je file, il y a des gâteaux qui m'attendent au couvent."),
    # Duc 30.10.2026: Don Anghjulu ist Portugiese (Padre Angelo), Probe auf europaeischem Portugiesisch
    "anghjulu_pt": ("Don Anghjulu", "PT",
                    "A Portuguese priest around sixty, a big, warm, wine-rounded, slightly slurred baritone, laughing easily, "
                    "lazy and kind, suddenly clear and quiet when it matters. Native European Portuguese speaker. Close "
                    "microphone, clean dry studio recording, no reverb, no background noise.",
                    "Meu filho, entra, entra. Deus vê tudo, mas ainda não viu esta garrafa. Há catorze anos que luto com aquela "
                    "gaivota, catorze! O Senhor providencia, e eu nunca pergunto de que conta. Corta as cartas, vá. Não, espera. "
                    "Senta-te um momento. Pareço bêbado, eu sei. Mas ouve-me bem, porque só digo isto uma vez."),
    # Duc 30.10.2026: Adrien ist Inder (Geburtsname Arjun), neue Stimme, Probe auf Hindi bringt den Akzent mit
    "adrien_in": ("Adrien Morel", "HI",
                  "A handsome 28-year-old Indian soldier of the French Foreign Legion, a warm, soft-spoken, smooth baritone, "
                  "wounded and exhausted but trying to stay calm, with a quiet dry humour when it hurts. Native Hindi speaker "
                  "from India. Close microphone, clean dry studio recording, no reverb, no background noise.",
                  "मेरा असली नाम यहाँ कोई नहीं जानता। लीजन ने मुझे नया नाम दिया, एड्रियन मोरेल। हमें पहाड़ों में एक जागीर की "
                  "रखवाली के लिए भेजा गया था, सुरक्षा के नाम पर। मैंने पिंजरे देखे। जानवरों के गले में चमकते हुए पट्टे। वे उन पर "
                  "परीक्षण कर रहे थे, समझे आप? इसलिए मैंने तस्वीरें लीं और भाग निकला। नौ दिन से भाग रहा हूँ। चोट लगी है, पर ठीक "
                  "हूँ। बस हँसने पर थोड़ा दर्द होता है।"),
    "batu": ("Ba Tu", "VI",
             "A Vietnamese woman in her mid-seventies from Saigon, a small, clear, firm and dry voice, a little raspy, "
             "bossy and warm at once, quick with a scolding, never sentimental. Native Vietnamese speaker with a southern "
             "Saigon accent. Close microphone, clean dry studio recording, no reverb, no background noise.",
             "Ăn đi con. Sao mà ốm dữ vậy? Mẹ con không cho con ăn hả? Ngồi xuống đi, ăn trước rồi nói sau. Mấy người ở đây "
             "ăn uống gì kỳ cục quá, phô mai với phô mai. Tui nấu dư rồi, lúc nào tui cũng nấu dư hết. Mà con đã gọi điện "
             "cho mẹ chưa? Chưa hả? Trời đất ơi. Ăn đi, rồi gọi."),
    "sandru": ("Sandru Amrani", "FR",
               "A 30-year-old Corsican man, a light, polite, quick tenor, too eager to please, with a nervous little laugh "
               "before his sentences, turning quiet and honest when he is tired. Native French speaker from Corsica with a "
               "southern lilt. Close microphone, clean dry studio recording, no reverb, no background noise.",
               "Bienvenue, bienvenue ! Un café offert pour l'ouverture, ha, c'est la maison qui régale. Non, ne regardez pas "
               "le badge, ici ils m'appellent Alex, c'est plus simple pour le système. Ça va, oui, ça va très bien. Vous, "
               "vous repartez dans trois semaines, et c'est normal. Moi, j'ai besoin de mes jambes en février. Pardon. Je "
               "vous mets un sac ?"),
    # Neue Figuren der Belagerung (Duc 01.11.2026)
    "minicu": ("Minicu", "IT",
               "A gentle giant of 34, a Corsican dock worker. An extremely deep, soft, resonant bass voice, slow and "
               "very, very kind, like a huge warm teddy bear. Speaks Italian with a rural Corsican accent, in short simple "
               "sentences, always careful and friendly. Close microphone, clean studio recording, no background noise.",
               "Ciao. Io sono Minicu. Porto le casse, qui al porto. Ti fa male? No? Bene. Sono contento. Questa è pesante, "
               "ma non è un problema, la porto io. Tu vai pure, piano piano. Pascal dice che devo restare al cancello, e io "
               "resto. Hai fame? Ho un po' di pane. Prendilo, è buono. Non ti preoccupare. Ci sono io."),
    "buenaventura": ("Captain Buenaventura", "ES",
                     "A handsome Spanish pirate captain in his mid-forties. A big, warm, theatrical baritone, proud and pompous, "
                     "a man who announces himself like a king and means every word. Native Spanish speaker from Spain. Close "
                     "microphone, clean studio recording, no background noise.",
                     "¡Soy el capitán Buenaventura, del navío The Eventually! Tengo una bandera, un himno y un rey. Solo me falta "
                     "la isla. ¿Mis deudas? ¿Qué deudas? Pagaré, señor. Algún día. ¡Lo pone en el barco! Mis hombres son los "
                     "mejores de todo el Mediterráneo, y tienen hambre, y yo también. Así que seamos civilizados: ¿dónde está el "
                     "tesoro?"),
    "anghjulu": ("Don Anghjulu", "IT",
                 "A Corsican priest around sixty, a big, warm, wine-rounded, slightly slurred baritone, laughing easily, "
                 "lazy and kind, suddenly clear and quiet when it matters. Speaks Italian with a rural Corsican accent. "
                 "Close microphone, clean dry studio recording, no reverb, no background noise.",
                 "Figliolo mio, entra, entra, Dio vede tutto, ma non ha ancora visto questa bottiglia. Quattordici anni "
                 "combatto con quel gabbiano, quattordici! Il Signore provvede, e io non chiedo mai da quale conto. Taglia "
                 "le carte, su. No, aspetta. Siediti un momento. Ti sembro ubriaco, lo so. Però ascoltami bene, perché lo "
                 "dico una volta sola."),
}


def schluessel():
    return json.load(open(r"X:\AI\VoiceStudio\voice-studio.json", encoding="utf-8-sig"))["api_key"]


def post(pfad, daten):
    req = urllib.request.Request(API + pfad, data=json.dumps(daten).encode(), method="POST",
                                 headers={"xi-api-key": schluessel(), "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())


def entwerfen(pid):
    name, spr, beschreibung, text = ROLLEN[pid]
    try:
        d = post("design", {"voice_description": beschreibung, "model_id": "eleven_ttv_v3", "text": text,
                            "auto_generate_text": False})
    except urllib.error.HTTPError as e:
        print(pid, "design:", e.code, e.read()[:200])
        d = post("create-previews", {"voice_description": beschreibung, "text": text})
    for n, p in enumerate(d.get("previews") or [], 1):
        open(os.path.join(ZIEL, "%s_%d.mp3" % (pid, n)), "wb").write(base64.b64decode(p["audio_base_64"]))
        print(pid, n, "%.1f s" % p.get("duration_secs", 0))


def messen(datei):
    """Pegel (LUFS), Dauer, Rauschband 8-10 kHz in den leisesten 10 % der Zeit (Qualitaet, nicht Samplerate)."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", datei, "-af", "loudnorm=print_format=json", "-f",
                        "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    lufs = float(re.search(r'"input_i" : "([-\d.]+)"', r).group(1))
    dauer = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", datei],
                                 capture_output=True, text=True).stdout)
    band = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", datei, "-af",
                           "highpass=f=8000,lowpass=f=10000,astats=metadata=1:reset=0", "-f", "null", "-"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    rms = re.findall(r"RMS level dB: ([-\d.inf]+)", band)
    voll = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", datei, "-af", "astats", "-f", "null", "-"],
                          capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    rms_voll = re.findall(r"RMS level dB: ([-\d.inf]+)", voll)
    b = float(rms[-1]) if rms and rms[-1] not in ("-inf", "inf") else -99
    v = float(rms_voll[-1]) if rms_voll and rms_voll[-1] not in ("-inf", "inf") else -99
    return {"lufs": round(lufs, 1), "dauer": round(dauer, 1), "band_8_10k_db": round(b - v, 1)}


def referenz(pid, n):
    name, spr = ROLLEN[pid][:2]
    aus = os.path.join(VOICES, "%s - %s.wav" % (name, spr))
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", os.path.join(ZIEL, "%s_%d.mp3" % (pid, n)),
                    "-af", "loudnorm=I=-20:TP=-2", "-ar", "24000", "-ac", "1", aus], check=True)
    return aus


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(ZIEL, exist_ok=True)
    args = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] != "--ziel"]
    nur = [a for a in args if a in ROLLEN]
    if args != nur:                    # 29.10.2026: unbekannter Name lief frueher still ueber ALLE Rollen (Credits)
        sys.exit("Unbekannte Rolle(n): %s - nichts entworfen" % ", ".join(a for a in args if a not in ROLLEN))
    if "--messen" not in sys.argv and not nur and "--alle" not in sys.argv:
        sys.exit("Rollen nennen (oder --alle) - nichts entworfen")
    if "--messen" not in sys.argv:
        for pid in nur or ROLLEN:
            entwerfen(pid)
    werte = {}
    for f in sorted(os.listdir(ZIEL)):
        if f.endswith(".mp3"):
            werte[f[:-4]] = messen(os.path.join(ZIEL, f))
            print(f, werte[f[:-4]])
    json.dump(werte, open(os.path.join(ZIEL, "messung.json"), "w", encoding="utf-8"), indent=1)


if __name__ == "__main__":
    main()
