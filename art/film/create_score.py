# SPDX-License-Identifier: MIT
"""An original, quiet ambient score for The Unfolding. No samples used."""
import wave
from pathlib import Path
import numpy as np

sr, duration = 44100, 28
t = np.arange(sr * duration) / sr
left = np.zeros_like(t)
right = np.zeros_like(t)

def swell(start, end, attack=2, release=3):
    return np.clip((t-start)/attack, 0, 1) * np.clip((end-t)/release, 0, 1)

for f, gain, phase in [(73.416,.12,0),(110,.055,.2),(146.832,.045,.4),(220,.02,.7)]:
    env=swell(0,28,4,4)
    tone=np.sin(2*np.pi*f*t+phase) + .15*np.sin(2*np.pi*f*2*t)
    left += tone * gain * env
    right += (np.sin(2*np.pi*(f+.045)*t+phase)+.15*np.sin(2*np.pi*f*2*t)) * gain * env
for start,end,f in [(6,13,185),(10,19,277.18),(17,25,246.94),(22,28,293.665)]:
    env=swell(start,end,2.5,3.5)*.026
    left += env*np.sin(2*np.pi*f*t)
    right += env*np.sin(2*np.pi*(f+.12)*t)
for start,f,gain in [(7.4,587.33,.055),(11.9,440,.04),(18.7,659.255,.045),(23.7,587.33,.05),(24.5,880,.025)]:
    u=np.maximum(t-start,0)
    env=(t>=start)*(1-np.exp(-u*12))*np.exp(-u/2.4)*gain
    bell=np.sin(2*np.pi*f*u)+.22*np.sin(2*np.pi*f*2.003*u)*np.exp(-u)
    left+=env*bell
    right+=env*(np.sin(2*np.pi*f*u+.12)+.22*np.sin(2*np.pi*f*2.003*u)*np.exp(-u))
# A soft exhalation at the sacrifice, rather than an explosive impact.
rng=np.random.default_rng(27)
noise=rng.normal(0,1,len(t))
noise=np.convolve(noise,np.ones(220)/220,mode='same')
env=np.exp(-((t-7.4)/1.15)**2)*.27
left+=env*noise; right+=env*np.roll(noise,550)
stereo=np.column_stack([left,right])
stereo*=np.clip(t/.8,0,1)[:,None]*np.clip((28-t)/1.3,0,1)[:,None]
pcm=(np.clip(stereo,-.9,.9)*32767).astype('<i2')
out=Path(__file__).resolve().parent / '(Footage)' / 'The-Unfolding-score.wav'
out.parent.mkdir(parents=True, exist_ok=True)
with wave.open(str(out),'wb') as w:
    w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(pcm.tobytes())
print(out)
