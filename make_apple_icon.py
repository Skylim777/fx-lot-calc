"""iOSホーム画面用 apple-touch-icon（180x180・透過なし・全面塗り）を生成"""
from PIL import Image, ImageDraw

BLUE = (39, 131, 222)       # #2783DE
BLUE_DARK = (28, 100, 172)
WHITE = (255, 255, 255)

def make_apple(size=180, path="apple-touch-icon.png"):
    S = 4
    W = 512 * S
    # 背景: 全面塗りの縦グラデーション（角丸・透過なし。iOSが自動で角を丸める）
    img = Image.new("RGB", (W, W), BLUE)
    d = ImageDraw.Draw(img)
    for y in range(W):
        t = y / W
        r = int(BLUE[0] + (BLUE_DARK[0] - BLUE[0]) * t)
        g = int(BLUE[1] + (BLUE_DARK[1] - BLUE[1]) * t)
        b = int(BLUE[2] + (BLUE_DARK[2] - BLUE[2]) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # ロウソク足3本（既存アイコンと同じデザイン）
    pad = 0.22
    x0, y0 = W * pad, W * pad
    x1, y1 = W * (1 - pad), W * (1 - pad)
    cw, ch = x1 - x0, y1 - y0
    lw = max(int(W * 0.045), 4)
    n = 3
    gap = cw * 0.14
    bw = (cw - gap * (n - 1)) / n
    bodies = [(0.28, 0.62), (0.34, 0.78), (0.02, 0.52)]
    wicks = [(0.16, 0.74), (0.22, 0.92), (-0.10, 0.66)]
    for i in range(n):
        cx = x0 + i * (bw + gap) + bw / 2
        wt, wb = wicks[i]
        bt, bb = bodies[i]
        d.line([(cx, y0 + ch * wt), (cx, y0 + ch * wb)], fill=WHITE, width=lw)
        d.rounded_rectangle(
            [cx - bw / 2, y0 + ch * bt, cx + bw / 2, y0 + ch * bb],
            radius=int(bw * 0.18), fill=WHITE,
        )

    img = img.resize((size, size), Image.LANCZOS)
    img.save(path)
    print("saved", path)

make_apple()
