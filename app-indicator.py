import datetime
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, GLib as glib

from tracking import track_sitting, track_standing

def main():
    indicator = appindicator.Indicator.new(
        'stand-up-timer', 
        f'{os.getcwd()}/icons/icon.png',
        appindicator.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu())
    glib.timeout_add(1000, change_label, indicator)
    gtk.main()

def menu():
    menu = gtk.Menu()
    
    menu_items = [
        {
            'type': 'CheckMenuItem',
            'label': 'Stand Up',
            'f': stand_up
        },
        {
            'type': 'CheckMenuItem',
            'label': 'Sit Down',
            'f': sit_down
        },
        {
            'type': 'SeparatorMenuItem',
        },
        {
            'type': 'MenuItem',
            'label': 'Get Stats',
            'f': get_stats
        },
        {
            'type': 'SeparatorMenuItem',
        },
        {
            'type': 'MenuItem',
            'label': 'Exit Tray',
            'f': quit_menu
        }
    ]

    for item in menu_items:
        ME = getattr(gtk, item['type'])
        if item.get('label'):
            c = ME(label=item['label'])
        else:
            c = ME()
        if item.get('f'):
            c.connect('activate', item['f'])
        menu.append(c)

    menu.show_all()
    return menu
  
def stand_up(menu_item):
    if menu_item.get_active():
        print('Standing up.')
        track_standing()
        untoggle_others(menu_item)

def sit_down(menu_item):
    if menu_item.get_active():
        print('Sitting down.')
        track_sitting()
        untoggle_others(menu_item)

def get_stats(menu_item):
    w = gtk.Window(
        title='Standing Stats',
    )
    w.set_default_size(500, 500)
    w.set_destroy_with_parent(True)
    w.show()

def untoggle_others(menu_item):
    menu = menu_item.get_parent()
    children = menu.get_children()
    for child in children:
        if child != menu_item and isinstance(child, gtk.CheckMenuItem) and child.get_active():
            child.set_active(False)

def change_label(indicator):
    time = datetime.datetime.now().strftime('%H:%M:%S')
    indicator.set_label(time, '')
    return True

def quit_menu(_):
    gtk.main_quit()

if __name__ == '__main__':
  main()