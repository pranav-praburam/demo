"""Split a picture into person layer + filled background plate for subtle motion."""
import sys, numpy as np, cv2
from ai_edge_litert.interpreter import Interpreter
S = sys.argv[1]
it = Interpreter(model_path=S + "/models/selfie_mc.tflite"); it.allocate_tensors()
inp, outp = it.get_input_details()[0], it.get_output_details()[0]
def person_prob(im):
    x = cv2.resize(im, (256, 256)).astype(np.float32) / 255.
    it.set_tensor(inp["index"], x[None]); it.invoke()
    o = it.get_tensor(outp["index"])[0]; p = np.exp(o - o.max(-1, keepdims=True)); p /= p.sum(-1, keepdims=True)
    return 1 - p[..., 0]
def tiles(im):  # run at full image + 2 overlapping halves for finer edges
    h, w = im.shape[:2]
    full = cv2.resize(person_prob(im), (w, h))
    acc = np.zeros((h, w), np.float32); cnt = np.zeros((h, w), np.float32)
    for y0 in (0, h // 3, h - h // 2):
        y1 = min(h, y0 + h // 2); crop = im[y0:y1]
        acc[y0:y1] += cv2.resize(person_prob(crop), (w, y1 - y0)); cnt[y0:y1] += 1
    fine = np.where(cnt > 0, acc / np.maximum(cnt, 1), full)
    return np.minimum(full + 0.15, np.maximum(full, fine) )
for name, src, keepx in [("couple", "couple_silver.png", (0.13, 0.87)), ("vk", "vanakkam_clean.png", (0.25, 0.80))]:
    im = cv2.cvtColor(cv2.imread(f"{S}/build/{src}"), cv2.COLOR_BGR2RGB)
    h, w = im.shape[:2]
    p = tiles(im)
    m = (p > 0.5).astype(np.uint8)
    m[:, :int(keepx[0] * w)] = 0; m[:, int(keepx[1] * w):] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    keep = [i for i in range(1, n) if st[i, cv2.CC_STAT_AREA] > 0.02 * h * w]
    m = np.isin(lab, keep).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    inv = (1 - m).astype(np.uint8)  # fill small interior holes (keep the gap between legs)
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(inv)
    for i in range(1, n2):
        if st2[i, cv2.CC_STAT_AREA] < 0.0015 * h * w: m[lab2 == i] = 1
    soft = cv2.GaussianBlur(m.astype(np.float32), (0, 0), 1.6)
    # background plate: inpaint dilated person area at half res
    big = cv2.dilate(m, np.ones((25, 25), np.uint8))
    sm = cv2.resize(im, (w // 2, h // 2)); smm = cv2.resize(big * 255, (w // 2, h // 2))
    plate = cv2.inpaint(cv2.cvtColor(sm, cv2.COLOR_RGB2BGR), smm, 12, cv2.INPAINT_TELEA)
    plate = cv2.cvtColor(cv2.resize(plate, (w, h), interpolation=cv2.INTER_CUBIC), cv2.COLOR_BGR2RGB)
    plate = cv2.GaussianBlur(plate, (0, 0), 1.0)
    bm = cv2.GaussianBlur(big.astype(np.float32), (0, 0), 6)[..., None]
    plate = (im * (1 - bm) + plate * bm).astype(np.uint8)
    cv2.imwrite(f"{S}/build/{name}_plate.png", cv2.cvtColor(plate, cv2.COLOR_RGB2BGR))
    cv2.imwrite(f"{S}/build/{name}_mask.png", (soft * 255).astype(np.uint8))
    prev = np.hstack([cv2.resize(im, (w // 4, h // 4)), cv2.resize(np.repeat((soft * 255).astype(np.uint8)[..., None], 3, -1), (w // 4, h // 4)), cv2.resize(plate, (w // 4, h // 4))])
    cv2.imwrite(f"{S}/build/{name}_layers_prev.jpg", cv2.cvtColor(prev, cv2.COLOR_RGB2BGR))
