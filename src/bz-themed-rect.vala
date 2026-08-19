// bz-themed-rect.vala
// 
// Copyright 2026 Eva M
// 
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// 
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.
// 
// SPDX-License-Identifier: GPL-3.0-or-later

public class Bz.ThemedRect : Gtk.Widget {
	private Gdk.RGBA _light_rgba;
	private string? _light_string;
	public string? light_color {
		get { return _light_string; }
		set {
			if (value != null)
				_light_rgba.parse (value);
			_light_string = value;
		}
	}

	private Gdk.RGBA _dark_rgba;
	private string? _dark_string;
	public string? dark_color {
		get { return _dark_string; }
		set {
			if (value != null)
				_dark_rgba.parse (value);
			_dark_string = value;
		}
	}
	
	private Gtk.Widget? _child;
	public Gtk.Widget? child {
		get { return _child; }
		set {
			if (value == child)
				return;

			_child?.unparent ();

			_child = value;
			value?.set_parent (this);
		}
	}

	construct {
		Adw.StyleManager.get_default ().notify["dark"].connect (queue_draw);
	}

	static construct {
        set_layout_manager_type (typeof (Gtk.BinLayout));
        set_css_name ("BzThemedRect");
    }

    protected override void snapshot (Gtk.Snapshot snapshot) {
		var dark = Adw.StyleManager.get_default ().get_dark ();
		var color = dark ? _dark_string : _light_string;

		if (color != null) {
			var rgba = dark ? _dark_rgba : _light_rgba;
			snapshot.append_color (rgba, {{ 0, 0 }, { get_width (), get_height () }});
		}

		if (_child != null)
			snapshot_child (_child, snapshot);
    }

	protected override void dispose () {
        if (_child != null) {
			_child.unparent ();
            _child = null;
        }

        base.dispose ();
    }
}

