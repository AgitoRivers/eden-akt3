# -*- coding: utf-8 -*-
r"""Ganze Kampf-Saetze fuer die neuen Tiere der Tierstation (Duc 01.11.2026): Madame (RussianBlue), Monday (Capybara), Twelve (Tortoise), Bones (BeardedVulture), Roter Panda, Schneeleopard, Waran.
Aufbau wie kampf_bearcub.py: Kartentexte je Tier nur fuer den Lauf, danach zurueckgesetzt. Die Standard-Karten sind teils fuer Menschen (Haende, Waffen).
surrender = die Schlafgranate wirkt, das Tier schlaeft ein (Ausgang "aufgabe"). Alle schauen nach links, flee rennt direkt nach rechts. Keine Lochmuster.

    kampf_tierstation_posen.py                  Probelauf
    kampf_tierstation_posen.py --los            alle vier
    kampf_tierstation_posen.py --los Tortoise   nur dieses Tier
"""
import io, json, os, subprocess, sys, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
PS = "http://127.0.0.1:8301"
PY = r"X:\AI\ComfyUI_krea2\python_embeded\python.exe"
HIER = os.path.dirname(os.path.abspath(__file__))
GANZ = ", the whole animal fully inside the image with empty space around it, one single animal, clean empty floor"

POSEN = {
    "RedPanda": {
        "idle": "standing low on all four legs, facing left, back arched, fluffy tail straight up, small teeth bared, wild staring eyes",
        "windup": "crouched low, rear end raised, one black front paw drawn back with claws out, eyes locked to the left",
        "attack": "leaping forward to the left, one black front paw swiping with claws out, mouth wide open, slight motion blur on the paw",
        "heavy_windup": "standing upright on its hind legs with both front paws raised high and wide to look big, fluffy tail behind it, mouth open, black belly showing",
        "heavy_attack": "dropping forward onto the left from its hind legs, both front paws slamming down, mouth wide open, motion blur on the paws",
        "guard": "pulled back on its haunches, turned slightly away, fluffy tail wrapped in front of its body, peeking warily to the left",
        "hurt": "knocked backwards onto its rump, head thrown back, eyes squeezed shut, mouth open, front paws in the air",
        "enraged": "all its fur standing up, tail puffed to twice its size, teeth bared, staring eyes, shrieking to the left",
        "weakened": "sitting heavily, head drooping, half-closed eyes, panting, fluffy tail flat on the ground, swaying",
        "surrender": "falling asleep, curled up on the ground with its fluffy tail over its nose, eyes closed, the small red light on its collar still on",
        "flee": "running away to the right at full speed, body seen from the side facing right, fluffy tail streaming behind, ears flat",
        "victory": "sitting upright on its rump, chin high, front paws on its black belly, looking down to the left, very pleased",
        "defeated": "lying collapsed on its side, legs limp, tail limp, the head on the floor on the RIGHT side of the image, eyes closed" + GANZ,
        "death": "lying flat on its side, legs stretched out, the head on the floor on the RIGHT side of the image, eyes closed, motionless, peaceful" + GANZ,
    },
    "SnowLeopard": {
        "idle": "low on all four legs, facing left, shoulders high, head low, long tail out behind it, wild pale green eyes, long fangs showing",
        "windup": "flat against the ground like a coiled spring, hind legs bunched under its body, tail twitching, eyes locked to the left",
        "attack": "leaping forward to the left with its whole body stretched in the air, both front paws reaching out with claws out, mouth wide open, slight motion blur on the paws, the whole tail inside the image",
        "heavy_windup": "rearing up on its hind legs, both huge front paws raised with claws out, mouth wide open showing long fangs, long tail on the ground",
        "heavy_attack": "crashing down forward onto the left with both huge front paws, whole weight behind them, mouth wide open, motion blur on the paws",
        "guard": "pulled back low on its haunches, turned slightly away, one front paw raised, ears flat, eyes on the threat",
        "hurt": "knocked sideways off balance, head thrown back, eyes squeezed shut, mouth open, one front paw lifted",
        "enraged": "thick fur bristling along its back, tail lashing, long fangs bared, staring pale eyes, snarling to the left",
        "weakened": "standing on shaking legs, head hanging low, half-closed eyes, panting, tail dragging on the ground",
        "surrender": "falling asleep, lying on its belly with its chin on its front paws and its long fluffy tail curled around its body, eyes closed, the small red light on its collar still on",
        "flee": "running away to the right at full speed, body seen from the side facing right, long tail streaming behind, the whole tail inside the image",
        "victory": "standing tall and elegant on a low flat stone, chin high, long tail curled, looking down to the left",
        "defeated": "lying collapsed on its side, legs limp, the head on the floor on the RIGHT side of the image, eyes closed" + GANZ,
        "death": "lying flat on its side, legs stretched out, the head on the floor on the RIGHT side of the image, eyes closed, motionless, peaceful" + GANZ,
    },
    "Komodo": {
        "idle": "standing low on its bowed legs, seen from the side, facing left, flat head raised, long yellow forked tongue out, cold furious eyes, the whole long tail inside the image",
        "windup": "body curved into a tight S shape, head pulled back, mouth slightly open, eyes locked to the left, the whole long tail inside the image",
        "attack": "lunging forward to the left, flat head shooting out, mouth wide open, slight motion blur on the head, the whole long tail inside the image",
        "heavy_windup": "rearing up on its hind legs and thick tail like a tripod, front legs hanging, chest high, mouth open, forked tongue out",
        "heavy_attack": "swinging its long heavy tail in a hard sweep towards the left, whole body twisted, mouth open, motion blur on the tail, the whole tail inside the image",
        "guard": "body turned sideways, head pulled back, thick tail curved around in front of its body, eyes on the threat",
        "hurt": "knocked sideways, head thrown up, eyes squeezed shut, mouth open, front legs off the ground, tail bent",
        "enraged": "neck swollen, mouth wide open, hissing to the left, long forked tongue out, body raised high on straight legs, tail lashing",
        "weakened": "belly flat on the ground, legs splayed, head low, tongue hanging out, eyes half closed",
        "surrender": "falling asleep, stretched out flat on its belly, chin on the floor, eyes closed, the small red light on its collar still on, the whole long tail inside the image",
        "flee": "running away to the right at full speed, seen from the side facing right, body swinging from side to side, tail straight behind, the whole tail inside the image",
        "victory": "standing high on its bowed legs, flat head raised, forked tongue out, looking down to the left, in no hurry at all",
        "defeated": "lying collapsed on its side, legs limp, tail limp, the head on the floor on the RIGHT side of the image, eyes closed" + GANZ,
        "death": "lying flat on its belly, legs and tail stretched out, the head on the floor on the RIGHT side of the image, eyes closed, motionless, peaceful" + GANZ,
    },
    "RussianBlue": {
        "idle": "standing low on all four short legs, facing left, back arched, fur bristling, wild staring green eyes, ears flat, hissing",
        "windup": "crouched low with its big round belly on the ground, rear end wiggling, one front paw drawn back, eyes locked to the left",
        "attack": "leaping forward to the left with its round body in the air, one front paw swiping with claws out, mouth wide open, slight motion blur on the paw",
        "heavy_windup": "standing tall on its hind legs, very round belly showing, both front paws raised high with claws out, puffed up to twice its size, furious",
        "heavy_attack": "dropping its whole heavy round body forward onto the left, both front paws slamming down, claws out, mouth wide open in a yowl, motion blur on the paws",
        "guard": "pulled back on its haunches, turned slightly away, ears flat, one front paw raised to block, peeking warily to the left",
        "hurt": "knocked backwards onto its round rump, head thrown back, eyes squeezed shut, mouth open, front paws in the air",
        "enraged": "fur standing straight up all over its round body, tail thick as a brush, teeth bared, staring green eyes, screaming to the left",
        "weakened": "sitting heavily with its round belly on the ground, head drooping, half-closed eyes, panting, swaying",
        "surrender": "falling asleep, lying on its round belly with its chin on its front paws, eyes closed, ears relaxed, the small red light on its collar still on",
        "flee": "running away to the right at full speed, body seen from the side facing right, belly swinging, ears flat, tail low",
        "victory": "sitting upright and very round, chin high, eyes half closed, looking down to the left, deeply pleased with itself",
        "defeated": "lying collapsed on its side, round belly up, legs limp, the head on the floor on the RIGHT side of the image, eyes closed" + GANZ,
        "death": "lying flat on its side, legs stretched out, the head on the floor on the RIGHT side of the image, eyes closed, motionless, peaceful" + GANZ,
    },
    "Capybara": {
        "idle": "standing square on four legs, facing left, head low and pushed forward, wide staring eyes, long front teeth bared",
        "windup": "backing up on its legs, heavy barrel body pulled back, head low, eyes locked to the left, about to charge",
        "attack": "charging forward to the left, heavy body low, mouth open with its long front teeth snapping forward, slight motion blur on the head",
        "heavy_windup": "rearing up on its hind legs with its barrel body upright, front feet in the air, mouth wide open, showing long front teeth",
        "heavy_attack": "throwing its whole heavy body forward onto the left, front feet slamming down, long front teeth bared, motion blur on the front legs",
        "guard": "turned sideways with its broad flank towards the left, head pulled in, braced on all four legs, eyes on the threat",
        "hurt": "knocked back onto its haunches, head thrown up, eyes squeezed shut, mouth open, front feet off the ground",
        "enraged": "coarse fur bristling along the whole back, teeth bared, staring eyes with white showing, head low, shaking with rage",
        "weakened": "standing on shaking legs, big head hanging low, half-closed eyes, panting, swaying",
        "surrender": "falling asleep, lying on its big belly with its blunt muzzle resting on the ground, eyes closed, completely at peace, the small red light on its collar still on",
        "flee": "running away to the right, body seen from the side facing right, heavy and clumsy at full speed, ears flat",
        "victory": "standing on a low flat stone, chin high, eyes half closed, looking down to the left, completely calm again",
        "defeated": "lying collapsed on its side, legs limp, the blunt head on the floor on the RIGHT side of the image, eyes closed" + GANZ,
        "death": "lying flat on its side, legs stretched out, the blunt head on the floor on the RIGHT side of the image, eyes closed, motionless, peaceful" + GANZ,
    },
    "Tortoise": {
        "idle": "standing high on its thick legs, facing left, wrinkled neck stretched far out towards the left, beak-like mouth slightly open, furious small eyes",
        "windup": "neck pulled back in an S shape, head low, thick front legs braced wide, eyes locked to the left, about to strike",
        "attack": "neck shooting forward to the left at full length, beak-like mouth wide open, biting the air, slight motion blur on the head",
        "heavy_windup": "rearing up on its hind legs with the front of its heavy shell in the air, front legs raised, neck stretched up, mouth open",
        "heavy_attack": "slamming its heavy shell down forward onto the left, front of the shell hitting the floor, neck stretched out, mouth wide open, motion blur on the shell",
        "guard": "pulled completely into its shell, only the tips of its thick front legs and the top of its head showing, the collar visible at the opening, shell facing left",
        "hurt": "tipped back with the front of its shell in the air, front legs waving, neck stretched up, eyes squeezed shut, mouth open",
        "enraged": "standing as tall as it can, neck at full length, head shaking, mouth wide open, hissing to the left, furious small eyes",
        "weakened": "low on the ground with its shell resting on the floor, neck hanging out limp, eyes half closed, legs splayed",
        "surrender": "falling asleep, shell flat on the ground, neck stretched out on the floor, eyes closed, deeply at peace, the small red light on its collar still on",
        "flee": "walking away to the right as fast as it can, body seen from the side facing right, neck stretched forward, one thick leg lifted, looking determined",
        "victory": "standing high on its thick legs, chin up, eyes half closed, chewing, looking down to the left, deeply unimpressed",
        "defeated": "lying flat with its shell on the ground, legs and neck limp and spread out, the head on the floor on the RIGHT side of the image, eyes closed" + GANZ,
        "death": "lying flat with its shell on the ground, legs and neck stretched out, the head on the floor on the RIGHT side of the image, eyes closed, motionless, peaceful" + GANZ,
    },
    "BeardedVulture": {
        "idle": "standing on the ground, facing left, wings half open at its sides, head low and pushed forward, beak open, pale wild eye with its red ring staring",
        "windup": "crouched on its strong legs, both wings raised behind its body, head pulled back, eyes locked to the left, ready to spring",
        "attack": "swooping forward to the left a little above the ground, both yellow-grey talons reaching forward, wings spread, beak open, slight motion blur on the talons, both wingtips inside the image",
        "heavy_windup": "rearing up tall with both huge wings spread wide and raised high, chest out, beak open, both wingtips inside the image",
        "heavy_attack": "diving steeply towards the left, wings swept back along its body, both talons stretched forward, beak open, motion blur on the talons",
        "guard": "turned sideways with one huge folded wing raised in front of its chest like a shield, peeking to the left over the wing",
        "hurt": "knocked backwards with both wings flung out, feathers ruffled, head thrown back, eye squeezed shut, beak open, both wingtips inside the image",
        "enraged": "all head and chest feathers standing up, rust-orange ruff spread wide, wings half open and shaking, beak wide open, screaming to the left",
        "weakened": "standing on shaking legs, wings hanging down and dragging on the ground, head drooping, eye half closed, beak open",
        "surrender": "falling asleep, sitting low on the ground with its wings folded and its head sunk onto its chest, eyes closed, the small red light on its collar still on",
        "flee": "flapping away to the right, seen from the side facing right, wings beating, feet just off the ground, both wingtips inside the image",
        "victory": "standing tall, wings half open, chest out, looking down to the left along its beak",
        "defeated": "lying collapsed on the ground on its side, one wing spread limp on the floor, the head on the floor on the RIGHT side of the image, eyes closed" + GANZ,
        "death": "lying flat on the ground, both wings spread limp, the head on the floor on the RIGHT side of the image, eyes closed, motionless, peaceful" + GANZ,
    },
}


def ps(pfad, daten=None):
    req = urllib.request.Request(PS + pfad, data=None if daten is None else json.dumps(daten).encode(),
                                 headers={"Content-Type": "application/json", "X-Tab": "skript"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


nur = [a for a in sys.argv[1:] if not a.startswith("-")] or list(POSEN)
print(", ".join("%s %d" % (n, len(POSEN[n])) for n in nur))
if "--los" not in sys.argv:
    sys.exit("PROBELAUF - mit --los einstellen")
original = {c["name"]: c["prompt"] for c in ps("/api/state")["decks"]["kampf"]}
n = 0
try:
    for wer in nur:
        for pose, text in POSEN[wer].items():
            d = ps("/api/state")["decks"]
            for c in d["kampf"]:
                if c["name"] == pose:
                    c["prompt"] = text
            ps("/api/decks", d)
            subprocess.run([PY, os.path.join(HIER, "kampf_test.py"), "--karten", pose, "--gegner", wer], check=True, stdout=subprocess.DEVNULL)
            n += 1
        print("eingereiht:", wer)
finally:
    d = ps("/api/state")["decks"]
    for c in d["kampf"]:
        if c["name"] in original:
            c["prompt"] = original[c["name"]]
    ps("/api/decks", d)
print("eingestellt: %d Posen, Kartentexte zurueckgesetzt" % n)
