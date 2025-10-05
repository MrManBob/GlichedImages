import cv2
import random
from PIL import Image

def CI(Image):
    im = cv2.imread(Image)        # BGR order!
    h, w = im.shape[:2]

    ranx = random.randrange(0, w)
    rany = random.randrange(0, h)

    w, h = 300, 100
    crop = im[rany:rany + h, ranx:ranx + w]

    return crop

def E(crop):
    ran = random.randrange(1, 6)
    if ran == 1:
        rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        return rgb
    elif ran == 2:
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        return gray
    elif ran == 3:
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        return hsv
    elif ran == 4:
        edges = cv2.Canny(crop, 100, 200)
        return edges
    else:
        return crop

def LMSI(base_path, overlay_path, n, out_path="out.jpg", opacity=1.0):
    # Work in RGBA so we can use alpha blending
    base = Image.open(base_path).convert("RGBA")
    overlay_src = Image.open(overlay_path).convert("RGBA")

    # Optional: apply global opacity to the overlay
    if opacity < 1.0:
        r, g, b, a = overlay_src.split()
        a = a.point(lambda p: int(p * opacity))
        overlay_src = Image.merge("RGBA", (r, g, b, a))

    W, H = base.size
    ow, oh = overlay_src.size

    for _ in range(n):
        # keep the overlay fully inside the base
        x = random.randrange(0, max(1, W - ow + 1))
        y = random.randrange(0, max(1, H - oh + 1))
        base.alpha_composite(overlay_src, dest=(x, y))

    # Save (JPEG has no alpha → convert to RGB)
    base.convert("RGB").save(out_path, quality=92)

def LM(base_path, overlay_path, n, out_path="out.jpg", opacity=1.0):
    # Work in RGBA so we can use alpha blending
    base = Image.open(base_path).convert("RGBA")
    overlay_src = Image.open(overlay_path).convert("RGBA")

    # Optional: apply global opacity to the overlay
    if opacity < 1.0:
        r, g, b, a = overlay_src.split()
        a = a.point(lambda p: int(p * opacity))
        overlay_src = Image.merge("RGBA", (r, g, b, a))

    W, H = base.size
    ow, oh = overlay_src.size

    for _ in range(n):
        # keep the overlay fully inside the base

        crop = CI(base_path)
        Ea = E(crop)
        cv2.imwrite(overlay_path, Ea, [cv2.IMWRITE_JPEG_QUALITY, 90])
        overlay_src = Image.open(overlay_path).convert("RGBA")

        x = random.randrange(0, max(1, W - ow + 1))
        y = random.randrange(0, max(1, H - oh + 1))
        base.alpha_composite(overlay_src, dest=(x, y))

    # Save (JPEG has no alpha → convert to RGB)
    base.convert("RGB").save(out_path, quality=92)


crop = CI('TEST2.jpg')
Ea = E(crop)
cv2.imwrite("out.jpg", Ea, [cv2.IMWRITE_JPEG_QUALITY, 90])
LMSI("TEST2.jpg", "out.jpg", n=9, out_path="stacked.jpg", opacity=1.0)
LM("TEST2.jpg", "out.jpg", n=6, out_path="stacked2.jpg", opacity=1.0)
