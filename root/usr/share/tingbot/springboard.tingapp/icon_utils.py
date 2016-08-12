import os
import tingbot


def iconise(fname):
    return os.path.join(os.path.dirname(__file__), 'icons', 'Icon_' + fname)


def get_network_icon_name(cell):
    if cell and cell.ssid:
        if hasattr(cell, 'link_quality'):
            quality = min(99, max(cell.link_quality * 100 / 70, 0))
        else:
            quality = min(99, max((110+cell.signal) * 100 / 70, 0))
    else:
        if tingbot.get_ip_address():
            quality = -1  # wired network
        else:
            return 'WiFi-1.png'
    if quality == -1:
        return 'Ethernet-1.png'
    else:
        return 'WiFi-%d.png' % (int(quality / 20) + 2)
