/* Bake transparent PREVIEW flipbooks. No game or IlluGen process is controlled.
 * Uses the existing bundled @napi-rs/canvas runtime, never installs packages.
 * Run: node effekt_export.cjs --canvas-module <absolute package directory>
 */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'../..'),gallery=path.join(root,'docs/effekt-auswahl');
const option=process.argv.indexOf('--canvas-module');
if(option<0||!process.argv[option+1])throw Error('Specify the existing canvas package with --canvas-module.');
const {createCanvas,loadImage}=require(path.resolve(process.argv[option+1]));
const catalog=JSON.parse(fs.readFileSync(path.join(gallery,'katalog.json'),'utf8'));
const out=path.join(gallery,'assets/varianten');fs.mkdirSync(out,{recursive:true});
const failures=[];
const environment={console,window:{},document:{createElement:tag=>{if(tag!=='canvas')throw Error('Unexpected element');return createCanvas(1,1);}},Promise,Map,Set,Math,Number,String,Array,Object};
environment.window=environment;
environment.Image=class {
  set src(src){loadImage(path.join(gallery,src)).then(im=>{this.native=im;this.width=im.width;this.height=im.height;this.onload();},()=>this.onerror());}
};
// The browser renderer draws the supplied Image directly. Replace that wrapper
// at the boundary with native loaded images, leaving all effect recipes intact.
const nativeDraw=createCanvas(1,1).getContext('2d').drawImage;
const prototype=Object.getPrototypeOf(createCanvas(1,1).getContext('2d'));
const original=prototype.drawImage;
prototype.drawImage=function(image,...args){return original.call(this,image.native||image,...args);};
vm.createContext(environment);
vm.runInContext(fs.readFileSync(path.join(gallery,'effekte.js'),'utf8'),environment);

async function main(){
 const loaded=await environment.EdenFxPreview.init(catalog);
 if(loaded.failed.length)throw Error('Missing preview inputs: '+loaded.failed.length);
 const cols=6,rows=4,count=24,fw=256,fh=196,manifest={schema:1,status:'Transparent Canvas preview bake; NOT an IlluGen production export',columns:cols,rows,frames:count,frame_width:fw,frame_height:fh,variants:{}};
 let done=0;
 for(const e of catalog.effects){
  for(const variant of e.variants){
   const frame=createCanvas(fw,fh),atlas=createCanvas(cols*fw,rows*fh),g=atlas.getContext('2d');
   const pose={stage:'neutral',target:variant.target,subtype:''};
   const signatures=new Set();let nonempty=0;
   for(let i=0;i<count;i++){
    environment.EdenFxPreview.renderLayer(frame,e,variant.index,i/(count-1),pose);
    const pixels=frame.getContext('2d').getImageData(0,0,fw,fh).data;
    let countAlpha=0;for(let j=3;j<pixels.length;j+=4)if(pixels[j]>5)countAlpha++;
    if(countAlpha)nonempty++;
    signatures.add(crypto.createHash('sha256').update(pixels).digest('hex'));
    g.drawImage(frame,(i%cols)*fw,Math.floor(i/cols)*fh);
   }
   if(nonempty<4||signatures.size<3)failures.push(variant.id);
   const file=path.join(out,variant.id+'.png');
   fs.writeFileSync(file,atlas.toBuffer('image/png'));
   manifest.variants[variant.id]={file:'assets/varianten/'+variant.id+'.png',frames:count,columns:cols,rows,frame_width:fw,frame_height:fh,duration_ms:variant.duration_ms,nonempty_frames:nonempty,distinct_frames:signatures.size,production_export:false};
   done++;
  }
  console.log(`${e.id}: ${done} / ${catalog.variant_count} preview flipbooks baked`);
 }
 fs.writeFileSync(path.join(gallery,'quellen/vorschau-exporte.json'),JSON.stringify(manifest,null,2)+'\n');
 console.log(JSON.stringify({variants:done,frames:done*count,invalid:failures,scope:'Canvas preview bakes, not IlluGen production exports'}));
 if(failures.length)process.exitCode=1;
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
