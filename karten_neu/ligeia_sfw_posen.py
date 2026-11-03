# -*- coding: utf-8 -*-
r"""Ligeia: der ganze 😇-SFW-Satz mit eigenen Posen fuer ihren Fischschwanz (Duc 30.10.2026: "alle SFW Posen spezielle fuer
sie, damit es mit ihrer Anatomie Sinn macht"). Sie hat keine Beine, Knie oder Fuesse: Sie sitzt, liegt oder stuetzt sich auf dem
Stein, Gefuehl tragen Gesicht, Arme, Oberkoerper und Schwanzflosse. Die Kartentexte gelten nur fuer diesen Lauf, denn die
Karten teilen sich alle Figuren. Kein Nachbelichten, Hintergrund spaeter.

    ligeia_sfw_posen.py          Probelauf
    ligeia_sfw_posen.py --los [--karten a,b]
    ligeia_sfw_posen.py --los --ohne-felsen   die sieben Posen, bei denen der Stein stehen blieb, ohne Stein (Abnahme ligeia_sfw)
"""
import io, json, os, shutil, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
PRESET, KOST, ST_SET = "Yacht_Ligeia", "Standard", "Yacht_Ligeia/Standard/roh"
ROH = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\Yacht_Ligeia\Standard\roh"
ALT_KOPF = ("sitting sideways on a low dark wet rock, propped on one straight arm, her upper body turned to the camera, her whole "
            "fish tail in full view,")
NEU_KOPF = ("resting on a low dark wet rock, she has no legs and no feet, only one fish tail from the hips down, her whole fish "
            "tail in full view,")
OHNE_FELSEN = {
    "caring": "She lies propped up on one elbow on the flat floor, the other arm reaching out toward the viewer, palm open. Soft empathetic face, gentle reassuring smile, warm relaxed eyes.",
    "caring_2": "She sits upright on the flat floor with both hands cupped gently in front of her chest as if cradling something precious, her tail stretched out straight behind her to one side, never behind her back. Tender nurturing face, soft eyes.",
    "embarrassment": "She sits upright on the flat floor with one arm crossed over her chest and the other hand at her cheek, shoulders raised, tail curling in on itself. Mortified flustered face, a natural flush across her cheeks, eyes sliding away.",
    "fear": "She sits on the flat floor twisting away with her back half to the camera, shoulders hunched, looking back over her shoulder, both hands drawn up against her chest, tail pulled in tight. Frightened wide eyes.",
    "fear_2": "She shrinks back on the flat floor, propped on one arm, the other hand raised defensively in front of her chest, shoulders hunched tight, tail coiled close. Terrified face, eyes wide, mouth open.",
    "grief_2": "She lies collapsed on the flat floor, her upper body sunk onto her folded arms, face lifted slightly toward the camera, tail fin lying still. Broken grieving face, tears on her cheeks.",
    "love": "She sits upright on the flat floor with both hands folded over her tail just below her hips, her body swaying toward the camera, tail fin curled in. Melting affectionate face, soft warm eyes, a shy closed-lip smile.",
}
KOPF_FREI = ("resting directly on a flat empty floor, nothing under her and no objects anywhere, she has no legs and no feet, only "
             "one fish tail from the hips down, her whole fish tail in full view,")
BOGEN_ALT, BOGEN_NEU = "across the rock and the floor", "across the floor"
POSEN = {
    "neutral": "She sits upright on the rock, one arm resting along her tail, the other hand on her chest, tail lying calm and still. Calm unreadable face, soft even gaze.",
    "neutral_2": "She sits in a relaxed three-quarter turn, one hand resting on the rock beside her, the other lying loose on her tail. Calm unreadable face, soft neutral gaze.",
    "admiration": "She sits leaning back a little on the rock, one hand pressed flat to her cheek, the other laid across her chest, tail fin lifting slightly. Starstruck admiring face, warm soft smile.",
    "love": "She sits with both hands folded over her tail just below her hips, her body swaying toward the camera, tail fin curled in. Melting affectionate face, soft warm eyes, a shy closed-lip smile.",
    "amusement": "She sits with one hand raised beside her mouth and the other across her stomach, shoulders shaking with laughter, tail fin flicking up. Cheeky open grin caught mid-giggle, eyes squeezed nearly shut.",
    "approval": "She sits with one hand on her hip and gives a slow nod, the other arm propped on the rock, tail lying easy. Warm approving grin, relaxed crinkled eyes, one corner of her mouth higher.",
    "approval_2": "She sits with her arms loosely crossed, chin lifted, nodding slowly, tail curved lazily behind her. Approving half-smile, warm eyes.",
    "gratitude": "She sits with both hands pressed flat over her heart, shoulders soft, dipping her head in a small bow. Touched grateful face, gentle smile.",
    "gratitude_2": "She bends forward over her tail with both hands clasped in front of her chest, head bowed slightly, shoulders soft and relaxed. Overwhelmed grateful face, eyes shining.",
    "joy": "She sits up tall with both fists drawn up under her chin, elbows tucked against her ribs, shoulders raised, tail fin slapping upward. Radiant open laugh showing teeth, cheeks pushed up.",
    "joy_2": "She arches back on the rock with one arm flung up and her head thrown back, the other hand on the stone, tail fin thrown high with water drops flying. Unrestrained joyful laugh, eyes crinkled shut.",
    "joy_3": "She sits with one fist raised overhead and the other hand on her hip, tail fin raised proudly. Radiant open laugh showing teeth, cheeks pushed up.",
    "optimism": "She sits upright with both hands on her hips and her chest open, gazing past the camera, tail stretched long across the stone. Bright hopeful smile, clear open eyes, relaxed brows.",
    "optimism_2": "She sits lifted tall on her tail with both hands clasped in front of her chest, elbows close to her body, head tilted slightly up, tail fin raised. Hopeful bright-eyed face, wide easy smile.",
    "pride": "She sits very straight with her fists on her hips, chest out, chin high, tail fin raised and spread wide. Self-satisfied smirk, lids lowered in a cool look, one eyebrow arched.",
    "relief": "She sinks back onto the rock with one hand flat on her chest and the other arm dropping loose beside her, tail going slack. Tension melting from her face, eyes half closed, a long breath out.",
    "relief_2": "She leans back on one arm with her shoulders dropping, the other hand resting flat on her chest, tail lying limp. Relieved unwinding face, eyes closed, a long breathy smile.",
    "disappointment": "She slumps sideways on the rock, shoulders sagging, arms hanging heavy, head turned toward the camera, tail fin drooping to the floor. Let-down face, flat mouth, lowered brows.",
    "disappointment_2": "She turns half away from the camera, arms crossed loosely over her stomach, head dropped and gaze cast down, tail curling away. Crestfallen face, downcast eyes.",
    "grief": "She curls over her tail with her back half to the camera, shoulders curled forward and head bowed, looking back over her shoulder, both arms wrapped tight around herself. Broken grieving face, wet eyes.",
    "grief_2": "She lies collapsed along the rock, her upper body sunk onto her folded arms, face lifted slightly toward the camera, tail fin lying still in the wet. Broken grieving face, tears on her cheeks.",
    "remorse": "She sits drawn in with her hands clasped low on her tail, fidgeting, shoulders in, head slightly bowed. Guilty apologetic grimace, wet pleading eyes, brows tented.",
    "remorse_2": "She sits hunched forward over her tail with both hands pressed over her face, shoulders curled inward. Anguished remorseful face half-hidden behind her fingers.",
    "sadness": "She hugs herself tightly with both arms, shoulders curled forward, tail pulled in close around the rock. Glassy brimming eyes, trembling chin, corners of her mouth pulled down.",
    "anger": "She leans in hard toward the camera on one straight arm, the other fist clenched at her side, shoulders squared, tail fin raised to strike the stone. Hard glare, brows drawn tight, clenched jaw.",
    "anger_2": "She lunges forward over the rock with one arm jabbing a rigid finger toward the camera, the other hand braced on the stone, tail lashing behind her. Furious face, bared teeth.",
    "annoyance": "She sits with her arms crossed tight and her elbows flared, her head turned back over her shoulder, tail fin tapping the stone. Irritated flat stare, one eyebrow raised.",
    "annoyance_2": "She sits with both hands planted on her hips, elbows out wide, head tipped back in an exasperated exhale, tail fin flicking to the side. Exasperated flat stare.",
    "disapproval": "She sits squared up to the camera, rigid, one arm barred across her body and an index finger wagging. Stern disapproving look, one eyebrow raised, lips pursed tight.",
    "disapproval_2": "She sits with both arms folded firmly across her chest, chin tucked down, shaking her head slowly, tail very still. Disapproving glare, brows pulled low.",
    "disgust": "She leans her torso back away from the camera with both palms pushed out, tail curling away from it. Face screwed up in revulsion, nose wrinkled, upper lip curled back.",
    "disgust_2": "She turns her shoulders sharply away from the camera with one hand raised palm-out as if warding it off, the other braced on the rock. Repulsed face, eyes narrowed.",
    "confusion": "She sits with one hand frozen mid-scratch at her temple, the other palm turned up, tail fin half lifted. Puzzled face, brows knitted unevenly, mouth twisted to one side.",
    "confusion_2": "She sits with both shoulders shrugged up to her ears, palms turned upward at her sides, head tilted sharply to one side. Baffled face, one brow raised.",
    "curiosity": "She leans far in toward the camera on both straight arms, her chin forward, tail fin swaying behind her. Keenly interested face, eyebrows lifted, a small intrigued smile, lips slightly parted.",
    "realization": "Her torso snaps around toward the camera, one index finger shooting upward, the other hand on the stone, tail fin stopped in mid-air. Dawning realization, eyes wide, mouth open.",
    "realization_2": "She freezes with one hand clapped over her open mouth, the other arm dropping loose, her whole body stiff, tail fin rigid. Stunned dawning face, eyes blown wide.",
    "surprise": "She jerks back on the rock mid-flinch, both hands flying up beside her face, tail fin snapping up. Jolted startled face, brows shot up, mouth dropped open in a gasp.",
    "embarrassment": "She sits with one arm crossed over her chest and the other hand at her cheek, shoulders raised, tail curling in on itself. Mortified flustered face, a natural flush across her cheeks, eyes sliding away.",
    "fear": "She twists away with her back half to the camera, shoulders hunched and pulled in, looking back over her shoulder, both hands drawn up against her chest, tail pulled in tight. Frightened wide eyes.",
    "fear_2": "She shrinks low against the rock with both hands raised defensively in front of her chest, shoulders hunched tight, tail coiled close. Terrified face, eyes wide, mouth open.",
    "nervousness": "She wrings her hands in front of her chest with her elbows pinned to her ribs, tail fin twitching. Anxious wince, teeth biting her lower lip, brows drawn up in the middle.",
    "caring": "She leans forward over the rock with both arms reaching out toward the viewer, palms open. Soft empathetic face, gentle reassuring smile, warm relaxed eyes.",
    "caring_2": "She bends forward with both hands cupped gently in front of her as if cradling something precious, torso leaning in close, tail curved around. Tender nurturing face, soft eyes.",
    "submissive": "She bows low over her tail with her hands resting open on the stone, her chin dipped and her eyes lifted to the camera. Quiet yielding face, soft eyes.",
    "worshipful": "She sits very tall with both hands cupped in front of her mouth, her head tilted up, gazing upward in awe. Reverent adoring face, eyes shining.",
    "amusement_back": "She sits with her back to the camera, twisting to look back over her shoulder with one hand raised beside her mouth, tail fin flicking. Cheeky open grin.",
    "embarrassment_back": "She sits with her back to the camera, shoulders raised, peeking back over her shoulder, tail curling in. Mortified flustered face, a natural flush across her cheeks.",
    "curiosity_back": "She sits with her back to the camera leaning forward on one arm, tilting her head around over her shoulder, tail fin swaying. Keenly interested face, eyebrows lifted.",
    "pride_back": "She sits very straight with her back to the camera, fists on her hips, chin turned over her shoulder, tail fin spread wide. Self-satisfied smirk, one eyebrow arched.",
    "sadness_back": "She sits with her back to the camera hugging herself, shoulders curled forward and head lowered, turning just enough to look back over her shoulder. Glassy brimming eyes.",
    "nervousness_back": "She sits with her back to the camera, elbows pinned to her ribs, glancing back over her shoulder, tail fin twitching. Anxious wince, teeth biting her lower lip.",
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


def main():
    nur = sys.argv[sys.argv.index("--karten") + 1].split(",") if "--karten" in sys.argv else None
    st = ps("/api/state")
    alt_preset = st["cfg"].get("preset_active")
    alt_prompt, vis = st["cfg"].get("sprite_prompt"), st["cfg"].get("decks_visible") or {}
    ps("/api/presets", {"action": "load", "name": PRESET})
    kp = ps("/api/set_preset_laden", {"char": PRESET, "kost": KOST})
    st = ps("/api/state")
    sp = st["cfg"]["sprite_prompt"]
    if ALT_KOPF not in sp:
        raise SystemExit("Kopfzeile im Preset hat sich geaendert - abgebrochen")
    d = st["decks"]
    soll = set(st["cfg"].get("sfw_posen") or [])
    fehlt = sorted(soll ^ set(POSEN))
    if fehlt:
        raise SystemExit("Posen passen nicht zum SFW-Satz: " + ", ".join(fehlt))
    frei = "--ohne-felsen" in sys.argv
    if frei:
        nur = nur or list(OHNE_FELSEN)
        POSEN.update(OHNE_FELSEN)
    wahl = [k for k in POSEN if not nur or k in nur]
    print("%d Posen" % len(wahl))
    if "--los" not in sys.argv:
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})
        sys.exit("PROBELAUF - mit --los einstellen")
    alt = {c["name"]: c["prompt"] for c in d["st"]}
    kopf = sp.replace(ALT_KOPF, KOPF_FREI).replace(BOGEN_ALT, BOGEN_NEU) if frei else sp.replace(ALT_KOPF, NEU_KOPF)
    if nur:
        korb = r"X:\AI\ComfyUI_krea2\ComfyUI\output\_expressions_papierkorb\Yacht_Ligeia_" + time.strftime("%Y%m%d_%H%M")
        os.makedirs(korb, exist_ok=True)
        for k in wahl:
            f = os.path.join(ROH, k + ".png")
            if os.path.isfile(f):
                shutil.move(f, korb)
        print("alte Bilder ->", korb)
    try:
        an = set(kp.get("tags") or [])
        tags = st["cfg"]["tags"]
        for t in tags:
            t["on"] = t["name"] in an
        for deck in ("outfit", "setting", "st", "kampf"):
            for c in d[deck]:
                c["sel"] = False
        for c in d["outfit"]:
            c["sel"] = c["name"] in set(kp.get("outfit") or [])
        for c in d["setting"]:
            c["sel"] = c["name"] in set(kp.get("setting") or [])
        for c in d["st"]:
            if c["name"] in wahl:
                c["prompt"], c["sel"] = POSEN[c["name"]], True
        ps("/api/config", {"tags": tags, "mode": "sprite", "st_set": ST_SET, "view_pro_karte": True, "combine_mode": "all",
                           "sprite_prompt": kopf, "st_rembg": True, "st_crop": True,
                           "decks_visible": dict(vis, kampf=False)})
        ps("/api/decks", d)
        print("eingereiht:", ps("/api/queue", {"cfg": {}, "decks": d, "max_auftraege": len(wahl)}).get("queued", 0))
    finally:
        d = ps("/api/state")["decks"]
        for c in d["st"]:
            if c["name"] in POSEN:
                c["prompt"] = alt[c["name"]]
        ps("/api/decks", d)
        ps("/api/config", {"view_pro_karte": False})
        if alt_preset:
            ps("/api/presets", {"action": "load", "name": alt_preset})


if __name__ == "__main__":
    main()
