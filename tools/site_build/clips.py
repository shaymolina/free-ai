"""חיתוך סרטוני מסך לקליפים קצרים: קטעים, האצה, טשטוש (פיקסלים), חיתוך מסגרת, הדבקה.
segment = (start, end, speed, crop(x1,y1,x2,y2), [blur boxes (x1,y1,x2,y2[,t0,t1 יחסית למקור])])"""
import subprocess, tempfile, os

def _seg(src, s, out, W, H):
    start, end, speed, crop, blurs = s
    f, last = [], '0:v'
    f.append(f"[{last}]trim={start}:{end},setpts=PTS-STARTPTS[v0]"); last = 'v0'
    for i, b in enumerate(blurs):
        x1, y1, x2, y2 = b[:4]; w, h = x2 - x1, y2 - y1
        en = f":enable='between(t,{b[4]-start},{b[5]-start})'" if len(b) > 4 else ''
        f.append(f"[{last}]split[a{i}][b{i}];[b{i}]crop={w}:{h}:{x1}:{y1},scale={max(2,w//14)}:{max(2,h//14)},scale={w}:{h}:flags=neighbor[p{i}];[a{i}][p{i}]overlay={x1}:{y1}{en}[o{i}]")
        last = f'o{i}'
    x1, y1, x2, y2 = crop
    f.append(f"[{last}]crop={x2-x1}:{y2-y1}:{x1}:{y1},setpts=PTS/{speed},scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=0x1f1f1f,fps=30,format=yuv420p[out]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', ';'.join(f), '-map', '[out]', '-an',
                    '-c:v', 'libx264', '-crf', '30', '-preset', 'medium', out], check=True)

def make(src, segs, out, W=1280, H=842):
    d = tempfile.mkdtemp()
    parts = []
    for i, s in enumerate(segs):
        p = os.path.join(d, f'{i}.mp4'); _seg(src, s, p, W, H); parts.append(p)
    lst = os.path.join(d, 'l.txt'); open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', out], check=True)
    print(out)
