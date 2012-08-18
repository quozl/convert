#Copyright (C) 2012 Cristhofer Travieso <cristhofert97@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import gtk
import pango
import convert

from sugar.activity import activity
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ActivityToolbarButton
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.graphics.radiotoolbutton import RadioToolButton

SCREEN_WIDTH = gtk.gdk.screen_width()


class ConvertActivity(activity.Activity):
    def __init__(self, handle):
        activity.Activity.__init__(self, handle, True)

        self.dic = {}

        #Canvas
        self._canvas = gtk.VBox()

        hbox = gtk.HBox()
        self.combo1 = gtk.combo_box_new_text()
        self.combo1.connect('changed', self._call)

        flip_btn = gtk.Button()
        flip_btn.connect('clicked', self._flip)
        flip_btn.add(gtk.image_new_from_file('icons/flip.svg'))

        self.combo2 = gtk.combo_box_new_text()
        self.combo2.connect('changed', self._call)
        self.label_box = gtk.HBox()

        self.adjustment = gtk.Adjustment(1.0, 1.0, 10000.0, 0.1, 1.0)
        self.spin = gtk.SpinButton(self.adjustment, 0.0, 1)

        self.label = gtk.Label()
        self.label.connect('expose-event', self.resize_label)

        self.convert_btn = gtk.Button(' Convert ')
        self.convert_btn.connect('clicked', self._call)

        self.label_info = gtk.Label('convert:\n')
        self.label_info.modify_font(pango.FontDescription('12'))

        self._canvas.pack_start(hbox, False, False, 20)
        hbox.pack_start(self.combo1, False, True, 20)
        hbox.pack_start(flip_btn, True, False)
        hbox.pack_end(self.combo2, False, True, 20)
        spin_box = gtk.HBox()
        convert_box = gtk.HBox()
        convert_box.pack_start(spin_box, True, False, 0)
        spin_box.pack_start(self.spin, False, False, 0)
        self._canvas.pack_start(convert_box, False, False, 5)
        self._canvas.pack_start(self.label_box, True, False, 0)
        self.label_box.add(self.label)
        spin_box.pack_start(self.convert_btn, False, False, 20)
        self._canvas.pack_end(self.label_info, False, False, 30)

        self.set_canvas(self._canvas)

        #Toolbar
        toolbarbox = ToolbarBox()

        activity_button = ActivityToolbarButton(self)

        toolbarbox.toolbar.insert(activity_button, 0)

        separator = gtk.SeparatorToolItem()
        separator.set_expand(False)
        separator.set_draw(True)
        toolbarbox.toolbar.insert(separator, -1)

        # RadioToolButton
        self._lenght_btn = RadioToolButton()
        self._lenght_btn.connect('clicked',
                                 lambda w: self._update_combo(convert.lenght))
        self._lenght_btn.set_tooltip('Lenght')
        self._lenght_btn.props.icon_name = 'lenght'

        self._volume_btn = RadioToolButton()
        self._volume_btn.connect('clicked',
                                 lambda w: self._update_combo(convert.volume))
        self._volume_btn.set_tooltip('Volume')
        self._volume_btn.props.icon_name = 'volume'
        self._volume_btn.props.group = self._lenght_btn

        self._area_btn = RadioToolButton()
        self._area_btn.connect('clicked',
                               lambda w: self._update_combo(convert.area))
        self._area_btn.set_tooltip('Area')
        self._area_btn.props.icon_name = 'area'
        self._area_btn.props.group = self._lenght_btn

        self._weight_btn = RadioToolButton()
        self._weight_btn.connect('clicked',
                                 lambda w: self._update_combo(convert.weight))
        self._weight_btn.set_tooltip('Weight')
        self._weight_btn.props.icon_name = 'weight'
        self._weight_btn.props.group = self._lenght_btn

        self._speed_btn = RadioToolButton()
        self._speed_btn.connect('clicked',
                                lambda w: self._update_combo(convert.speed))
        self._speed_btn.set_tooltip('Speed')
        self._speed_btn.props.icon_name = 'speed'
        self._speed_btn.props.group = self._lenght_btn

        self._temp_btn = RadioToolButton()
        self._temp_btn.connect('clicked',
                               lambda w: self._update_combo(convert.temp))
        self._temp_btn.set_tooltip('Temperature')
        self._temp_btn.props.icon_name = 'temp'
        self._temp_btn.props.group = self._lenght_btn

        toolbarbox.toolbar.insert(self._lenght_btn, -1)
        toolbarbox.toolbar.insert(self._volume_btn, -1)
        toolbarbox.toolbar.insert(self._area_btn, -1)
        toolbarbox.toolbar.insert(self._weight_btn, -1)
        toolbarbox.toolbar.insert(self._speed_btn, -1)
        toolbarbox.toolbar.insert(self._temp_btn, -1)

        #
        separator = gtk.SeparatorToolItem()
        separator.set_expand(True)
        separator.set_draw(False)
        toolbarbox.toolbar.insert(separator, -1)

        stopbtn = StopButton(self)
        toolbarbox.toolbar.insert(stopbtn, -1)

        self.set_toolbar_box(toolbarbox)
        self._update_combo(convert.lenght)
        self.show_all()

    def _update_label(self):
        a = '%s ~ %s' % (str(self.spin.get_text()), str(self.convert()))
        print a
        self.label.set_text(a)

    def _call(self, widget=None):
        _unit = self._get_active_text(self.combo1)
        _to_unit = self._get_active_text(self.combo2)
        self._update_label()
        self.update_label_info(_unit, _to_unit)
        self.show_all()

    def _update_combo(self, data):
        for x in self.dic.keys():
            self.combo1.remove_text(0)
            self.combo2.remove_text(0)
        self.dic = data
        for x in self.dic.keys():
            self.combo1.append_text(x)
            self.combo2.append_text(x)
        self.combo1.set_active(0)
        self.combo2.set_active(0)
        self._call()
        self.show_all()

    def _get_active_text(self, combobox):
        model = combobox.get_model()
        active = combobox.get_active()
        if active < 0:
            return None
        return model[active][0]

    def _flip(self, widget):
        active_combo1 = self.combo1.get_active()
        active_combo2 = self.combo2.get_active()
        self.combo1.set_active(active_combo2)
        self.combo2.set_active(active_combo1)
        self.spin.set_value(float(self.label.get_text().split(' ~ ')[1]))
        self._call()

    def update_label_info(self, util=None, to_util=None):
        value = 1 * self.dic[util] / self.dic[to_util]
        self.label_info.set_text('   Convert: \n %s x %s = %s' % (str(util),
                                 str(value), str(to_util)))

    def resize_label(self, widget, event):
        num_label = len(self.label.get_text())
        size = str((60 * SCREEN_WIDTH / 100) / num_label)
        try:
            self.label.modify_font(pango.FontDescription(size))
        except ZeroDivisionError:
            pass

    def convert(self):
        number = float(self.spin.get_text())
        unit = self._get_active_text(self.combo1)
        to_unit = self._get_active_text(self.combo2)
        return convert.convert(number, unit, to_unit, self.dic)

    def recut(self, num):
        num = str(num)
        before_dot = num.split('.')[0]
        then_dot = num.split('.')[1]

        short_num = before_dot + '.' + then_dot[:2]

        return float(short_num)
