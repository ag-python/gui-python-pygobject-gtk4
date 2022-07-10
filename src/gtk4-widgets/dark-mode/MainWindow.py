# -*- coding: utf-8 -*-
"""Python e GTK 4: PyGObject Ativando e desativando o dark mode (modo escuro)."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.application = kwargs.get('application')
        self.gtk_settings = self.application.gtk_settings

        self.set_title(title='Python e GTK 4: PyGObject Ativando e desativando o dark mode (modo escuro)')
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

        grid = Gtk.Grid.new()
        grid.set_margin_top(margin=12)
        grid.set_margin_end(margin=12)
        grid.set_margin_bottom(margin=12)
        grid.set_margin_start(margin=12)
        grid.set_column_spacing(spacing=12)
        self.set_child(child=grid)

        text = 'Clique no switch para ativar ou desativar o modo escuro (dark mode)'
        label = Gtk.Label.new(str=text)
        grid.attach(child=label, column=0, row=0, width=1, height=1)

        self.switch = Gtk.Switch.new()
        self.switch.connect('notify::active', self.on_switch_active)
        grid.attach(child=self.switch, column=1, row=0, width=1, height=1)

    def on_switch_active(self, widget, state):
        if widget.get_active():
            # self.settings.set_property('gtk-application-prefer-dark-theme', True)
            self.gtk_settings.set_property('gtk-theme-name', 'Adwaita-dark')
        else:
            # self.settings.set_property('gtk-application-prefer-dark-theme', False)
            self.gtk_settings.set_property('gtk-theme-name', 'Adwaita')


class ExampleApplication(Adw.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)

        self.gtk_settings = Gtk.Settings.get_default()
        self.gtk_theme_name = self.gtk_settings.get_property('gtk-theme-name')

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

        if self.gtk_theme_name == 'Adwaita-dark':
            win.switch.set_state(state=True)

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
