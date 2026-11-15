import json,numpy as np,soundfile as sf,subprocess,sys,os
L,OUT=sys.argv[1],sys.argv[2]
beats=json.load(open(f'{L}/beats.json')); SC=list(dict.fromkeys(r[0] for r in beats)); parts=[]; srt=[]; t0=0
for s in SC:
    info=json.load(open(f'{L}/timing/{s}.json')); n=int(np.ceil(info['dur']*30))/30
    sr=24000; buf=np.zeros(int(round(n*sr)),dtype=np.float32)
    for b,v in info['beats'].items():
        a,_=sf.read(f'{L}/audio/{b}.wav',dtype='float32'); i=int(v['s']*sr); buf[i:i+len(a)]+=a[:len(buf)-i]
        srt.append((t0+v['s'],t0+v['s']+v['d'],next(r[2] for r in beats if r[1]==b)))
    parts.append(buf); t0+=n
sf.write(f'{L}/vo.wav',np.concatenate(parts),24000)
f=lambda x:'%02d:%02d:%02d,%03d'%(x//3600,x%3600//60,x%60,(x%1)*1000)
open(OUT[:-4]+'.srt','w').write(''.join(f'{i+1}\n{f(a)} --> {f(b)}\n{t}\n\n' for i,(a,b,t) in enumerate(srt)))
open(f'{L}/list.txt','w').write(''.join(f"file 'parts/{s}.mp4'\n" for s in SC))
subprocess.run(f'ffmpeg -y -v error -f concat -safe 0 -i {L}/list.txt -c copy {L}/video_only.mp4',shell=True,check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i',f'{L}/video_only.mp4','-i',f'{L}/vo.wav','-i',OUT[:-4]+'.srt','-map','0:v','-map','1:a','-map','2','-c:v','copy','-c:a','aac','-b:a','160k','-af','loudnorm=I=-16:TP=-1.5','-c:s','mov_text','-metadata:s:s:0','language=eng','-shortest',OUT],check=True)
print('OK',OUT)
