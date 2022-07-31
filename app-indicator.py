import datetime
import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, GLib as glib

from tracking import get_todays_standing_time, track_standing

CUMMULATIVE_TIME = 0
STANDING = False

def main():
    global CUMMULATIVE_TIME
    CUMMULATIVE_TIME += get_todays_standing_time()
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
    global STANDING
    STANDING = menu_item.get_active()
    track_standing(menu_item.get_active())

def get_stats(menu_item):
    w = gtk.Window(
        title='Standing Stats',
    )
    w.set_default_size(500, 500)
    w.set_destroy_with_parent(True)
    w.show()

def change_label(indicator):
    global CUMMULATIVE_TIME
    global STANDING
    CUMMULATIVE_TIME += 1 if STANDING else 0
    indicator.set_label(format_cummulative_time(CUMMULATIVE_TIME), '')
    return True

def format_cummulative_time(ct):
    minutes, secs = divmod(ct, 60)
    hour, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hour, minutes, secs)

def quit_menu(_):
    global STANDING
    if STANDING:
        track_standing(False)
    gtk.main_quit()

if __name__ == '__main__':
  main()