# -*- coding: utf-8 -*-
"""Mastery moment (Duc 28.10.2026): candidates for the sound and the picture when a path is mastered, on one audition page.

Picture: the preview flipbooks embedded in IlluGen presets (Y:\\JangaFX\\IlluGen\\presets_2_0_0) are copied out as JPG
(same reading as effekt_vorschau_quellen.py: frame_count, frame_rate, flipbook_col_row) - preview resolution only, played
with mix-blend-mode screen over a mastered path row. Sound: Pixabay candidates, streamed from the CDN, nothing downloaded.
Writes docs/abnahme/meister_moment/ (index.html + bilder/). Verdicts are kept in the browser (localStorage) and can be copied.
"""
from pathlib import Path
import json
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
QUELLE = Path(r'Y:\JangaFX\IlluGen\presets_2_0_0')
ZIEL = ROOT / 'docs' / 'abnahme' / 'meister_moment'
# Sorted out after a look at the frames: grey backgrounds (magic_ground_impact, warp_drive, swipe_dissolve), plain
# textures (D3_VFX_Article, nebula_skies) and anything with dot, hole or fragment patterns (tech_wave, pixel_portal, worm_hole).
BILDER = ['shield_gradient']   # Duc 28.10.2026: gewaehlt (Runde 1: dazu golden_shockwave, star_gradient, combine_orb, lense_flare, mystical_curl_noise, advect_stylized_portal, power_storm)
TOENE_RUNDE1 = [  # verworfen; (name, author, seconds, cdn, page) - Pixabay Content License
    ('Achievement Unlock', 'Universfield', 4, 'https://cdn.pixabay.com/audio/2024/09/23/audio_863336b4be.mp3', 'https://pixabay.com/sound-effects/film-special-effects-achievement-unlock-243762/'),
    ('Level Up 08', 'Universfield', 5, 'https://cdn.pixabay.com/audio/2025/09/09/audio_cfe42a23f8.mp3', 'https://pixabay.com/sound-effects/film-special-effects-level-up-08-402152/'),
    ('Achievement Unlocked', 'PWLPL', 8, 'https://cdn.pixabay.com/audio/2025/06/18/audio_3e758ebcf4.mp3', 'https://pixabay.com/sound-effects/film-special-effects-achievement-unlocked-361842/'),
    ('Magic UI Level Up Stinger', '', 5, 'https://cdn.pixabay.com/audio/2026/06/15/audio_4efc21edca.mp3', 'https://pixabay.com/sound-effects/musical-magic-ui-level-up-stinger-fantasy-confirmation-sound-552109/'),
    ('XP Gain Magic Tone', 'humordome', 6, 'https://cdn.pixabay.com/audio/2025/12/18/audio_b23afb7e39.mp3', 'https://pixabay.com/sound-effects/technology-xp-gain-magic-tone-453274/'),
    ('Brass Fanfare', 'Universfield', 4, 'https://cdn.pixabay.com/audio/2023/04/02/audio_35739dee5a.mp3', 'https://pixabay.com/sound-effects/film-special-effects-brass-fanfare-144755/'),
    ('Victory Fanfare', 'Universfield', 4, 'https://cdn.pixabay.com/audio/2023/06/04/audio_3700fd07a3.mp3', 'https://pixabay.com/sound-effects/musical-victory-fanfare-152480/'),
    ('Success Fanfare Trumpets', 'freesound_community', 4, 'https://cdn.pixabay.com/audio/2021/08/04/audio_12b0c7443c.mp3', 'https://pixabay.com/sound-effects/film-special-effects-success-fanfare-trumpets-6185/'),
    ('Loud Fanfare Trumpet #01', 'AberrantRealities', 4, 'https://cdn.pixabay.com/audio/2025/09/29/audio_c412f017e4.mp3', 'https://pixabay.com/sound-effects/musical-loud-fanfare-trumpet-effect-01-412045/'),
    ('Heroic Orchestra Intro Logo', 'BreakzStudios', 8, 'https://cdn.pixabay.com/audio/2023/09/05/audio_fb7d3f5c8d.mp3', 'https://pixabay.com/sound-effects/musical-heroic-orchestra-intro-logo-165196/'),
    ('Epic Cinematic Reveal Logo', 'BreakzStudios', 12, 'https://cdn.pixabay.com/audio/2024/04/08/audio_82ab7bf29b.mp3', 'https://pixabay.com/sound-effects/musical-epic-cinematic-reveal-logo-201065/'),
    ('Logo Reveal', 'Universfield', 3, 'https://cdn.pixabay.com/audio/2024/04/01/audio_a41c2ba674.mp3', 'https://pixabay.com/sound-effects/film-special-effects-logo-reveal-199582/'),
]

TOENE = [  # Runde 2 (Duc 28.10.2026: Runde 1 - Fanfaren, Achievement-Klaenge - gefiel nicht): Chor, Gong, Harfe, Aufstieg, Licht
    ("Celestial Gong", "VoiceBosch", 5, 'https://cdn.pixabay.com/audio/2024/02/13/audio_4d8b9ef2f4.mp3', 'https://pixabay.com/sound-effects/film-special-effects-celestial-gong-191122/'),
    ("Holy Spell Cast", "DRAGON-STUDIO", 6, 'https://cdn.pixabay.com/audio/2025/12/12/audio_63e9c863f3.mp3', 'https://pixabay.com/sound-effects/musical-holy-spell-cast-450460/'),
    ("Holy Magic short (3)", "Yodguard", 3, 'https://cdn.pixabay.com/audio/2026/05/15/audio_c21579e2b7.mp3', 'https://pixabay.com/sound-effects/film-special-effects-holy-magic-short-3-534666/'),
    ("Light Magic (2)", "Yodguard", 8, 'https://cdn.pixabay.com/audio/2025/07/22/audio_6d6327dd7d.mp3', 'https://pixabay.com/sound-effects/film-special-effects-light-magic-2-378662/'),
    ("mixed chorus transformation", "freesound_community", 8, 'https://cdn.pixabay.com/audio/2022/03/10/audio_1670c4af33.mp3', 'https://pixabay.com/sound-effects/musical-mixed-chorus-transformation-43104/'),
    ("Magical Spell Transformation 1", "AppleHillStudios", 9, 'https://cdn.pixabay.com/audio/2026/06/04/audio_cf6d7bc2a9.mp3', 'https://pixabay.com/sound-effects/musical-magical-spell-transformation-1-543568/'),
    ("Magic Ascend 1", "BenKirb", 4, 'https://cdn.pixabay.com/audio/2024/11/03/audio_a735dd0003.mp3', 'https://pixabay.com/sound-effects/film-special-effects-magic-ascend-1-259521/'),
    ("Magic Ascend 3", "BenKirb", 10, 'https://cdn.pixabay.com/audio/2024/11/03/audio_acd3b835ce.mp3', 'https://pixabay.com/sound-effects/film-special-effects-magic-ascend-3-259526/'),
    ("Magic Harp Logo", "SergeQuadrado", 10, 'https://cdn.pixabay.com/audio/2022/03/24/audio_0485e65dcc.mp3', 'https://pixabay.com/sound-effects/magic-harp-logo-103888/'),
    ("Fairy Sparkle long", "humordome", 5, 'https://cdn.pixabay.com/audio/2025/12/14/audio_ab5538b66c.mp3', 'https://pixabay.com/sound-effects/fairy-sparkle-long-451416/'),
    ("Voxswell FX", "SoundReality", 6, 'https://cdn.pixabay.com/audio/2025/05/19/audio_5d88d24ec0.mp3', 'https://pixabay.com/sound-effects/film-special-effects-voxswell-fx-344128/'),
    ("Elemental Magic Spell Impact", "RescopicSound", 3, 'https://cdn.pixabay.com/audio/2024/07/30/audio_e8c15810bd.mp3', 'https://pixabay.com/sound-effects/film-special-effects-elemental-magic-spell-impact-outgoing-228342/'),
    ("Riser Hit sfx 001", "AudioPapkin", 4, 'https://cdn.pixabay.com/audio/2025/01/19/audio_175064ba80.mp3', 'https://pixabay.com/sound-effects/film-special-effects-riser-hit-sfx-001-289802/'),
    ("Cinematic Piano Hit", "Universfield", 4, 'https://cdn.pixabay.com/audio/2026/07/14/audio_8f98537420.mp3', 'https://pixabay.com/sound-effects/musical-cinematic-piano-hit-567216/'),
]


def wert(data, key, default):
    at = data.find(key.encode(), 0, 500)
    if at < 0:
        return default
    at += len(key)
    return struct.unpack_from('<Q', data, at + 1)[0] if data[at] == 5 else default


def vorschau(name):
    data = (QUELLE / (name + '.illugen')).read_bytes()
    a = data.find(b'\xff\xd8\xff')
    e = data.find(b'\xff\xd9', a) + 2
    if a < 0 or e <= a:
        return None
    at = data.find(b'flipbook_col_row', 0, 500)
    cols, rows = (8, 8)
    if at >= 0:
        at += len('flipbook_col_row')
        if data[at] == 6:
            cols, rows = struct.unpack_from('<QQ', data, at + 1)
    return data[a:e], {'cols': cols, 'rows': rows, 'frames': wert(data, 'frame_count', 64), 'fps': wert(data, 'frame_rate', 30)}


def main():
    (ZIEL / 'bilder').mkdir(parents=True, exist_ok=True)
    bilder = []
    for n in BILDER:
        v = vorschau(n)
        if not v:
            print('ohne Vorschau:', n)
            continue
        (ZIEL / 'bilder' / (n + '.jpg')).write_bytes(v[0])
        bilder.append(dict(v[1], id=n, file='bilder/' + n + '.jpg'))
    daten = {'bilder': bilder, 'toene': [dict(zip(('name', 'autor', 'sek', 'src', 'seite'), t)) for t in TOENE]}
    seite = (ZIEL / 'vorlage.html').read_text(encoding='utf-8').replace('/*DATEN*/', json.dumps(daten, ensure_ascii=False))
    (ZIEL / 'index.html').write_text(seite, encoding='utf-8', newline='\n')
    print('%d Bilder, %d Toene -> %s' % (len(bilder), len(TOENE), ZIEL / 'index.html'))


if __name__ == '__main__':
    sys.exit(main())
