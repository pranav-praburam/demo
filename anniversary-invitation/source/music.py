import numpy as np, sys, wave
SR=44100; DUR=float(sys.argv[2]); N=int(SR*DUR); rng=np.random.default_rng(3)
out=np.zeros((N,2))
def ks(freq, dur, damp=0.996, bright=0.5):
    n=int(SR*dur); p=int(SR/freq); buf=rng.uniform(-1,1,p)
    buf=np.convolve(buf,[bright,1-bright],'same'); y=np.zeros(n)
    for i in range(n):
        y[i]=buf[i%p]; buf[i%p]=damp*0.5*(buf[i%p]+buf[(i+1)%p])
    return y
def add(sig,t,gain,pan=0.5):
    i=int(t*SR); j=min(N,i+len(sig))
    if i>=N: return
    out[i:j,0]+=sig[:j-i]*gain*(1-pan); out[i:j,1]+=sig[:j-i]*gain*pan
Sa=146.83
# tanpura: Pa Sa' Sa' Sa cycle with buzzy harmonics, precompute 4 strings
def tanpura(f,dur=3.2):
    t=np.arange(int(SR*dur))/SR
    s=sum((1/k**0.9)*np.sin(2*np.pi*f*k*t+rng.uniform(0,6))*(1+0.3*np.sin(2*np.pi*(0.3+0.1*k)*t)) for k in range(1,14))
    return s*np.exp(-t/1.6)*(1-np.exp(-t*60))
strings=[tanpura(Sa*0.75),tanpura(Sa),tanpura(Sa),tanpura(Sa/2)]
t=0; k=0
while t<DUR:
    add(strings[k%4],t,0.035,0.35+0.1*(k%4)); t+=0.8; k+=1
# melody: Mohanam (S R2 G3 P D2) in upper octave, veena-like plucks
ratio={'S':1,'R':9/8,'G':5/4,'P':3/2,'D':5/3,"S'":2,"R'":9/4,"G'":5/2,'d':5/6,'p':3/4}
phr=["G P D S' . D P G","R G P G R S . .","S R G P D P G R","G . R S d S . .",
     "P D S' R' G' R' S' D","P . G R S R G .","G P D P G R S .","S . . . . . . ."]
notes=[n for ph in phr for n in ph.split()]
cache={}
beat=0.62; t0=2.0; i=0
while t0+i*beat<DUR-3:
    n=notes[i%len(notes)]
    if n!='.':
        f=Sa*2*ratio[n]
        if n not in cache: cache[n]=ks(f,2.2,0.9975,0.55)
        add(cache[n],t0+i*beat,0.16,0.55)
        add(cache[n]*0.5,t0+i*beat+0.012,0.06,0.3)
    i+=1
# temple bell (inharmonic partials)
def bell(f,dur=5):
    t=np.arange(int(SR*dur))/SR
    return sum(a*np.sin(2*np.pi*f*r*t)*np.exp(-t/(dur*d)) for r,a,d in [(1,1,.5),(2.4,.6,.3),(3.0,.4,.25),(4.5,.3,.18),(5.9,.2,.12)])
add(bell(Sa*4),0.05,0.12); add(bell(Sa*4),DUR-4.5,0.10)
# reverb
ir_t=np.arange(int(SR*2.2))/SR; ir=rng.normal(0,1,len(ir_t))*np.exp(-ir_t/0.55); ir/=np.abs(ir).sum()/6
from numpy.fft import rfft, irfft
L=N+len(ir); nf=1<<(L-1).bit_length()
wet=np.stack([irfft(rfft(out[:,c],nf)*rfft(ir,nf),nf)[:N] for c in range(2)],1)
mix=out*0.75+wet*0.45
fade=np.ones(N); f=int(SR*2.5); fade[-f:]=np.linspace(1,0,f); fade[:int(SR*0.3)]=np.linspace(0,1,int(SR*0.3))
mix*=fade[:,None]; mix/=np.abs(mix).max()/0.85
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((mix*32767).astype(np.int16).tobytes()); w.close()
