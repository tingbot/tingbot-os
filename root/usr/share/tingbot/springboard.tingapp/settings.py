import socket
import threading

import wifi
import pygame
import tingbot
import tingbot_gui as gui
from icon_utils import get_network_icon_name, iconise

IFACE = 'wlan0'


def get_os_version():
    return tingbot.__version__


def can_update_os():
    return True


def update_os():
    ###FIXME###
    print "updating OS"


def draw_cell(widget, cell):
    if widget.pressed:
        widget.fill(widget.style.button_pressed_color)
    else:
        widget.fill(widget.style.popup_bg_color)
    if isinstance(cell, wifi.Cell) or isinstance(cell, tingbot.hardware.WifiCell):
        label = cell.ssid
        widget.image(iconise(get_network_icon_name(cell)),
                     xy=(widget.size[0]-5, widget.size[1] / 2),
                     align="right")
        if hasattr(cell, 'encrypted') and cell.encrypted:
            widget.image(iconise("Lock-1.png"),
                         xy=(widget.size[0]-23, widget.size[1] / 2),
                         align="right")
    else:
        label = cell
    widget.text(label,
                xy=(5, widget.size[1] / 2),
                size=(widget.size[0]-36, widget.size[1]),
                align="left",
                color=widget.style.button_text_color,
                font=widget.style.button_text_font,
                font_size=widget.style.button_text_font_size)


class CellButton(gui.Button):
    def draw(self):
        draw_cell(self, self.label)


class CellDropDown(gui.DropDown):
    def __init__(self, *args, **kwargs):
        super(CellDropDown, self).__init__(*args, **kwargs)
        self.style.popupmenu_button_class = CellButton

    def draw(self):
        draw_cell(self, self.selected[0])


class CellSettings(gui.MessageBox):
    def __init__(self, cell, style=None):
        super(CellSettings, self).__init__((20, 20), (280, 160), "topleft", style=style,
                                           buttons=['Connect', 'Forget', 'Cancel'])
        gui.StaticText((140, 0), (100, 30), "top", parent=self.panel, label=cell.ssid)
        self.cell = cell
        self.scheme = wifi.Scheme.find(IFACE, cell.ssid)
        if cell.encrypted:
            if self.scheme:
                pwd = "        "
            else:
                pwd = ""
            gui.StaticText((10, 55), (90, 30), "left", label="Password:",
                           style=style, parent=self.panel)
            self.password = gui.PasswordEntry((270, 55), (160, 30), "right", parent=self.panel,
                                              label="Password", string=pwd)
        else:
            self.password = None

    def close(self, label):
        if label == "Connect":
            if (self.scheme is None) or (self.password and self.password.string != "        "):
                if self.password:
                    self.scheme = wifi.Scheme.for_cell(interface=IFACE,
                                                       name=self.cell.ssid,
                                                       cell=self.cell,
                                                       passkey=self.password.string)
                else:
                    self.scheme = wifi.Scheme.for_cell(interface=IFACE,
                                                       name=self.cell.ssid,
                                                       cell=self.cell)
            try:
                self.scheme.save()
                try:
                    self.scheme.activate()
                except wifi.exceptions.ConnectionError:
                    gui.message_box(message="Incorrect Password")
            except IOError:
                gui.message_box(message="Not allowed to change network")
        elif label == "Forget":
            if self.scheme:
                self.scheme.delete()
        elif label == "Cancel":
            # do nothing
            pass
        super(CellSettings, self).close(label)


class Settings(gui.Dialog):
    # we're using a ScrollArea here in order to do the animation bit
    # but we need to alter it's functionality slightly
    def __init__(self, callback=None, style=None):
        super(Settings, self).__init__((0, 0), (320, 200), "topleft",
                                       style=style, callback=callback, transition="slide_down")
        style14 = self.style.copy(statictext_font_size=14, button_text_font_size=14)
        gui.StaticText((160, 23), (100, 20), parent=self.panel, style=style14, label="Settings")
        # add widgets
        i = 0
        self.current_cell = tingbot.get_wifi_cell()
        if self.current_cell is not None:
            # fill in with basic details for now, but set scan running and we'll
            # update later
            self.cell_finder = threading.Thread(target=self.find_cells)
            self.cell_finder.start()
            self.found_cells_timer = self.create_timer(self.show_found_cells, seconds=0.5)
            if self.current_cell:
                cell_list = [self.current_cell]
            else:
                cell_list = ["Scanning..."]
            gui.StaticText((16, 59 + i*32), (120, 27), align="left", style=style14,
                           parent=self.panel, label="Wi-Fi Network:", text_align="left")
            self.cell_dropdown = CellDropDown((313, 59 + i*32), (153, 27),
                                              align="right",
                                              style=style14,
                                              parent=self.panel,
                                              values=cell_list)
            i += 1
        # show IP address
        ip_addr = tingbot.get_ip_address() or "No connection"
        gui.StaticText((16, 59 + i*32), (120, 27), align="left", style=style14,
                       parent=self.panel, label="IP Address:", text_align="left")
        gui.StaticText((304, 59 + i*32), (153, 27), align="right", style=style14,
                       parent=self.panel, label=ip_addr, text_align="right")
        i += 1
        # show tingbot version
        gui.StaticText((16, 59 + i*32), (120, 27), align="left", style=style14,
                       parent=self.panel, label="Tingbot OS:", text_align="left")
        gui.StaticText((304, 59 + i*32), (120, 27), align="right", style=style14,
                       parent=self.panel, label=tingbot.__version__, text_align="right")
        i += 1
        # show update button
        if can_update_os():
            gui.StaticText((16, 59 + i*32), (120, 27), align="left", style=style14,
                           parent=self.panel, label="Update Available:", text_align="left")
            gui.Button((313, 59 + i*32), (120, 27), align="right", style=style14,
                       parent=self.panel, label="Update Now", callback=update_os)
        self.update(downwards=True)

    def wifi_selected(self, name, cell):
        CellSettings(cell, self.style).run()

    def find_cells(self):
        try:
            self.cells = wifi.Cell.all(IFACE)
        except wifi.exceptions.InterfaceError:
            self.cells = []

    def show_found_cells(self):
        if not self.cell_finder.is_alive():
            self.found_cells_timer.stop()
            cell_list = [(x, x) for x in self.cells]
            self.cell_dropdown.values = cell_list
            self.cell_dropdown.callback = self.wifi_selected
            if cell_list:
                self.cell_dropdown.selected = cell_list[0]
            else:
                self.cell_dropdown.selected = ("No wifi signals", None)
            self.update(downwards=True)
