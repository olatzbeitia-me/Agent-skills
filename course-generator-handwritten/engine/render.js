// node render.js <LectureDir> still <scene> b10:4.5 end | node render.js <LectureDir> video <scene>
const {chromium}=require('playwright');const fs=require('fs');const {spawn}=require('child_process');
(async()=>{
 const [L,mode,scene,...rest]=process.argv.slice(2);
 const durs=JSON.parse(fs.readFileSync(`${L}/audio/durs.json`));
 for(const d of ['timing','parts','stills'])fs.mkdirSync(`${L}/${d}`,{recursive:true});
 const b=await chromium.launch();const p=await b.newPage({viewport:{width:1920,height:1080}});
 p.on('pageerror',e=>console.error('PAGEERR',scene,e.message)); p.on('console',m=>{if(m.text().includes('WORDMISS'))console.error(m.text())});
 await p.goto('file://'+__dirname+'/engine.html#'+L);await p.evaluate(()=>document.fonts.ready);
 await p.evaluate(()=>document.fonts.load('40px Hand'));
 const info=await p.evaluate(([s,d])=>loadScene(s,d,null),[scene,durs]);
 fs.writeFileSync(`${L}/timing/${scene}.json`,JSON.stringify(info));
 if(mode==='still'){for(const spec of rest){
     const t=spec==='end'?info.dur-0.6:(()=>{const [bb,o]=spec.split(':');return o==='e'?info.beats[bb].s+info.beats[bb].d-0.05:info.beats[bb].s+parseFloat(o)})();
     await p.evaluate(t=>setTime(t),t);await p.screenshot({path:`${L}/stills/${scene}_${spec.replace(':','_')}.jpg`,type:'jpeg',quality:80});}
 } else {
   const fps=30,N=Math.ceil(info.dur*fps);
   const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',''+fps,'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r',''+fps,`${L}/parts/${scene}.tmp.mp4`]);
   const ok=new Promise(r=>ff.on('close',r));
   for(let i=0;i<N;i++){await p.evaluate(t=>setTime(t),i/fps);const buf=await p.screenshot({type:'jpeg',quality:90});
     if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
   ff.stdin.end();const code=await ok;if(code===0)fs.renameSync(`${L}/parts/${scene}.tmp.mp4`,`${L}/parts/${scene}.mp4`);console.log(L,scene,'done',code);
 }
 await b.close();
})();
