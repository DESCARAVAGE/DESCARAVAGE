"""Photo détourée (PNG avec transparence) -> lignes ASCII."""
import cv2
import numpy as np

RAMP = " .:-=+*#%@"


def to_ascii(path, cols=78, rows=50, ratio=360 / 450):
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)          # BGRA
    h, w = img.shape[:2]
    if w / h > ratio:                                           # recadrage centré au ratio du bloc
        nw = int(h * ratio); img = img[:, (w - nw) // 2:(w - nw) // 2 + nw]
    else:
        img = img[:int(w / ratio)]

    gray = cv2.cvtColor(img[..., :3], cv2.COLOR_BGR2GRAY)
    gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(6, 6)).apply(gray)
    gray = cv2.addWeighted(gray, 1.8, cv2.GaussianBlur(gray, (0, 0), 3), -0.8, 0)  # accentue les traits
    lum = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_AREA) / 255
    fg = cv2.resize(img[..., 3], (cols, rows), interpolation=cv2.INTER_AREA) > 127

    # égalisation sur la silhouette, puis inversion : zones sombres = caractères denses
    vals = np.sort(lum[fg])
    ink = 1.12 - (0.12 + 0.88 * np.searchsorted(vals, lum) / max(1, len(vals)))
    idx = np.clip((ink * len(RAMP)).astype(int), 1, len(RAMP) - 1)
    return ["".join(RAMP[i] if f else " " for i, f in zip(ri, rf)) for ri, rf in zip(idx, fg)]