import tingbot
from tingbot import *
import time, sys, math, codecs

def pseudo_rand(x):
    """
    Returns a randomly-distributed number between 0 and 1, but is
    deterministic, so always returns the same number for the same input `x`
    """
    return (abs(math.sin(x*123.5))*8.79) % 1

class Backer(object):
    def __init__(self, name):
        self.name = name
        self._image = None

    @property
    def image(self):
        if self._image is None:
            self._image = Image.from_text(
                self.name.lower(),
                color='white',
                font_size=16,
                font='BTTF.ttf')
        return self._image

    def is_offscreen(self):
        self._image = None

    def draw(self, y):
        screen.image(
            self.image,
            xy=(160, y))

start_time = time.time()
line_separation = 40
scroll_speed = 40
stars_speed = 30

num_particles = 200

#########
# SETUP #
#########

# note: we rot13'd the backers list so the names wouldn't be indexed by search engines
# this info is public already (accessible via http://kickstarter.com/profile/your_id),
# but we're doing this as a courtesy to our backers
with codecs.open('backers.txt', encoding='rot13') as f:
    backer_names = [line.strip() for line in f]

backers = [Backer(name) for name in backer_names]

########
# LOOP #
########

def loop():
    screen.fill(color='black')
    current_time = time.time() - start_time

    for i in range(num_particles):
        speed_index = pseudo_rand(i)
        speed = speed_index * stars_speed
        x = pseudo_rand(i*3.2123) * 320
        y = (pseudo_rand(i*2)*240 - current_time*speed) % 240
        brightness = speed_index*200
        screen.rectangle(
            xy=(x, y),
            size=(2, 2),
            color=(brightness, brightness, brightness))

    scroll_position = -current_time*scroll_speed
    image_y = min(120, 320 + scroll_position)

    if image_y > -100:
        screen.image(
            'tingbotrainbow.gif',
            xy=(160, image_y))

    for index, backer in enumerate(backers):
        y = 400 + line_separation*index + scroll_position

        if -20 < y < 260:
            backer.draw(y)
        else:
            backer.is_offscreen()

    if y < -10:
        sys.exit()

# run the app
tingbot.run(loop)
