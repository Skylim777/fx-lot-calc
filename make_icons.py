from PIL import Image, ImageDraw

BLUE = (39, 131, 222)       # #2783DE
BLUE_DARK = (28, 100, 172)
WHITE = (255, 255, 255)

def make(size, maskable=False, path="icon.png"):
    S = 4  # supersample
    W = size * S
    img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # background: rounded square (full bleed if maskable)
    radius = 0 if maskable else int(W * 0.22)
    # vertical gradient blue
    grad = Image.new("RGBA", (W, W))
    gd = ImageDraw.Draw(grad)
    for y in range(W):
        t = y / W
        r = int(BLUE[0] + (BLUE_DARK[0] - BLUE[0]) * t)
        g = int(BLUE[1] + (BLUE_DARK[1] - BLUE[1]) * t)
        b = int(BLUE[2] + (BLUE_DARK[2] - BLUE[2]) * t)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
    mask = Image.new("L", (W, W), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, W - 1, W - 1], radius=radius, fill=255)
    img.paste(grad, (0, 0), mask)

    d = ImageDraw.Draw(img)
    # content area (safe zone for maskable: center 80%)
    pad = 0.24 if maskable else 0.20
    x0, y0 = W * pad, W * pad
    x1, y1 = W * (1 - pad), W * (1 - pad)
    cw, ch = x1 - x0, y1 - y0

    lw = max(int(W * 0.045), 4)  # line width

    # three candlesticks: down, up, up (rising)
    n = 3
    gap = cw * 0.14
    bw = (cw - gap * (n - 1)) / n  # body width
    bodies = [
        (0.28, 0.62),  # candle 1 body top/bottom (relative in ch)
        (0.34, 0.78),
        (0.02, 0.52),
    ]
    wicks = [
        (0.16, 0.74),
        (0.22, 0.92),
        (-0.10, 0.66),
    ]
    for i in range(n):
        cx = x0 + i * (bw + gap) + bw / 2
        wt, wb = wicks[i]
        bt, bb = bodies[i]
        # wick
        d.line([(cx, y0 + ch * wt), (cx, y0 + ch * wb)], fill=WHITE, width=lw)
        # body
        d.rounded_rectangle(
            [cx - bw / 2, y0 + ch * bt, cx + bw / 2, y0 + ch * bb],
            radius=int(bw * 0.18), fill=WHITE,
        )

    img = img.resize((size, size), Image.LANCZOS)
    img.save(path)
    print("saved", path)

make(192, False, "icon-192.png")
make(512, False, "icon-512.png")
make(512, True, "icon-maskable-512.png")
