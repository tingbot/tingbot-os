import subprocess, sys
from terminal_colors import terminal_colors as tc

# clear the screen
sys.stdout.write("\x1b[2J\x1b[H")

print ''
print tc.cyan+'Welcome to the terminal!'+tc.end
print ''
print "You'll need to connect a keyboard to"
print 'get started here. To exit, press'
print 'Ctrl-D on your keyboard or hold the'
print 'two middle buttons on the Tingbot.'
print ''
print 'Press [return] to begin...'
print ''

# in the call below, we manually set the stdin, stdout, stderr
# file descriptors to /dev/tty1. This is to give bash real TTY
# fds so that programs like `man' work

subprocess.call([
    'sudo', '-u', 'pi',
    'bash', '--login', '-i'],
    cwd='/home/pi',
    stdin=open('/dev/tty1', 'r'),
    stdout=open('/dev/tty1', 'w'),
    stderr=open('/dev/tty1', 'w'))
