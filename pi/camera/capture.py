import subprocess, time, pathlib
outdir=pathlib.Path('/data')
outdir.mkdir(parents=True, exist_ok=True)
def capture_clip(seconds=5):
    ts=time.strftime('%Y%m%d_%H%M%S')
    f=outdir/f'{ts}.mp4'
    cmd=['libcamera-vid','-t',str(seconds*1000),'-o',str(f)]
    subprocess.run(cmd,check=False)
    return str(f)
if __name__=='__main__':
    print(capture_clip())
