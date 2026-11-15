# Pluggable OpenAI-compatible /audio/speech TTS per beat -> audio/<beat>.wav (24 kHz mono, sped up by ATEMPO for ~1.2x pace)
import json,sys,os,time,subprocess,urllib.request,concurrent.futures as cf
K=os.environ['TTS_API_KEY']; MODEL=os.environ['TTS_MODEL']; VOICE=os.environ['TTS_VOICE']
URL=os.environ.get('TTS_URL','https://openrouter.ai/api/v1/audio/speech'); ATEMPO=os.environ.get('ATEMPO','1.12')
def synth(text,out):
    raw=out+'.pcm'
    body=json.dumps({"model":MODEL,"input":text,"voice":VOICE,"response_format":"pcm"}).encode()
    for a in range(8):
        try:
            r=urllib.request.Request(URL,body,{"Authorization":"Bearer "+K,"Content-Type":"application/json"})
            with urllib.request.urlopen(r,timeout=120) as f:
                ct=f.headers.get('Content-Type',''); d=f.read()
            if 'pcm' not in ct or len(d)<2000: raise Exception('bad '+ct+str(d[:200]))
            rate=[x.split('=')[1] for x in ct.split(';') if 'rate' in x][0]
            open(raw,'wb').write(d)
            subprocess.run(['ffmpeg','-y','-v','error','-f','s16le','-ar',rate,'-ac','1','-i',raw,'-af',f'silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo={ATEMPO}','-ar','24000',out],check=True)
            os.remove(raw); open(out+'.txt','w').write(text); return
        except Exception as e:
            msg=getattr(e,'read',lambda:b'')(); print('retry',out,a,e,msg[:200],flush=True); time.sleep(5*(a+1))
    raise SystemExit('FAILED '+out)
jobs=[]
for L in sys.argv[1:]:
    for sc,b,txt,*rest in json.load(open(f'{L}/beats.json')):
        out=f'{L}/audio/{b}.wav'
        t=rest[0] if rest else txt
        if not (os.path.exists(out) and os.path.exists(out+'.txt') and open(out+'.txt').read()==t): jobs.append((t,out))
print(len(jobs),'jobs',flush=True)
with cf.ThreadPoolExecutor(int(os.environ.get('PAR','4'))) as ex:
    for _ in ex.map(lambda j:synth(*j),jobs): pass
import soundfile as sf
for L in sys.argv[1:]:
    d={b:round(sf.info(f'{L}/audio/{b}.wav').duration,3) for sc,b,*_ in json.load(open(f'{L}/beats.json'))}
    json.dump(d,open(f'{L}/audio/durs.json','w')); print(L,'speech min',round(sum(d.values())/60,2),flush=True)
