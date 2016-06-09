import tingbot
from tingbot import *
from cached_property import cached_property
import os, logging, math, subprocess, json

def image_with_text(string, color='grey', font=None, font_size=32, antialias=None):
    from tingbot.graphics import _font, _color
    font, antialias = _font(font, font_size, antialias)
    string = unicode(string)

    if antialias is None:
        antialias

    return Image(surface=font.render(string, antialias, _color(color)))

class TingApp(object):
    def __init__(self, path):
        self.path = path
    
    @cached_property
    def info(self):
        info_path = os.path.join(self.path, 'app.tbinfo')
        try:
            with open(info_path) as f:
                return json.load(f)
        except:
            logging.exception('Failed to get app info at %s', info_path)
            return {}
    
    @property
    def name(self):
        if 'name' in self.info:
            return self.info['name']
        else:
            basename = os.path.basename(self.path)
            name, ext = os.path.splitext(basename)
            return name

    @cached_property
    def name_image(self):
        return image_with_text(
            self.name,
            font_size=16,
            color='white',
            antialias=True,
            font='OpenSans-Semibold.ttf',
        )

    @cached_property
    def icon(self):
        image_path = os.path.join(self.path, 'icon-48.png')
        
        if not os.path.isfile(image_path):
            logging.warning(
                'Icon not found for app %s, expected an image at %s',
                self.path,
                image_path)
            return None
        
        try:
            image = Image.load(image_path)
        except:
            logging.exception('Failed to load image at %s', image_path)
            return None

        return image

    def draw(self, surface, centered_at):
        if self.icon:
            surface.image(
                self.icon,
                xy=centered_at,
                align='center',
                scale=1,
            )
        surface.image(
            self.name_image,
            xy=(centered_at[0], centered_at[1]+57),
            align='top',
        )

apps_dir = os.environ.get('APPS_DIR', '/apps')
apps = []

for filename in os.listdir(apps_dir):
    file = os.path.join(apps_dir, filename)
    _, ext = os.path.splitext(file)
        
    if ext == '.tingapp':
        apps.append(TingApp(file))

state = {
    'app_index': 0,
    'scroll_position': 0
}

@button.press('left')
def button_left():
    state['app_index'] -= 1
    if state['app_index'] < 0:
        state['app_index'] = 0
        state['scroll_position'] -= 0.02  # little nudge animation

@button.press('right')
def button_right():
    state['app_index'] += 1
    if state['app_index'] >= len(apps):
        state['app_index'] = len(apps) - 1
        state['scroll_position'] += 0.02  # little nudge animation

@touch()
def on_touch(action):
    if action == 'down':
        app = apps[state['app_index']]
        screen.fill(color='black')
        screen.text(
            'Opening %s...' % os.path.basename(app.path),
            font_size=14,
            color='white')

        screen.update()
        subprocess.check_call(['tbopen', os.path.abspath(app.path)])

def draw_app_at_index(app_i, scroll_position):
    if app_i < 0 or app_i >= len(apps):
        return

    draw_x = -(scroll_position - app_i)*320 + 160
    app = apps[int(app_i)]
    app.draw(surface=screen, centered_at=(draw_x, 100))

def draw_dots():
    num_apps = len(apps)
    
    width = num_apps * 10
    start_x = 320/2 - width/2
    
    for app_i in range(len(apps)):
        if app_i == state['app_index']:
            image = 'dot-selected.png'
        else:
            image = 'dot.png'
        
        screen.image(
            image,
            xy=(start_x + app_i*10, 230),
            align='left'
        )
    
def loop():
    screen.fill(color='black')
    
    screen.image(
        'tingbot-t.png',
        xy=(10,7),
        align='topleft',
    )
    draw_dots()
    
    scroll_position = state['scroll_position']
    app_index = state['app_index']
    scroll_position += (app_index-scroll_position)*0.2
    
    if math.floor(scroll_position) != math.ceil(scroll_position):
        draw_app_at_index(
            int(math.floor(scroll_position)),
            scroll_position)
        
    draw_app_at_index(
        int(math.ceil(scroll_position)),
        scroll_position)
         
    state['scroll_position'] = scroll_position

# run the app
tingbot.run(loop)
