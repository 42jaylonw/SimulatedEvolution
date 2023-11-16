import numpy as np
from PIL import Image, ImageDraw
import random

"""
Rewrite from https://2draw.me/random_ship_generator/index.en.htm
"""


def r():
    return random.randint(50, 215)


def rc():
    return (r(), r(), r())


class InvaderCreator:
    def __init__(self, img_size):
        self.img_size = img_size
        self.list_sym = []

    def create_square(self, border, draw, rand_color, element, size):
        if element == int(size / 2):
            draw.rectangle(border, rand_color)
        elif len(self.list_sym) > 0 and len(self.list_sym) == element + 1:
            draw.rectangle(border, self.list_sym.pop())
        else:
            self.list_sym.append(rand_color)
            draw.rectangle(border, rand_color)

    def get_an_invader(self, size=5):
        orig_image = Image.new('RGB', (size, size))
        draw = ImageDraw.Draw(orig_image)
        invader_size = self.img_size
        self.draw_invader((0, 0, invader_size, invader_size), draw, size)
        # process so it more like an entity
        image = np.array(orig_image)
        empty_mask = image.sum(2) == 0
        half_body = int(size / 4)
        body_mask = np.zeros((size, size)).astype(bool)
        body_mask[half_body:-half_body, half_body:-half_body] = True
        filling_mask = empty_mask * body_mask
        image[filling_mask] = np.uint8(np.mean(image[~empty_mask].reshape(-1, 3), axis=0))
        return image

    def draw_invader(self, border, draw, size):
        x0, y0, x1, y1 = border
        square_size = (x1 - x0) / size
        rand_colors = [rc(), rc(), rc(), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        i = 1
        for y in range(size):
            i *= -1
            element = 0
            for x in range(size):
                top_left_x = x * square_size + x0
                top_left_y = y * square_size + y0
                bot_right_x = top_left_x + square_size
                bot_right_y = top_left_y + square_size
                self.create_square((top_left_x, top_left_y, bot_right_x, bot_right_y), draw, random.choice(rand_colors),
                                   element, size)
                if element == int(size / 2) or element == 0:
                    i *= -1
                element += i

    def create_image(self, size, invaders):
        orig_image = Image.new('RGB', (self.img_size, self.img_size))
        draw = ImageDraw.Draw(orig_image)
        invader_size = self.img_size / invaders
        padding = invader_size / size

        for x in range(invaders):
            for y in range(invaders):
                top_left_x = x * invader_size + padding / 2
                top_left_y = y * invader_size + padding / 2
                bot_right_x = top_left_x + invader_size - padding
                bot_right_y = top_left_y + invader_size - padding
                self.create_invader((top_left_x, top_left_y, bot_right_x, bot_right_y), draw, size)

        return orig_image


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # Example usage
    # creator = InvaderCreator(img_size=1500)
    # image = creator.create_image(size=5, invaders=5)
    # image.show()  # or image.save("invaders.png")
    generator = InvaderCreator(img_size=6)
    for _ in range(1000):
        invader = generator.get_an_invader()
        plt.imshow(invader)
        plt.show()
