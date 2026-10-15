"""Silver Jubilee invitation video renderer: 1080x1920 @30fps, frames piped to ffmpeg."""
import sys, math, subprocess, numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = sys.argv[1]
OUT = sys.argv[2]
PREVIEW = len(sys.argv) > 3  # write sample stills instead of the video
W, H, FPS = 1080, 1920, 30
F = S + "/fonts/"
RAQM = ImageFont.Layout.RAQM
rng = np.random.default_rng(7)

def font(name, size):
    return ImageFont.truetype(F + name, size, layout_engine=RAQM)

# ---------------------------------------------------------------- text
SILVER = [(255, 255, 255), (226, 229, 236), (176, 181, 192), (238, 240, 245), (150, 156, 168)]
STEEL = [(92, 98, 112), (60, 64, 78), (98, 104, 120)]
PLUM = [(110, 48, 78), (84, 32, 60), (120, 56, 88)]
DEEP = [(196, 200, 212), (118, 124, 140), (172, 177, 190), (92, 98, 114)]

def grad(h, stops):
    ys = np.linspace(0, 1, h)
    xs = np.linspace(0, 1, len(stops))
    return np.stack([np.interp(ys, xs, [c[i] for c in stops]) for i in range(3)], -1)

def text_img(txt, fnt, stops=SILVER, shadow=(20, 14, 30), shadow_a=0.85, glow=False, spacing=0):
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    l, t, r, b = d.textbbox((0, 0), txt, font=fnt)
    pad = 24
    w, h = r - l + 2 * pad, b - t + 2 * pad
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).text((pad - l, pad - t), txt, font=fnt, fill=255)
    m = np.array(m).astype(np.float32) / 255
    col = np.repeat(grad(h, stops)[:, None, :], w, 1)
    out = np.zeros((h, w, 4), np.float32)
    if shadow is not None:
        sh = cv2.GaussianBlur(np.roll(m, (3, 2), (0, 1)), (0, 0), 4 if not glow else 9) * shadow_a
        out[..., :3] = np.array(shadow, np.float32)
        out[..., 3] = np.clip(sh * (1.6 if glow else 1.0), 0, 1)
    a = m
    out[..., :3] = out[..., :3] * (1 - a[..., None]) + col * a[..., None]
    out[..., 3] = np.clip(a + out[..., 3] * (1 - a), 0, 1)
    return out

def wrap(txt, fnt, maxw):
    words, lines, cur = txt.split(" "), [], ""
    d = ImageDraw.Draw(Image.new("L", (1, 1)))
    for wd in words:
        tryl = (cur + " " + wd).strip()
        if d.textlength(tryl, font=fnt) <= maxw or not cur:
            cur = tryl
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    return lines

# ---------------------------------------------------------------- compositing
def over(dst, src, x, y, alpha=1.0):
    """alpha-composite float RGBA src onto float RGB dst at (x, y)."""
    if alpha <= 0: return
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0: return
    s = src[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4] * alpha
    dst[y0:y1, x0:x1] = dst[y0:y1, x0:x1] * (1 - a) + s[..., :3] * a

def ease(t): t = min(max(t, 0), 1); return t * t * (3 - 2 * t)

class El:
    """A text/graphic element centred at cx, top y, fading in at t0 with a small rise."""
    def __init__(self, img, y, t0, dur=0.9, cx=W // 2, rise=26, t1=None):
        self.img, self.y, self.t0, self.dur, self.cx, self.rise, self.t1 = img, y, t0, dur, cx, rise, t1
    def draw(self, fr, t):
        a = ease((t - self.t0) / self.dur)
        if self.t1 is not None: a *= 1 - ease((t - self.t1) / 0.6)
        if a <= 0: return
        h, w = self.img.shape[:2]
        over(fr, self.img, self.cx - w // 2, int(self.y + (1 - a) * self.rise), a)

def T(txt, fname, size, y, t0, stops=SILVER, **kw):
    sh = kw.pop("shadow", (20, 14, 30)); sa = kw.pop("shadow_a", 0.85); glow = kw.pop("glow", False)
    return El(text_img(txt, font(fname, size), stops, sh, sa, glow), y, t0, **kw)

def block(lines, fname, size, y, t0, gap=1.45, step=0.45, **kw):
    out, yy = [], y
    for i, ln in enumerate(lines):
        out.append(T(ln, fname, size, yy, t0 + i * step, **kw)); yy += int(size * gap)
    return out, yy

def load(p, size=None):
    im = Image.open(p).convert("RGB")
    return np.array(im).astype(np.float32)

def cover(img, z=1.0, fx=0.5, fy=0.5):
    """crop img to 9:16 at zoom z around focus (fx, fy) and resize to WxH."""
    h, w = img.shape[:2]
    cw = min(w, h * W / H) / z; ch = cw * H / W
    x0 = np.clip(fx * w - cw / 2, 0, w - cw); y0 = np.clip(fy * h - ch / 2, 0, h - ch)
    M = np.array([[W / cw, 0, -x0 * W / cw], [0, H / ch, -y0 * H / ch]], np.float32)
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def load_layer(name, size=None):
    plate = Image.open(S + f"/build/{name}_plate.png").convert("RGB")
    mask = Image.open(S + f"/build/{name}_mask.png").convert("L")
    if size: plate, mask = plate.resize(size, Image.LANCZOS), mask.resize(size, Image.LANCZOS)
    return np.array(plate).astype(np.float32), (np.array(mask).astype(np.float32) / 255)[..., None]

def alive(base, plate, mask, t, ax, ay, amp=1.0):
    """subtle life: breathing + gentle sway of the people, parallax against the background plate."""
    h, w = base.shape[:2]
    sy = 1 + 0.0065 * amp * math.sin(2 * math.pi * t / 3.6)
    sx = 1 - 0.002 * amp * math.sin(2 * math.pi * t / 3.6)
    ang = math.radians(0.4 * amp * math.sin(2 * math.pi * t / 6.2 + 0.8))
    dx = 7 * amp * math.sin(2 * math.pi * t / 8.5)
    c, s_ = math.cos(ang), math.sin(ang)
    A = np.array([[c * sx, -s_ * sy], [s_ * sx, c * sy]])
    off = np.array([ax, ay]) - A @ np.array([ax, ay]) + np.array([dx, 0])
    M = np.hstack([A, off[:, None]]).astype(np.float32)
    fg = cv2.warpAffine(base, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    m = cv2.warpAffine(mask, M, (w, h), flags=cv2.INTER_LINEAR)[..., None]
    Mb = np.float32([[1, 0, -0.5 * dx], [0, 1, 0]])
    bg = cv2.warpAffine(plate, Mb, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return bg * (1 - m) + fg * m

def vgrad(y0, y1, color, a0, a1):
    """vertical alpha band as RGBA layer covering full width."""
    h = y1 - y0
    a = np.linspace(a0, a1, h)[:, None].repeat(W, 1)
    layer = np.zeros((h, W, 4), np.float32); layer[..., :3] = color; layer[..., 3] = a
    return layer

def ornament(width, color=(200, 204, 214)):
    """silver divider: line - diamond - line with small dots."""
    h = 40; im = Image.new("RGBA", (width, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = h // 2; mid = width // 2
    d.line([(10, c), (mid - 30, c)], fill=color + (255,), width=3)
    d.line([(mid + 30, c), (width - 10, c)], fill=color + (255,), width=3)
    d.polygon([(mid, c - 16), (mid + 16, c), (mid, c + 16), (mid - 16, c)], fill=color + (255,))
    for dx in (-44, 44): d.ellipse([mid + dx - 5, c - 5, mid + dx + 5, c + 5], fill=color + (255,))
    for x in (10, width - 10): d.ellipse([x - 6, c - 6, x + 6, c + 6], fill=color + (255,))
    a = np.array(im).astype(np.float32); a[..., 3] /= 255
    sh = np.zeros_like(a); sh[..., 3] = cv2.GaussianBlur(a[..., 3], (0, 0), 3) * 0.6
    res = sh.copy(); al = a[..., 3:4]
    res[..., :3] = a[..., :3] * al; res[..., 3] = np.clip(a[..., 3] + sh[..., 3] * (1 - a[..., 3]), 0, 1)
    res[..., :3] = np.where(al > 0, a[..., :3], 20)
    return res

# ---------------------------------------------------------------- particles
NS = 70
spark = dict(x=rng.uniform(0, W, NS), y=rng.uniform(0, H, NS), r=rng.uniform(1.5, 4.5, NS),
             ph=rng.uniform(0, 6.28, NS), sp=rng.uniform(1.5, 3.5, NS), vy=rng.uniform(-25, -8, NS))
NP = 26
petal = dict(x=rng.uniform(0, W, NP), y=rng.uniform(-H, H, NP), s=rng.uniform(10, 20, NP),
             vy=rng.uniform(70, 140, NP), sw=rng.uniform(20, 60, NP), ph=rng.uniform(0, 6.28, NP),
             rot=rng.uniform(0, 360, NP), col=[(232, 128, 150), (240, 170, 185), (214, 96, 124)])

def draw_particles(fr, t, petals=True, sparks=True, petal_a=0.9):
    if sparks:
        lay = np.zeros((H, W), np.float32)
        for i in range(NS):
            a = 0.5 + 0.5 * math.sin(t * spark["sp"][i] + spark["ph"][i])
            y = (spark["y"][i] + spark["vy"][i] * t) % H
            x = spark["x"][i] + 10 * math.sin(t * 0.7 + i)
            r = spark["r"][i] * (0.6 + 0.6 * a)
            cv2.circle(lay, (int(x), int(y)), int(max(r, 1)), a, -1, cv2.LINE_AA)
            if spark["r"][i] > 3.6:  # star cross
                L = int(r * 4)
                cv2.line(lay, (int(x) - L, int(y)), (int(x) + L, int(y)), a * 0.7, 1, cv2.LINE_AA)
                cv2.line(lay, (int(x), int(y) - L), (int(x), int(y) + L), a * 0.7, 1, cv2.LINE_AA)
        lay = cv2.GaussianBlur(lay, (0, 0), 1.2)
        fr += (lay[..., None] * np.array([235, 238, 248], np.float32) - fr) * np.clip(lay, 0, 1)[..., None] * 0.9
    if petals:
        lay = np.zeros((H, W, 3), np.float32); al = np.zeros((H, W), np.float32)
        for i in range(NP):
            y = (petal["y"][i] + petal["vy"][i] * t) % (H + 200) - 100
            x = petal["x"][i] + petal["sw"][i] * math.sin(t * 1.3 + petal["ph"][i])
            s = petal["s"][i]; ang = petal["rot"][i] + t * 60
            sq = abs(math.cos(t * 2 + petal["ph"][i]))
            col = petal["col"][i % 3]
            cv2.ellipse(lay, (int(x), int(y)), (int(s), int(max(s * 0.55 * sq, 2))), ang, 0, 360, col, -1, cv2.LINE_AA)
            cv2.ellipse(al, (int(x), int(y)), (int(s), int(max(s * 0.55 * sq, 2))), ang, 0, 360, 1.0, -1, cv2.LINE_AA)
        al = al[..., None] * petal_a
        fr[:] = fr * (1 - al) + lay * al

VIG = None
def vignette(fr, strength=0.35):
    global VIG
    if VIG is None:
        yy, xx = np.mgrid[0:H, 0:W]
        d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.75)) ** 2)
        VIG = np.clip(1 - strength * d ** 2.2, 0, 1)[..., None].astype(np.float32)
    fr *= VIG

# ---------------------------------------------------------------- assets
couple = load(S + "/build/couple_silver.png")              # 1188x2160
ganesha = load(S + "/build/ganesha_916.png")               # 1080x1920
blur_c = cv2.GaussianBlur(couple, (0, 0), 28)
c_plate, c_mask = load_layer("couple")
CAX, CAY = couple.shape[1] * 0.5, couple.shape[0] * 0.955
def couple_at(t, amp=1.0): return alive(couple, c_plate, c_mask, t, CAX, CAY, amp)

def silver_wash(img, amt):
    g = img.mean(-1, keepdims=True)
    return img * (1 - amt) + (g * np.array([1.0, 1.01, 1.05]) * 0.55 + 255 * 0.45) * amt

bg_soft = np.repeat(grad(H, [(236, 238, 244), (250, 250, 253), (226, 229, 237)])[:, None, :], W, 1).astype(np.float32)
_yy, _xx = np.mgrid[0:H, 0:W]
_g = np.exp(-(((_xx - W / 2) / 480) ** 2 + ((_yy - 880) / 480) ** 2))[..., None]
bg_soft = bg_soft * (1 - 0.6 * _g) + 255 * 0.6 * _g

def card(x0, y0, x1, y1):
    """frosted silver-ivory card with double silver border (RGBA)."""
    w, h = x1 - x0, y1 - y0
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 46, fill=(252, 251, 255, 236))
    d.rounded_rectangle([18, 18, w - 19, h - 19], 34, outline=(168, 174, 188, 255), width=4)
    d.rounded_rectangle([32, 32, w - 33, h - 33], 26, outline=(205, 209, 220, 255), width=2)
    for cx, cy in [(18, 18), (w - 19, 18), (18, h - 19), (w - 19, h - 19)]:
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(176, 182, 196, 255))
    a = np.array(im).astype(np.float32); a[..., 3] /= 255
    return a

# ---------------------------------------------------------------- scenes
XF = 0.7  # crossfade seconds

class Scene:
    def __init__(self, dur, bg, els=(), petals=False, sparks=True, layers=(), vig=0.3):
        self.dur, self.bg, self.els, self.petals, self.sparks, self.layers, self.vig = dur, bg, list(els), petals, sparks, list(layers), vig
    def render(self, t):
        fr = self.bg(t).copy()
        for lay, x, y in self.layers: over(fr, lay, x, y)
        draw_particles(fr, t, self.petals, self.sparks)
        for e in self.els: e.draw(fr, t)
        if self.vig: vignette(fr, self.vig)
        return fr

scenes = []

# 1 Opening: silver doors open on the Vanakkam welcome --------------------
vk = np.array(Image.open(S + "/build/vanakkam_clean.png").convert("RGB").resize((1430, 2676), Image.LANCZOS)).astype(np.float32)
DL, DR, DT, DB = 216, 1244, 536, 2600          # doorway in 2x image coords
LEAF_L = np.concatenate([vk[DT:DB, 236:456], vk[DT:DB, 236:300][:, ::-1]], 1)  # clean outer part + mirrored stile
LEAF_R = LEAF_L[:, ::-1].copy()
OPEN_W = 326
vk_plate, vk_mask = load_layer("vk", (1430, 2676))
HALF = (DR - DL) // 2
_gy, _gx = np.mgrid[0:vk.shape[0], 0:vk.shape[1]]
DOOR_GLOW = np.exp(-(((_gx - 730) / 380) ** 2 + ((_gy - 1450) / 900) ** 2)).astype(np.float32)[..., None]
def bg1(t):
    img = alive(vk, vk_plate, vk_mask, t, 730, 2580, 0.9)
    p = ease((t - 0.9) / 2.2)                   # 0 closed -> 1 open
    fade = 1 - ease((t - 3.1) / 0.35)          # leaves dissolve into the photo's own open doors
    if fade > 0:
        for tex, side in ((LEAF_L, 0), (LEAF_R, 1)):
            w = int(HALF * (1 - p) + OPEN_W * p)
            leaf = cv2.resize(tex, (max(w, 2), DB - DT), interpolation=cv2.INTER_LINEAR)
            shade = 1 - 0.18 * math.sin(math.pi * p)
            leaf = leaf * shade
            x0 = DL if side == 0 else DR - w
            reg = img[DT:DB, x0:x0 + w]
            img[DT:DB, x0:x0 + w] = reg * (1 - fade) + leaf * fade
        if p < 0.05:                            # dark seam while closed
            img[DT:DB, DL + HALF - 4:DL + HALF + 4] *= 0.55
    burst = math.sin(math.pi * min(max((t - 0.9) / 2.6, 0), 1)) * 0.55
    if burst > 0:
        img = img * (1 - burst * DOOR_GLOW) + np.array([255, 246, 225], np.float32) * burst * DOOR_GLOW
    return cover(img, 1.0 + 0.008 * t, 0.5, 0.5)
band1 = vgrad(1380, H, (34, 26, 44), 0.0, 0.8)
s1 = [T("வணக்கம்", "TamilFullBold.ttf", 120, 1500, 3.1, glow=True),
      T("Vanakkam  ·  Welcome", "Cinzel.ttf", 48, 1670, 3.7),
      El(ornament(560), 1760, 4.1),
      T("to our Silver Jubilee celebration", "CormIt.ttf", 46, 1810, 4.4)]
class FadeLayer:
    def __init__(self, lay, y, t0): self.lay, self.y, self.t0 = lay, y, t0
    def draw(self, fr, t): over(fr, self.lay, 0, self.y, ease((t - self.t0) / 0.8))
scenes.append(Scene(7.0, bg1, [FadeLayer(band1, 1380, 2.8)] + s1, petals=False, sparks=True, vig=0.12))

# 2 Ganesha (original artwork, Hindi removed, Tamil verse) ------------------
def bg2(t): return cover(ganesha, 1.0 + 0.012 * t, 0.5, 0.45)
V = ["வாக்குண்டாம் நல்ல மனமுண்டாம் மாமலராள்",
     "நோக்குண்டாம் மேனி நுடங்காது — பூக்கொண்டு",
     "துப்பார் திருமேனித் தும்பிக்கை யான்பாதம்",
     "தப்பாமல் சார்வார் தமக்கு."]
s2 = [T("விநாயகர் துதி", "TamilFullBold.ttf", 48, 1355, 0.5, stops=STEEL, shadow=(255, 255, 255), shadow_a=0.6),
      El(ornament(380, (150, 156, 172)), 1425, 0.8)]
b, yy = block(V, "TamilFullSemi.ttf", 38, 1485, 1.3, gap=1.62, step=0.75, stops=PLUM, shadow=(255, 255, 255), shadow_a=0.5)
s2 += b + [T("— ஔவையார்", "TamilFullSemi.ttf", 32, yy + 18, 4.6, stops=STEEL, shadow=None)]
scenes.append(Scene(9.0, bg2, s2, sparks=True, vig=0.18))

# 3 Thiruvalluvar / Thirukkural on a palm leaf -------------------------------
bg3_img = np.zeros((H, W, 3), np.float32)
g = grad(H, [(250, 250, 253), (232, 234, 241), (246, 246, 250)]); bg3_img[:] = g[:, None, :]
yy_, xx_ = np.mgrid[0:H, 0:W]
glow3 = np.exp(-(((xx_ - W / 2) / 520) ** 2 + ((yy_ - 460) / 520) ** 2))[..., None]
bg3_img = bg3_img * (1 - 0.25 * glow3) + 255 * 0.25 * glow3
fr3 = card(60, 90, W - 60, H - 90)
leaf = Image.new("RGBA", (960, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(leaf)
d.rounded_rectangle([0, 0, 959, 419], 200, fill=(214, 186, 128, 255))
for k in range(12): d.line([(70, 40 + k * 30), (890, 40 + k * 30)], fill=(196, 166, 108, 255), width=2)
for hx in (90, 870): d.ellipse([hx - 12, 198, hx + 12, 222], fill=(120, 90, 50, 255))
leaf = leaf.filter(ImageFilter.GaussianBlur(0.6))
leaf = np.array(leaf).astype(np.float32); leaf[..., 3] /= 255
sh = np.zeros((460, 1000, 4), np.float32); sh[20:440, 20:980, 3] = cv2.GaussianBlur(leaf[..., 3], (0, 0), 12) * 0.35
def bg3(t):
    fr = bg3_img.copy(); over(fr, fr3, 60, 90); return fr
LEAF = (np.concatenate([leaf[..., :3], leaf[..., 3:]], -1))
INK = [(70, 40, 20), (52, 28, 12), (78, 46, 24)]
vl = Image.open(S + "/../images/7.png").convert("RGB").resize((560, 555), Image.LANCZOS)
VW, VH, BR = 560 + 24, 555 + 24, 40
vfr = Image.new("RGBA", (VW, VH), (0, 0, 0, 0)); d = ImageDraw.Draw(vfr)
d.rounded_rectangle([0, 0, VW - 1, VH - 1], BR, fill=(176, 182, 196, 255))
d.rounded_rectangle([5, 5, VW - 6, VH - 6], BR - 4, fill=(236, 238, 244, 255))
msk = Image.new("L", (560, 555), 0); ImageDraw.Draw(msk).rounded_rectangle([0, 0, 559, 554], BR - 10, fill=255)
vfr.paste(vl, (12, 12), msk)
VAL = np.array(vfr).astype(np.float32); VAL[..., 3] /= 255
vsh = np.zeros((VH + 60, VW + 60, 4), np.float32); vsh[30:30 + VH, 30:30 + VW, 3] = 1
vsh[..., 3] = cv2.GaussianBlur(vsh[..., 3], (0, 0), 16) * 0.35
s3 = [El(vsh, 140, 0.3, rise=0), El(VAL, 170, 0.3, rise=40),
      T("திருக்குறள் · 45", "TamilFullSemi.ttf", 40, 772, 0.9, stops=PLUM, shadow=None),
      El(ornament(520, (150, 156, 172)), 838, 1.2),
      El(sh, 880, 1.5, rise=0), El(LEAF, 900, 1.5, rise=0),
      T("அன்பும் அறனும் உடைத்தாயின்", "TamilFullBold.ttf", 44, 970, 2.4, stops=INK, shadow=None),
      T("இல்வாழ்க்கை", "TamilFullBold.ttf", 44, 1065, 3.0, stops=INK, shadow=None),
      T("பண்பும் பயனும் அது.", "TamilFullBold.ttf", 44, 1160, 3.6, stops=INK, shadow=None),
      El(ornament(420, (150, 156, 172)), 1350, 4.4)]
eng, _ = block(wrap("If married life is filled with love and virtue, that itself is its grace and its reward.",
                    font("CormIt.ttf", 50), 820), "CormIt.ttf", 46, 1405, 4.8, gap=1.3, step=0.3, stops=STEEL, shadow=None)
s3 += eng
s3 += [T("அன்பும் அறமும் நிறைந்த 25 ஆண்டுகள்", "TamilFullSemi.ttf", 40, 1585, 6.0, stops=PLUM, shadow=None),
       T("25 years of love and virtue", "Corm.ttf", 44, 1655, 6.4, stops=STEEL, shadow=None)]
scenes.append(Scene(9.0, bg3, s3, sparks=True, vig=0.12))

# 4 Couple reveal -------------------------------------------------------------
band = vgrad(1290, H, (34, 26, 44), 0.0, 0.82)
def bg4(t): return cover(couple_at(t), 1.0 + 0.008 * t, 0.5, 0.42)
s4 = [T("இனிய 25-ஆம் திருமண நாள்", "TamilFullBold.ttf", 54, 1505, 1.0, glow=True),
      T("Happy 25th Wedding Anniversary", "Cinzel.ttf", 46, 1610, 1.8),
      El(ornament(520), 1700, 2.4),
      T("வெள்ளி விழா  ·  Silver Jubilee", "TamilFullSemi.ttf", 44, 1755, 2.9)]
scenes.append(Scene(9.0, bg4, s4, petals=True, layers=[(band, 0, 1290)], vig=0.1))

# 5 Names close-up ---------------------------------------------------------------
band5 = vgrad(1150, H, (34, 26, 44), 0.0, 0.85)
def bg5(t): return cover(couple_at(t + 3.0, 0.8), 1.55 + 0.02 * t, 0.5, 0.3)
s5 = [T("லலிதா  &  பிரபுராம்", "TamilFullBold.ttf", 72, 1395, 0.6, glow=True),
      T("Lalitha & Praburam", "Vibes.ttf", 120, 1520, 1.4, glow=True),
      El(ornament(560), 1700, 2.2),
      T("Celebrating 25 beautiful years together", "CormIt.ttf", 46, 1755, 2.6)]
scenes.append(Scene(7.5, bg5, s5, petals=True, layers=[(band5, 0, 1150)], vig=0.1))

# 6 Invitation & date -------------------------------------------------------------
c6 = card(70, 300, W - 70, 1640)
def bg6(t):
    fr = silver_wash(cover(blur_c, 1.2 + 0.01 * t, 0.5, 0.4), 0.78); over(fr, c6, 70, 300); return fr
s6 = [T("அன்புடன் அழைக்கிறோம்", "TamilFullBold.ttf", 66, 420, 0.4, stops=PLUM, shadow=None),
      T("With love, we invite you", "Vibes.ttf", 84, 530, 1.0, stops=STEEL, shadow=None),
      T("to celebrate our", "Corm.ttf", 46, 660, 1.4, stops=STEEL, shadow=None),
      T("25th Wedding Anniversary", "Cinzel.ttf", 52, 730, 1.7, stops=PLUM, shadow=None),
      El(ornament(560, (150, 156, 172)), 840, 2.2),
      T("ஞாயிறு, அக்டோபர் 25, 2026", "TamilFullBold.ttf", 54, 930, 2.6, stops=PLUM, shadow=None),
      T("Sunday, October 25, 2026", "Cinzel.ttf", 50, 1040, 3.0, stops=STEEL, shadow=None),
      El(ornament(360, (150, 156, 172)), 1150, 3.4),
      T("மாலை 4:00 – இரவு 9:00", "TamilFullSemi.ttf", 46, 1230, 3.8, stops=PLUM, shadow=None),
      T("4:00 PM – 9:00 PM", "Cinzel.ttf", 64, 1320, 4.1, stops=STEEL, shadow=None),
      T("Dinner & celebration to follow", "CormIt.ttf", 44, 1450, 4.6, stops=STEEL, shadow=None)]
scenes.append(Scene(8.0, bg6, s6, sparks=True, vig=0.2))

# 7 Venue ---------------------------------------------------------------------------
c7 = card(70, 420, W - 70, 1500)
pin = Image.new("RGBA", (160, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(pin)
d.ellipse([10, 10, 150, 150], fill=(140, 60, 96, 255)); d.polygon([(22, 110), (138, 110), (80, 210)], fill=(140, 60, 96, 255))
d.ellipse([50, 50, 110, 110], fill=(245, 245, 250, 255))
pin = np.array(pin).astype(np.float32); pin[..., 3] /= 255
def bg7(t):
    fr = silver_wash(cover(blur_c, 1.35 + 0.01 * t, 0.45, 0.6), 0.78); over(fr, c7, 70, 420); return fr
class Bounce(El):
    def draw(self, fr, t):
        a = ease((t - self.t0) / 0.5)
        if a <= 0: return
        h, w = self.img.shape[:2]
        dy = -abs(math.sin((t - self.t0) * 3)) * 26 * max(0, 1 - (t - self.t0) / 2.5)
        over(fr, self.img, self.cx - w // 2, int(self.y + dy), a)
s7 = [Bounce(pin, 530, 0.4),
      T("Venue", "Cinzel.ttf", 72, 790, 1.0, stops=STEEL, shadow=None),
      El(ornament(460, (150, 156, 172)), 905, 1.5),
      T("26 Sandpiper Drive", "Cinzel.ttf", 64, 990, 2.0, stops=PLUM, shadow=None),
      T("Shrewsbury, MA", "Cinzel.ttf", 64, 1105, 2.5, stops=PLUM, shadow=None),
      T("Your presence will make our day complete", "CormIt.ttf", 44, 1265, 3.2, stops=STEEL, shadow=None)]
scenes.append(Scene(7.0, bg7, s7, sparks=True, vig=0.2))

# 8 Closing ----------------------------------------------------------------------------
band8 = vgrad(1230, H, (34, 26, 44), 0.0, 0.86)
def bg8(t): return cover(couple_at(t + 1.5), 1.12 - 0.012 * t, 0.5, 0.45)
s8 = [T("உங்கள் வருகையும் ஆசீர்வாதமும்", "TamilFullBold.ttf", 46, 1405, 0.6, glow=True),
      T("எங்கள் மகிழ்ச்சி", "TamilFullBold.ttf", 46, 1480, 1.0, glow=True),
      T("Your presence and blessings are our joy", "CormIt.ttf", 46, 1575, 1.6),
      El(ornament(460), 1650, 2.2),
      T("With love,", "Vibes.ttf", 64, 1700, 2.6),
      T("Lalitha & Praburam and Family", "Cinzel.ttf", 44, 1795, 3.0)]
scenes.append(Scene(8.5, bg8, s8, petals=True, layers=[(band8, 0, 1230)], vig=0.1))

# ---------------------------------------------------------------- timeline
starts, acc = [], 0.0
for sc in scenes:
    starts.append(acc); acc += sc.dur - XF
TOTAL = acc + XF
print("total seconds", round(TOTAL, 2), file=sys.stderr)

def frame_at(t):
    out = None
    for sc, st in zip(scenes, starts):
        lt = t - st
        if lt < 0 or lt > sc.dur: continue
        f = sc.render(lt)
        a = 1.0
        if st > 0 and lt < XF: a = ease(lt / XF)
        out = f if out is None else out * (1 - a) + f * a
    # fade in from white / out to white
    if t < 0.6: out = out * ease(t / 0.6) + 255 * (1 - ease(t / 0.6))
    if t > TOTAL - 1.2: k = ease((t - (TOTAL - 1.2)) / 1.2); out = out * (1 - k) + 252 * k
    return np.clip(out, 0, 255).astype(np.uint8)

if PREVIEW:
    for i, sc in enumerate(scenes):
        t = starts[i] + sc.dur - XF - 0.3
        Image.fromarray(frame_at(t)).resize((540, 960)).save(f"{OUT}_s{i+1}.jpg", quality=80)
    for k, t in enumerate((0.8, 1.6, 2.4, 3.3)):
        Image.fromarray(frame_at(t)).resize((360, 640)).save(f"{OUT}_door{k}.jpg", quality=80)
    sys.exit()

n = int(TOTAL * FPS)
p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                      "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19",
                      "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
for i in range(n):
    p.stdin.write(frame_at(i / FPS).tobytes())
    if i % 150 == 0: print("frame", i, "/", n, file=sys.stderr, flush=True)
p.stdin.close(); p.wait()
