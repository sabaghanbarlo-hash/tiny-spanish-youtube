"""Place hooks. The French project layered Paris-only scenes over the generic ones; the Spanish project uses the generic places
(cafe, store/market, street, park, beach ...) and only needs this interface. Add Spanish-flavoured scenes here (plaza, mercado,
taquería ...) by filling SCENES / KEYWORDS / ALIASES / LANDMARKS / DRAW (story scenes) and SHORT_SCENES / SHORT_DRAW (Shorts)."""
from PIL import Image, ImageDraw

L = None
SCENES, KEYWORDS, ALIASES, LANDMARKS, DRAW, FLOOR = {}, {}, {}, {}, {}, {}
SHORT_SCENES, SHORT_DRAW, OUTDOOR, BIRD_SCENES = set(), {}, set(), set()


def bind(mod):
    global L
    L = mod


def register(mod):
    bind(mod)


def register_short(mod):
    pass


def draw_short(scene, bg, rng):
    pass


def sparkle(fr, tt):
    pass


def slide_backdrop(W=1920, H=1080, ground=1000):
    """Warm backdrop for the vocabulary / grammar / quiz slides: sky gradient, rooftops, pavement."""
    top, bot = (190, 224, 248), (255, 244, 230)
    bg = Image.new("RGB", (W, H), bot); d = ImageDraw.Draw(bg)
    for y in range(ground):
        t = y / ground
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(top, bot)))
    cols = [(250, 226, 190), (244, 206, 168), (252, 236, 204), (238, 196, 150)]
    x, k = -40, 0
    while x < W:
        w = 260 + (k * 53) % 120; h = 420 + (k * 37) % 90
        d.rectangle((x, ground - h, x + w, ground), fill=cols[k % 4])
        d.rectangle((x - 8, ground - h - 26, x + w + 8, ground - h), fill=(196, 96, 64))
        for wx in range(x + 36, x + w - 60, 96):
            d.rounded_rectangle((wx, ground - h + 80, wx + 52, ground - h + 190), radius=8, fill=(120, 168, 190))
            d.rectangle((wx - 6, ground - h + 190, wx + 58, ground - h + 204), fill=(34, 120, 126))
        x += w + 6; k += 1
    d.rectangle((0, ground, W, H), fill=(214, 196, 170))
    return bg
