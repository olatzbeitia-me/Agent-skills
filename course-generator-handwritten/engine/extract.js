// node extract.js <L> : write <L>/beats.json from <L>/spec.js (say fields + SAY registry)
const fs=require('fs');const L=process.argv[2];const rows=[];const SAY={};
global.say=o=>Object.assign(SAY,o);
global.intro=(id,h,t)=>{rows.push([id,h,SAY[h]],[id,t,SAY[t]])};
global.recap=(id,r,o)=>{rows.push([id,r,SAY[r]],[id,o,SAY[o]])};
global.section=(id,l,c,specs)=>specs.forEach(s=>rows.push([id,s.b,s.say]));
eval(fs.readFileSync(`${L}/spec.js`,'utf8').replace(/^const (LECT|LAYERS) =/gm,'global.$1 =').replace(/^say\(/m,'global.say('));
const bad=rows.filter(r=>!r[2]);if(bad.length)throw 'missing say: '+bad.map(r=>r[1]);
const ids=rows.map(r=>r[1]);if(new Set(ids).size!==ids.length)throw 'dup beat ids';
fs.writeFileSync(`${L}/beats.json`,JSON.stringify(rows,null,0));
const w=rows.reduce((a,r)=>a+r[2].split(/\s+/).length,0);console.log(L,rows.length,'beats',w,'words ≈',(w/2.65/60).toFixed(1),'min');
