"""Build the separate four-status visual experiment; never writes game data."""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'docs/effekt-auswahl/status-labor'
TEXTURES = Path('Y:/JangaFX/IlluGen/textures')


def emission(image):
    """Convert black-backed emission to straight alpha without losing RGB detail."""
    result = Image.new('RGBA', image.size)
    pixels = []
    for index, (r, g, b) in enumerate(image.convert('RGB').getdata()):
        a = max(r, g, b)
        x, y = index % image.width % 256, index // image.width % 256
        edge = min(1, min(x, y, 255-x, 255-y) / 18)
        pixels.append((r * 255 // a, g * 255 // a, b * 255 // a, int(a * edge)) if a > 5 else (0, 0, 0, 0))
    result.putdata(pixels)
    return result


def main():
    (DEST / 'assets').mkdir(parents=True, exist_ok=True)
    records = []
    sources = [
        ('feuer', TEXTURES / 'game_fire_loop_2_render_all.png', True, 'Mitgelieferte originale Feueranimation; keine neue Simulation'),
        ('staub', TEXTURES / 'diablo_mana_smoke_loop_8x8.png', False, 'Mitgelieferter Rauch, als bodennahe Staubwolke gestaltet'),
        ('strom', ROOT / 'docs/effekt-auswahl/quellen/vorlagen-vorschauen/lightning_sheet.jpg', True, 'Eingebettete IlluGen-Vorschau; noch kein Produktions-Export'),
    ]
    for name, source, light, description in sources:
        picture = Image.open(source).convert('RGBA')
        picture = picture.resize((2048, 2048), Image.Resampling.LANCZOS)
        if light:
            picture = emission(picture)
        if name == 'staub':
            # Fade every frame independently, so an atlas cell never forms a box.
            edge = Image.new('L', (256, 256))
            edge.putdata([int(255 * (lambda t: t*t*(3-2*t))(min(1, min(x,y,255-x,255-y)/48))) for y in range(256) for x in range(256)])
            mask = Image.new('L', picture.size)
            for row in range(8):
                for col in range(8):
                    mask.paste(edge, (col*256, row*256))
            picture.putalpha(ImageChops.multiply(picture.getchannel('A'), mask))
        picture.save(DEST / 'assets' / (name + '.png'))
        records.append({'name': name, 'source': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'description': description, 'frames': 64, 'columns': 8, 'frame_pixels': 256, 'production_ready': False})
    for pose in ('idle', 'hurt', 'windup', 'guard', 'weakened'):
        shutil.copy2(ROOT / ('docs/effekt-auswahl/assets/figur_' + pose + '.webp'), DEST / ('assets/figur_' + pose + '.webp'))
    (DEST / 'quellen/manifest.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Drei Texturfolgen vorbereitet; vier Statusentwuerfe, keine Spieldaten geaendert.')


if __name__ == '__main__':
    main()
