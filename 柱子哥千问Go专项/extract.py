from pathlib import Path
import subprocess,json,re
from PIL import Image,ImageDraw
p=Path(__file__).parent.resolve(); d=p/'evidence'; src=p/'media/7695964257132891434.mp4'
times=[i*129.74/29 for i in range(30)]; nums=[round(t*60) for t in times]
expr='+'.join('eq(n,%d)'%n for n in nums)
with (d/'frames.log').open('w') as log:
 subprocess.run(['/Users/USER/.local/bin/ffmpeg','-hide_banner','-i',str(src),'-vf',"select='"+expr+"',scale=640:-2,showinfo",'-vsync','0','-q:v','4',str(d/'frame-%03d.jpg')],stdout=subprocess.DEVNULL,stderr=log,check=True)
pts=[float(x) for x in re.findall(r'pts_time:([\d.]+)',(d/'frames.log').read_text())];fs=sorted(d.glob('frame-*.jpg'));assert len(fs)==30
for k in range(5):
 canvas=Image.new('RGB',(1920,800),'white');draw=ImageDraw.Draw(canvas)
 for j,f in enumerate(fs[k*6:k*6+6]):
  x=j%3*640;y=j//3*400;canvas.paste(Image.open(f),(x,y+30));draw.text((x+3,y+3),f'PTS {pts[k*6+j]:.3f}s',fill='black')
 canvas.save(d/f'sheet-{k+1}.jpg',quality=90)
(d/'coverage.json').write_text(json.dumps({'pts':pts[:30],'frames':list(map(str,fs)),'method':'30 fullspan sampled decoded frames with original PTS; not continuous viewing','viewed':False},indent=2))
print('30 frames ready')
