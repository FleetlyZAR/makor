"""Shared prompt text for the photoreal treatment (films/STYLE-BIBLE.md, "Photoreal").

Every film from The Garden on uses these words, so the look and the people stay the same from
film to film. The Garden carries its own copy of the same text (written first); new films import
this module:

    sys.path.insert(0, str(REPO / "films" / "tools")); import photoreal as PR
"""

SUFFIX = ("Photorealistic cinematic film still, shot on 35mm film, natural light, colour grade of deep ink teal "
          "shadows and warm muted gold highlights, warm cream whites, no saturated reds or purples, calm and reverent, "
          "wide 16:9 composition with calm low detail space in the lower third, full frame with no borders or black "
          "bars, the image filling the whole frame edge to edge with no blank or faded band, no text, no lettering, "
          "no watermark, not a painting, not an illustration, not a 3D render, not cartoon.")
MOTION = ("Photorealistic cinematic footage with natural real world motion, slow and steady camera, no camera shake, "
          "no cuts, no text appears.")
REFNOTE = " Match the light, colour grade and world of the reference images."
NEAR_EAST = ("The land is the ancient Near East by the Tigris and Euphrates: date palms, fig trees, pomegranate trees, "
             "olive trees, grape vines, reeds along the river, no tropical plants, no mango, no banana, no apple trees. "
             "No walls, no buildings, no ruins, no fences, nothing made by hands.")
KEEP = " Each person's face, skin tone and hair stay exactly the same throughout; the framing stays modest."

# The cast, relative to a film folder in films/genesis/.
ADAM = "../02-the-garden/stills/cast/adam.jpg"
EVE = "../02-the-garden/stills/cast/eve.jpg"

_CAST = ("The man and the woman are the man and the woman in the reference portraits: keep their faces, skin tone "
         "and hair exactly, but not the cloth on their shoulders in the portraits. ")
_FRAME = "Never a close up. No other people."

# What the man and the woman wear, by stage of Genesis 2 and 3.
BEFORE_FIGS = (_CAST + "Before they ate, they wear nothing: seen at medium or long distance, from behind or in profile, "
               "with bare shoulders, tall grass, leaves or the landscape covering the man below the chest and the woman "
               "below the shoulders. " + _FRAME)
FIG_LEAVES = (_CAST + "Now they wear simple coverings of broad fig leaves sewn together (Genesis 3:7), and the woman's "
              "long hair falls over her shoulders; seen at medium or long distance, from behind or in profile, framed "
              "from the chest up for the man and the shoulders up for the woman, or with plants covering them. "
              + _FRAME)
HIDES = (_CAST + "They wear rough untailored garments of animal hide (Genesis 3:21), wrapped over one shoulder and tied "
         "with a leather strip, no woven cloth, no seams, no sleeves; seen at medium or long distance. " + _FRAME)
