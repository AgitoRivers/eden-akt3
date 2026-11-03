# -*- coding: utf-8 -*-
"""Prepare local IlluGen PREVIEW masks, never label them as production exports.

Uses Pillow already supplied by ComfyUI's Python; installs nothing.
Only the named local output directory is written. Original presets and sprites
are read and copied; no game saves or configuration files are accessed.
"""
from pathlib import Path
import argparse
import hashlib
import io
import json
import shutil
import struct
from PIL import Image, ImageChops, ImageFilter, ImageStat

ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'docs'/'effekt-auswahl'
NAMES=['swipe_dissolve','sword_slash_3D','painted_style_golden_shockwave',
       'electric_arc_4','electric_arc_5','lightning_sheet','erosion_based_lightning',
       'stylized_flame_flipbook','stylized_smoke_trail','waterfall_3D_2',
       'shield_gradient','lense_flare','tornado_3D']

def integer(data,key,default):
    at=data.find(key.encode(),0,500)
    if at<0:return default
    at+=len(key)
    return struct.unpack_from('<Q',data,at+1)[0] if data[at]==5 else default

def without_flecks(mask,min_area=60):
    """Remove isolated small islands rather than introduce a point-cloud pattern."""
    width,height=mask.size
    pixels=bytearray(mask.tobytes());seen=bytearray(len(pixels))
    for start,value in enumerate(pixels):
        if not value or seen[start]:continue
        stack=[start];seen[start]=1;component=[]
        while stack:
            at=stack.pop();component.append(at);x,y=at%width,at//width
            for dy in (-1,0,1):
                yy=y+dy
                if not 0<=yy<height:continue
                for dx in (-1,0,1):
                    xx=x+dx
                    if not 0<=xx<width:continue
                    nxt=yy*width+xx
                    if pixels[nxt] and not seen[nxt]:seen[nxt]=1;stack.append(nxt)
        xs=[at%width for at in component];ys=[at//width for at in component]
        if len(component)<min_area or max(max(xs)-min(xs),max(ys)-min(ys))<16:
            for at in component:pixels[at]=0
    return Image.frombytes('L',mask.size,bytes(pixels))

def build(source):
    manifest={}
    for folder in ('assets','quellen/vorlagen-vorschauen','quellen/illugen-projekte'):
        (DEST/folder).mkdir(parents=True,exist_ok=True)
    for name in NAMES:
        path=source/(name+'.illugen');data=path.read_bytes()
        start=data.find(b'\xff\xd8\xff');end=data.find(b'\xff\xd9',start)+2
        if start<0 or end<=start:raise ValueError('No embedded preview: '+name)
        jpg=data[start:end]
        picture=Image.open(io.BytesIO(jpg)).convert('RGB')
        count=integer(data,'frame_count',64);fps=integer(data,'frame_rate',30)
        at=data.find(b'flipbook_col_row',0,500)
        if at<0:raise ValueError('Preview layout missing: '+name)
        at+=len('flipbook_col_row')
        cols,rows=struct.unpack_from('<QQ',data,at+1) if data[at]==6 else (8,8)
        if not (1<=cols<=32 and 1<=rows<=32 and 1<=count<=cols*rows):raise ValueError('Invalid preview layout: '+name)
        if picture.width%cols or picture.height%rows:raise ValueError('Preview dimensions mismatch: '+name)
        fw,fh=picture.width//cols,picture.height//rows
        size=192 if count>1 else 320
        result=Image.new('RGBA',(size*cols,size*rows))
        for i in range(count):
            frame=picture.crop((i%cols*fw,i//cols*fh,(i%cols+1)*fw,(i//cols+1)*fh))
            r,g,b=frame.split();lum=ImageChops.lighter(ImageChops.lighter(r,g),b)
            bg=max(ImageStat.Stat(frame.crop((0,0,max(1,fw//12),fh))).median)
            base=min(80,max(7,int(bg)+5))
            lum=lum.point(lambda p:max(0,min(255,int((p-base)*255/max(1,255-base)))))
            lum=lum.resize((size,size),Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(1.8 if 'flame' in name else .65))
            lum=lum.point(lambda p:0 if p<18 else min(255,int((p-18)*255/237)))
            if any(word in name for word in ('electric','lightning','flame','waterfall')):
                lum=without_flecks(lum)
            rgba=Image.new('RGBA',(size,size),'white');rgba.putalpha(lum)
            result.paste(rgba,(i%cols*size,i//cols*size))
        target=DEST/'assets'/(name+'.png');result.save(target,optimize=True)
        (DEST/'quellen/vorlagen-vorschauen'/(name+'.jpg')).write_bytes(jpg)
        shutil.copy2(path,DEST/'quellen/illugen-projekte'/path.name)
        manifest[name]={'file':'assets/'+target.name,'columns':cols,'rows':rows,'frames':count,'fps':fps,
                        'width':result.width,'height':result.height,'source':str(path),
                        'sha256':hashlib.sha256(data).hexdigest(),
                        'origin':'IlluGen bundled preset thumbnail','production_export':False,
                        'preview_frame_pixels':size,
                        'processing':'Luminance mask, neutral background removed, smoothed; isolated small islands removed for lightning/fire/water; preview only'}
    for pose in ('idle','hurt','windup','guard','weakened'):
        shutil.copy2(ROOT/'module/eden_rise/kampf/Thief'/(pose+'.webp'),DEST/'assets'/('figur_'+pose+'.webp'))
    (DEST/'quellen/illugen-vorschauen.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'{len(manifest)} IlluGen preview masks built. Production exports: 0.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vorlagen',type=Path,default=Path(r'Y:\JangaFX\IlluGen\presets_2_0_0'))
    args=parser.parse_args();build(args.vorlagen)
