/*
 * bz-decorated-screenshot.vala
 *
 * Copyright 2026 Eva M
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

public class Bz.DecoratedScreenshot : Gtk.Button {
    public Bz.AsyncTexture? async_texture { get; set; }

    construct {
        init_template ();
    }
    
    static construct {
        /* Can't use class annotation since the gresources are compiled into the
         * main binary */
        set_template_from_resource ("/io/github/kolunmi/Bazaar/bz-decorated-screenshot.ui");
    }
}

