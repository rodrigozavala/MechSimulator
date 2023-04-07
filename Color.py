import enum
class Color(enum.Enum):
    WHITE=(255,255,255)
    CYAN=(0, 251, 255)
    BLACK=(0,0,0)
    BLUE=(0,0,255)
    LIGHT_BLUE=(5, 207, 242)
    AQUAMARINE=(35, 184, 169)
    RED=(255,0,0)
    GREEN=(0,255,0)
    LIGHT_PINK=(249, 157, 252)
    PINK=(247, 0, 255)
    LAVENDER=(199, 135, 245)
    VIOLETE=(86, 21, 133)
    LILA=(225, 134, 235)
    LIGHT_GRAY=(178, 177, 179)
    GRAY=(121, 120, 122)
    OBSCURE_GRAY=(71, 70, 71)
    YELLOW=(240, 232, 5)
    ORANGE=(252, 161, 3)
    DARK_BROWN=(54, 39, 14)
    BROWN=(107, 79, 32)
    LIGHT_BRONW=(140, 111, 62)
    def __init__(self, R, G, B):
        self.colorCode =(R,G,B)



