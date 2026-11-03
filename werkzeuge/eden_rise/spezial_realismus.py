"""Stage original generated images and a verified CC0 library, never game data."""
from pathlib import Path
import hashlib
import json
import shutil
import urllib.request
import zipfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT/'docs/effekt-auswahl/status-labor'
SOURCES = LAB/'quellen/realismus-v3'
GENERATED = Path('C:/Users/DucNg/.codex/generated_images/01a14a5c-defd-7ac1-88da-ea3225a65e1f')
FILES = {'stahl':'exec-798aa25a-5de0-4dbd-95a9-a2834d4dec09.png',
         'wasser':'exec-f9da10af-7292-4ad7-bd88-46514298cf54.png',
         'licht':'exec-83e9859e-b6cc-49d1-ae0d-ae641599c73a.png'}
URL = 'https://kenney.nl/media/pages/assets/particle-pack/f8fe0f8cb8-1677578741/kenney_particle-pack.zip'


def main():
    SOURCES.mkdir(parents=True,exist_ok=True)
    out=LAB/'assets/realismus-v3';out.mkdir(parents=True,exist_ok=True)
    manifest={'version':3,'generated':[],'libraries':[]}
    for name,file in FILES.items():
        source=GENERATED/file
        shutil.copy2(source,SOURCES/(name+'-original.png'))
        shutil.copy2(source,out/(name+'.png'))
        im=Image.open(source)
        alpha=im.getchannel('A') if im.mode=='RGBA' else None
        record={'name':name,'origin':'OpenAI built-in image generation; single raster material, not simulation',
                'sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'size':im.size,'mode':im.mode,
                'alpha_range':alpha.getextrema() if alpha else None}
        manifest['generated'].append(record)
        print(name,im.size,im.mode,record['alpha_range'])
    archive=SOURCES/'kenney_particle-pack.zip'
    if not archive.exists():
        request=urllib.request.Request(URL,headers={'User-Agent':'Eden-Local-Asset-Research/1.0'})
        with urllib.request.urlopen(request,timeout=40) as response:
            data=response.read(20*1024*1024)
        archive.write_bytes(data)
    with zipfile.ZipFile(archive) as z:
        names=z.namelist()
        for name in ('light_02.png','flare_01.png','trace_04.png'):
            (out/('kenney-'+name)).write_bytes(z.read('PNG (Transparent)/'+name))
        for name in names:
            if name.lower().endswith('.txt') and ('license' in name.lower()):
                (SOURCES/'KENNEY-LICENSE.txt').write_bytes(z.read(name))
    manifest['libraries'].append({'author':'Kenney','url':'https://kenney.nl/assets/particle-pack','download':URL,'license':'CC0','used_files':['flare_01.png','trace_04.png'],
                                  'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
    for name in ('stahl','wasser','licht'):
        im=Image.open(out/(name+'.png'))
        box=im.getchannel('A').point(lambda x:255 if x>10 else 0).getbbox()
        manifest['generated'][list(FILES).index(name)]['crop']=box
        print('CROP',name,box)
    (SOURCES/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (LAB/'realismus-quellen.js').write_text('window.EDEN_REALISM_SOURCES = '+json.dumps(manifest,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')


if __name__=='__main__':main()
