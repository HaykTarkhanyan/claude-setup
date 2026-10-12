"""Synthesize the backing beat for the Armenian verse (the box at the top of the handout).

Boom-bap at 88 BPM in D minor, 22 bars (~60 s):
  bars 1-4    intro: muffled keys, vinyl crackle, a duduk-like reed lead in D harmonic minor
  bars 5-18   full beat for the 12 verse lines (one line per bar = 16th-note flow)
  bar 19      drop: keys only, room for the punchline
  bar 20      crash, beat back for one bar
  bars 21-22  outro: lead returns over A7 -> Dm, ends in a tape stop

Everything is synthesized from oscillators and seeded noise - no samples, nothing downloaded.
Writes assets/verse-beat.mp3 (ffmpeg, 160 kbps); build_standalone.py inlines it into the handout.

Usage (9-40 s on this laptop depending on load, plus ~30 s the first time uv builds the env):
    uv run --no-project --with numpy==2.5.4 --with scipy==1.18.1 python non_essential/make_beat.py
"""
import logging
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

START = time.perf_counter()
REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "verse-beat.mp3"

(REPO / "logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(REPO / "logs" / "make_beat.log", encoding="utf-8"),
    ],
)
log = logging.getLogger(__name__)

SR = 44100
BPM = 88
BEAT = 60 / BPM
BAR = 4 * BEAT
STEP = BEAT / 4  # one 16th note
SWING = 0.18 * STEP  # offbeat 16ths land late
N_BARS = 22
rng = np.random.default_rng(509)

# D minor: i9 - VImaj7 - iv9 - V7b9, one chord per bar (MIDI note numbers)
VOICINGS = [[53, 57, 60, 64], [53, 57, 62, 65], [53, 58, 62, 69], [55, 61, 64, 70]]
ROOTS = [38, 34, 31, 33]  # D2 Bb1 G1 A1
CHORD_OVERRIDE = {20: 3, 21: 0}  # outro: A7b9 resolves to Dm9

# reed lead, (start beat, length in beats, MIDI); D harmonic minor, augmented second Bb-C#
INTRO_PHRASE = [
    (0.5, 2.0, 69), (2.5, 0.5, 70), (3.0, 1.0, 69),
    (4.0, 1.0, 67), (5.0, 0.5, 65), (5.5, 0.5, 64), (6.0, 2.0, 65),
    (8.0, 0.5, 62), (8.5, 0.5, 65), (9.0, 1.5, 69), (10.5, 0.5, 70), (11.0, 1.0, 73),
    (12.0, 1.0, 74), (13.0, 0.5, 73), (13.5, 0.5, 70), (14.0, 2.0, 69),
]
OUTRO_PHRASE = [(0.0, 0.5, 62), (0.5, 0.5, 65), (1.0, 1.5, 69), (2.5, 0.5, 70), (3.0, 1.0, 73), (4.0, 3.5, 74)]

INTRO, VERSE, DROP, RETURN, OUTRO = range(0, 4), range(4, 18), 18, 19, range(20, 22)
TAPE_STOP_AT = 21 * BAR + 2 * BEAT  # last bar, beat 3
TAPE_STOP_LEN = 1.4
TOTAL = TAPE_STOP_AT + TAPE_STOP_LEN + 0.3
N = int(TOTAL * SR)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def decay(n, tau):
    return np.exp(-np.arange(n) / SR / tau)


def filt(x, kind, freq, order=2):
    return sosfilt(butter(order, freq, kind, fs=SR, output="sos"), x)


def noise(n):
    return rng.standard_normal(n)


def kick():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    pitch = 45 + 75 * np.exp(-t / 0.04)  # 120 -> 45 Hz sweep
    body = np.sin(2 * np.pi * np.cumsum(pitch) / SR) * decay(n, 0.22)
    click = filt(noise(n), "high", 2000) * decay(n, 0.004) * 0.4
    return np.tanh(1.8 * (body + click))


def snare():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    rattle = filt(noise(n), "band", [1200, 7000]) * decay(n, 0.07)
    tone = np.sin(2 * np.pi * 185 * t) * decay(n, 0.05)
    return 0.8 * rattle + 0.6 * tone


def hat(open_hat=False):
    n = int((0.35 if open_hat else 0.06) * SR)
    return filt(noise(n), "high", 7000, 4) * decay(n, 0.12 if open_hat else 0.018)


def crash():
    n = int(2.2 * SR)
    return filt(noise(n), "high", 3500) * decay(n, 0.7)


def epiano(m, dur):
    """FM electric piano: bright attack that mellows out."""
    f = hz(m)
    n = int((dur + 0.6) * SR)
    t = np.arange(n) / SR
    index = 1.6 * np.exp(-t / 0.25) + 0.15
    tone = np.sin(2 * np.pi * f * t + index * np.sin(2 * np.pi * f * t))
    tine = 0.15 * np.sin(2 * np.pi * 4 * f * t) * decay(n, 0.05)
    amp = np.minimum(1, t / 0.004) * decay(n, 1.4) * np.clip((dur + 0.6 - t) / 0.6, 0, 1)
    return (tone + tine) * amp


def bass(m, dur):
    """Sub sine, saturated so laptop speakers still get the harmonics."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    amp = np.minimum(1, t / 0.006) * np.clip((dur - t) / 0.03, 0, 1) * decay(n, 1.5)
    return np.tanh(2.2 * np.sin(2 * np.pi * hz(m) * t)) * amp


def reed(notes, start):
    """Duduk-like legato line: glides between notes, vibrato that grows into each note, breath noise."""
    freq = np.zeros(N)
    gate = np.zeros(N)
    since = np.full(N, 10.0)  # seconds since the current note began
    for b, length, m in notes:
        i0 = int((start + b * BEAT) * SR)
        i1 = int((start + (b + length * 0.95) * BEAT) * SR)
        freq[i0:i1] = hz(m)
        gate[i0:i1] = 1
        since[i0:i1] = np.arange(i1 - i0) / SR
    filled = np.where(freq > 0, np.arange(N), 0)
    np.maximum.accumulate(filled, out=filled)
    freq = freq[filled]
    freq[freq == 0] = hz(notes[0][2])
    freq = filt(freq, "low", 6, 1)  # ~25 ms portamento
    t = np.arange(N) / SR
    depth = 0.007 * np.clip((since - 0.25) / 0.4, 0, 1)
    phase = 2 * np.pi * np.cumsum(freq * (1 + depth * np.sin(2 * np.pi * 5.3 * t))) / SR
    tone = sum((0.6 if k % 2 == 0 else 1.0) / k**1.3 * np.sin(k * phase) for k in range(1, 11))
    breath = filt(noise(N), "band", [800, 3000]) * 0.08
    return (filt(tone, "low", 2400) + breath) * np.clip(filt(gate, "low", 3, 1), 0, 1)


def reverb_ir(seconds=1.8):
    n = int(seconds * SR)
    ir = filt(noise(n), "low", 5000) * decay(n, 0.45)
    ir[: int(0.02 * SR)] = 0  # 20 ms pre-delay
    return ir / np.sqrt(np.sum(ir**2))


def place(track, x, t, gain=1.0):
    i = int(round(t * SR))
    j = min(len(track), i + len(x))
    if j > i:
        track[i:j] += gain * x[: j - i]


def at(bar, step):
    return bar * BAR + step * STEP + (SWING if step % 2 else 0)


tracks = {name: np.zeros(N) for name in
          ["kick", "snare", "hats", "crash", "bass", "keys_lofi", "keys", "kick_env", "fx"]}
K, S = kick(), snare()

for bar in range(N_BARS):
    chord = CHORD_OVERRIDE.get(bar, bar % 4)
    voicing, root = VOICINGS[chord], ROOTS[chord]
    full = bar in VERSE or bar == RETURN

    # keys: muffled sustained chord in intro/outro, two stabs per bar otherwise
    if bar in INTRO or bar in OUTRO:
        for m in voicing:
            place(tracks["keys_lofi"], epiano(m, 3.8 * BEAT), at(bar, 0), 0.9)
    else:
        for m in voicing:
            place(tracks["keys"], epiano(m, 1.4 * BEAT), at(bar, 0))
            place(tracks["keys"], epiano(m, 1.5 * BEAT), at(bar, 10), 0.6)

    if full:
        kicks = [0, 6, 9, 11] if bar % 4 == 3 else [0, 6, 10]
        for st in kicks:
            place(tracks["kick"], K, at(bar, st))
            place(tracks["kick_env"], decay(int(0.3 * SR), 0.12), at(bar, st))
        for st, nxt in zip(kicks, kicks[1:] + [16]):
            note = root + (12 if bar % 2 else 7) if st == kicks[-1] else root
            place(tracks["bass"], bass(note, (nxt - st) * STEP), at(bar, st))
        for st in (4, 12):
            place(tracks["snare"], S, at(bar, st))
        if bar % 4 == 1:
            place(tracks["snare"], S, at(bar, 15), 0.25)  # ghost notes
        if bar % 4 == 3:
            place(tracks["snare"], S, at(bar, 7), 0.2)
        for st in range(0, 16, 2):
            if st == 14 and bar % 4 == 3:
                place(tracks["hats"], hat(open_hat=True), at(bar, st), 0.8)
                continue
            accent = 0.9 if st % 4 == 0 else 0.6
            place(tracks["hats"], hat(), at(bar, st), accent * rng.uniform(0.85, 1.0))
        if bar % 2:
            place(tracks["hats"], hat(), at(bar, 15), 0.35)

    if bar in OUTRO:  # kick on the one, nothing else
        place(tracks["kick"], K, at(bar, 0), 0.8)

# intro -> verse: snare roll and a noise riser, crash on the downbeat; crash again when the beat returns
for i, st in enumerate((12, 13, 14, 15)):
    place(tracks["snare"], S, at(3, st), 0.35 + 0.18 * i)
riser_n = int(2 * BEAT * SR)
riser = filt(noise(riser_n), "band", [2000, 8000]) * np.linspace(0, 1, riser_n) ** 2
place(tracks["fx"], riser, at(3, 8), 0.35)
for bar in (VERSE[0], RETURN):
    place(tracks["crash"], crash(), at(bar, 0))

lead = reed(INTRO_PHRASE, 0.0) + reed(OUTRO_PHRASE, OUTRO[0] * BAR)

# vinyl crackle: sparse clicks plus a little hiss
clicks = np.where(rng.random(N) < 0.0004, rng.choice([-1.0, 1.0], N), 0.0)
crackle = filt(clicks, "band", [1000, 6000]) * 3 + filt(noise(N), "low", 4000) * 0.05

# keys: muffled in intro/outro, open in the verse, ducked by the kick (sidechain pump)
keys = filt(tracks["keys_lofi"], "low", 900) + filt(tracks["keys"], "low", 3500)
keys *= 1 - 0.35 * np.clip(tracks["kick_env"], 0, 1)

# levels balanced by measured band energy, not by ear: room and laptop speakers lose the sub,
# so kick and bass sit lower and snare, hats, and keys higher than a headphone mix would want
center = tracks["kick"] * 0.7 + tracks["bass"] * 0.35 + tracks["snare"] * 0.75 + tracks["fx"]
delay = int(0.011 * SR)
keys_r = np.concatenate([np.zeros(delay), keys[:-delay]])  # Haas widening
send = tracks["snare"] * 0.3 + keys * 0.25 + lead * 0.45 + tracks["crash"] * 0.1
wet_l = fftconvolve(send, reverb_ir())[:N]
wet_r = fftconvolve(send, reverb_ir())[:N]

left = center + tracks["hats"] * 0.32 + keys * 0.4 + lead * 0.3 + tracks["crash"] * 0.22 + crackle * 0.025 + wet_l * 0.22
right = center + tracks["hats"] * 0.4 + keys_r * 0.4 + lead * 0.24 + tracks["crash"] * 0.22 + crackle * 0.025 + wet_r * 0.22
mix = np.stack([left, right], axis=1)

# tape stop: playback rate falls from 1 to 0, then silence
i0 = int(TAPE_STOP_AT * SR)
n_stop = int(TAPE_STOP_LEN * SR)
rate = (1 - np.arange(n_stop) / n_stop) ** 1.5
pos = i0 + np.cumsum(rate)
idx = np.arange(N)
for ch in range(2):
    mix[i0:i0 + n_stop, ch] = np.interp(pos, idx, mix[:, ch])
mix[i0 + n_stop:] = 0
mix[i0 + n_stop - int(0.05 * SR):i0 + n_stop] *= np.linspace(1, 0, int(0.05 * SR))[:, None]

if not np.all(np.isfinite(mix)):
    raise ValueError("mix contains NaN or inf - a synth function is broken")
mix /= np.max(np.abs(mix))
mix = np.tanh(1.3 * mix) / np.tanh(1.3)  # soft-clip master
mix *= 10 ** (-1 / 20)  # peak at -1 dBFS
rms_db = 20 * np.log10(np.sqrt(np.mean(mix[: i0] ** 2)))
log.info(f"Rendered {TOTAL:.1f} s, {N_BARS} bars at {BPM} BPM; peak -1.0 dBFS, RMS {rms_db:.1f} dBFS")

with tempfile.TemporaryDirectory() as tmp:
    wav = Path(tmp) / "beat.wav"
    wavfile.write(wav, SR, (mix * 32767).astype(np.int16))
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-codec:a", "libmp3lame", "-b:a", "160k", str(OUT)],
        check=True,
    )
log.info(f"Wrote {OUT.relative_to(REPO)} ({OUT.stat().st_size / 1024:.0f} KB) in {time.perf_counter() - START:.1f} s")
