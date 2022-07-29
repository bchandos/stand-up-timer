import os
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

from tracking import track_sitting, track_standing

def main():
    indicator = appindicator.Indicator.new(
        'customtray', 
        f'{os.getcwd()}/icons/icon.png',
        appindicator.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(menu())
    gtk.main()

def menu():
    menu = gtk.Menu()
    
    commands = [
        {
            'name': 'Stand Up',
            'f': stand_up
        },
        {
            'name': 'Sit Down',
            'f': sit_down
        },
        {
            'name': 'Exit Tray',
            'f': quit_menu
        }
    ]

    for command in commands:
        c = gtk.MenuItem(label=command['name'])
        c.connect('activate', command['f'])
        menu.append(c)

    menu.show_all()
    return menu
  
def stand_up(menu_item):
    track_standing()
    menu = menu_item.get_parent()
    set_checks(menu, menu_item)
    # label = menu_item.get_label()
    # menu_item.set_label(f'\u2713 {label}')

def sit_down(menu_item):
    track_sitting()
    menu = menu_item.get_parent()
    set_checks(menu, menu_item)
    # label = menu_item.get_label()
    # menu_item.set_label(f'\u2713 {label}')

def quit_menu(_):
    gtk.main_quit()

def set_checks(menu, menu_item):
    children = menu.get_children()
    for child in children:
        label_parts = child.get_label().split(' \u2713')
        label = label_parts[0]
        child.set_label(label)
        print(label)
        if child == menu_item:
            child.set_label(f'{label} \u2713')
    

if __name__ == '__main__':
  main()