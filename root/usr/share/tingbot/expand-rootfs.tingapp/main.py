import tingbot, subprocess, time, os
from tingbot import *

state = {
    'process': None,
    'finish_called': False
}

@once(seconds=2)
def start_resize():
    state['process'] = subprocess.Popen(
        'raspi-config --expand-rootfs',
        shell=True)

def loop():
    screen.fill(color='blue')
    screen.image('logo.png',
        xy=(160, 60),
        scale=0.3)
    
    screen.image(
        'spinner.gif',
        xy=(160,140))
    
    if state['process'] is not None:
        returncode = state['process'].poll()
        if returncode is None:
            # process is still running
            screen.text('Expanding SD card...',
                font_size=12,
                xy=(160,180),
                color='white')
        elif returncode != 0:
            screen.text('Expand rootfs failed with error %i' % returncode,
                font_size=12,
                xy=(160,180),
                color='white')
        else:
            screen.text('Success. Tingbot is rebooting...',
                font_size=12,
                xy=(160,180),
                color='white')

            if not state['finish_called']:
                once(seconds=5)(finish)
                state['finish_called'] = True

def finish():
    # update the startup link to point back at springboard
    subprocess.check_call('ln -snf home /apps/startup', shell=True)
    subprocess.check_call(['reboot'])

# run the app
tingbot.run(loop)
