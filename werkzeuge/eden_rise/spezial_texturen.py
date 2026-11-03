"""Small deterministic material textures for the local VFX study, not simulations."""
from pathlib import Path
import random
from PIL import Image, ImageFilter

DEST = Path(__file__).resolve().parents[2] / 'docs/effekt-auswahl/status-labor/assets'


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    rng = random.Random(27182)
    # Low frequency, seamless fields with retained midtones. No cell/dot pattern.
    layers = []
    for size, weight in ((8, .58), (16, .28), (32, .14)):
        core = [[rng.randrange(70, 226) for x in range(size)] for y in range(size)]
        tile = Image.new('L', (size+2, size+2))
        tile.putdata([core[(y-1)%size][(x-1)%size] for y in range(size+2) for x in range(size+2)])
        scaled = tile.resize(((size+2)*32, (size+2)*32), Image.Resampling.BICUBIC)
        layers.append((list(scaled.crop((32,32,(size+1)*32,(size+1)*32)).resize((256,256), Image.Resampling.BICUBIC).getdata()),weight))
    texture = Image.new('L',(256,256))
    texture.putdata([int(sum(layer[i]*weight for layer,weight in layers)) for i in range(256*256)])
    texture.filter(ImageFilter.GaussianBlur(.6)).convert('RGB').save(DEST/'stroemung.png')
    mask = Image.new('RGBA', (256,256), 'white')
    mask.putalpha(texture.point(lambda v: min(255, int(90+v*.65))))
    mask.save(DEST/'stroemung_maske.png')
    print('Stroemungstextur erzeugt: lokale prozedurale Materialstudie.')


if __name__ == '__main__':
    main()
