# -*- coding: utf-8 -*-
"""Python e GTK 4: PyGObject Gtk.PopoverMenu()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python e GTK 4: PyGObject Gtk.PopoverMenu()')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)

        menu_button_model = Gio.Menu()
        menu_button_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        # Menu principal.
        gio_menu = Gio.Menu.new()

        # Item do menu.
        gio_menu_item_01 = Gio.MenuItem.new()
        gio_menu_item_01.set_label(label='Item 01')
        # Ação que será realizada quando o item menu for ativo/pressionado.
        gio_menu_item_01.set_detailed_action(
            detailed_action='win.menu-item-activate',
        )
        gio_menu.append_item(gio_menu_item_01)

        # Menu que irá conter os itens do submenu.
        gio_menu_submenu = Gio.Menu.new()

        # Submenu.
        gio_menu_item_submenu = Gio.MenuItem.new_submenu(
            label='Submenu',
            submenu=gio_menu_submenu,
        )
        gio_menu.append_item(gio_menu_item_submenu)

        # Item que será adicionando no submenu.
        gio_menu_item_02 = Gio.MenuItem.new()
        gio_menu_item_02.set_label(label='Item 02')
        gio_menu_item_02.set_detailed_action(
            detailed_action='win.menu-item-activate',
        )
        gio_menu_submenu.append_item(gio_menu_item_02)

        # Sessão que irá conter os itens.
        gio_menu_section = Gio.Menu.new()

        # Sessão.
        gio_menu_item_section = Gio.MenuItem.new_section(
            label='Editar',
            section=gio_menu_section,
        )
        gio_menu.append_item(gio_menu_item_section)

        # Outra forma de se criar itens.
        # Itens que serão adicionados na sessão.
        gio_menu_section.append(
            label='item 03',
            detailed_action='win.menu-item-activate',
        )
        gio_menu_section.append(
            label='item 04',
            detailed_action='win.menu-item-activate',
        )

        # Criando uma nova ação para os itens do menu.
        action_menu_item_activate = Gio.SimpleAction.new(
            name='menu-item-activate',
            parameter_type=None,
        )
        # Método que será chamado quando o menu for ativo/pressionado.
        action_menu_item_activate.connect('activate', self.on_gio_menu_item_activate)
        # Adicionando a ação que foi criada.
        self.add_action(action_menu_item_activate)

        # Popover menu irá conter o menu principal que contem os outros menus.
        popover_menu = Gtk.PopoverMenu.new_from_model(gio_menu)

        headerbar = Gtk.HeaderBar.new()
        headerbar.set_show_title_buttons(setting=True)
        self.set_titlebar(titlebar=headerbar)

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_popover(popover=popover_menu)
        headerbar.pack_end(child=menu_button)

    def on_gio_menu_item_activate(self, widget, variant_type):
        print('Gio.SimpleAction')


class ExampleApplication(Adw.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        print('Ação app.preferences foi ativa.')

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
