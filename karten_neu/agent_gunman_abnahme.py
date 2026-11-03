# -*- coding: utf-8 -*-
r"""Abnahme-Spec fuer den vollen Satz AgentGunman: docs\abnahme\agent_gunman_satz.json."""
import glob, json, os

W = r"X:\AI\ComfyUI_krea2\ComfyUI\output\expressions\_agent_gunman_satz"
HINWEISE = {"idle": "Deine Wahl.", "attack": "Mündungsfeuer kommt im Kampf als Effekt.", "heavy_attack": "Kniend, Mündungsfeuer kommt im Kampf als Effekt.",
            "heavy_windup": "Kniend, fast wie heavy_attack. Der Unterschied im Kampf kommt vor allem durch das Feuer.",
            "guard": "Das Gewehr liegt schräg vor dem Körper, zeigt aber eher nach unten. Wirkt weniger nach Abwehr als Wolffs Klinge.",
            "flee": "Wird beim Einbau gespiegelt, damit sie nach rechts wegläuft.", "defeated": "Ohne Waffe.", "surrender": "Ohne Waffe."}
items = []
for p in sorted(glob.glob(os.path.join(W, "*.png"))):
    pose = os.path.basename(p)[:-4]
    items.append({"id": pose, "titel": "Schützin · %s" % pose, "bild": p, "soll": HINWEISE.get(pose, "Wie deine Wahl.")})
spec = {"id": "agent_gunman_satz_v1", "titel": "Die Schützin der Agenten: voller Satz", "items": items,
        "hinweis": "13 Kampf-Posen auf Basis von Variante 1. Mein Vorschlag: alles übernehmen, guard höchstens noch einmal neu. Nur was nicht passt, auf „Neu“ setzen. Ins Spiel kommt der Satz erst nach deinem Urteil."}
with open(r"X:\AI\Eden\docs\abnahme\agent_gunman_satz.json", "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print(len(items))
