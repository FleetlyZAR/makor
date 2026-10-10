"""Research-led thumbnails for The Seven Days v2 (vidIQ research, 9 October 2026).

Three clearly different concepts for YouTube Studio's Test & Compare, chosen from the
evidence in exports/vidiq-research.md:

    r1  a face:     the brick-maker looking up by the kiln fire, "MADE IN GOD'S IMAGE"
    r2  a question: light racing over the black deep, "WHERE'S THE SUN?"
    r3  spectacle:  the earth from space, poster style "GENESIS 1" under "THE SEVEN DAYS"

Same helpers as make_concepts.py (films/tools/thumbs.py). Layouts in 1280x720 units;
--final renders 3840x2160 into exports/art/thumbnail-r1.jpg, -r2.jpg, -r3.jpg (under 2 MB).
Without --final it writes 1280x720 previews and a phone-size feed mock beside this script.

    python3 films/genesis/01-the-seven-days-v2/exports/art/concepts/make_concepts_research.py [--final]
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FILM = HERE.parents[2]
STILLS = FILM / "stills" / "movement"
CAST = FILM / "stills" / "cast"
sys.path.insert(0, str(HERE.parents[4] / "tools"))
import thumbs  # noqa: E402
from thumbs import C, G, cover, grade, kicker, shade, text, vignette  # noqa: E402

if "--final" in sys.argv:
    thumbs.set_scale(3)
W, H = thumbs.W, thumbs.H


def concept_image():
    # Human face: the brick-maker lifts his eyes by the kiln (cast/shot-06, the frame behind s023
    # in the cold open). The film's turn: in Babylon's story people carry the gods' labour; in
    # Genesis 1:27 the image of God is given to people like him. Face left, text right, never over it.
    im = grade(cover(CAST / "shot-06.jpg", (W, H), focus=(0.54, 0.36), zoom=1.25), contrast=1.12, color=1.05,
               bright=1.06)
    im = vignette(shade(im, "right", 0.88, 0.55), 0.28)
    im = kicker(im, (1280 - 60, 92), "GENESIS 1:27", anchor="ra")
    return text(im, (1280 - 54, 136), [[("MADE IN", C)], [("GOD'S", G)], [("IMAGE", G)]], 120, anchor="ra")


def concept_sun():
    # Question: Day One, light breaks over the black ocean and there is no sun in the sky (s040).
    # Answered on Day One and Day Four (the sun is made on the fourth day, and was a god in Egypt).
    im = grade(cover(STILLS / "s040.jpg", (W, H), focus=(0.42, 0.55), zoom=1.18), contrast=1.2, bright=0.97)
    im = vignette(shade(im, "bottom", 0.55, 0.45), 0.35)
    im = shade(im, "left", 0.55, 0.5)
    im = kicker(im, (60, 62), "DAY ONE  ·  GENESIS 1:3")
    return text(im, (54, 104), [[("WHERE'S", C)], [("THE ", C), ("SUN?", G)]], 150)


def concept_earth():
    # Spectacle, in the poster style of the cinematic Bible channels: the earth from space with
    # Africa and Arabia facing us (s005, the cold open), title low and centred, bottom right clear.
    im = grade(cover(STILLS / "s005.jpg", (W, H), focus=(0.58, 0.4), zoom=1.05), contrast=1.1, color=1.12,
               bright=1.12)
    im = vignette(shade(im, "bottom", 0.88, 0.5), 0.3)
    im = kicker(im, (640, 430), "THE  SEVEN  DAYS", anchor="ma")
    return text(im, (640, 476), [[("GENESIS 1", G)]], 150, anchor="ma")


CONCEPTS = [
    ("r1", concept_image, "The 7 Days of Creation: What Genesis 1 Told a Nation of Slaves"),
    ("r2", concept_sun, "Light Before the Sun? Genesis 1 and the 7 Days of Creation"),
    ("r3", concept_earth, "Genesis 1 Like You've Never Seen It: The 7 Days of Creation"),
]

if __name__ == "__main__":
    final = thumbs.S > 1
    out_dir = HERE.parent if final else HERE
    previews = []
    for name, fn, title in CONCEPTS:
        img = fn().convert("RGB")
        out = out_dir / (f"thumbnail-{name}.jpg" if final else f"research-{name}.jpg")
        q = 90
        img.save(out, quality=q, optimize=True)
        while out.stat().st_size > 1.95e6 and q > 70:
            q -= 4
            img.save(out, quality=q, optimize=True)
        print(out, img.size, f"{out.stat().st_size / 1e6:.2f} MB", f"q{q}")
        previews.append((img, title))
    if not final:
        thumbs.feed_mock(previews, HERE / "research-feed-mock.jpg", "15:26")
        print(HERE / "research-feed-mock.jpg")
