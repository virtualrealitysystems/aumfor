"""
    Virtual Reality Systems - Real Solutions for Virtual Systems.
    Email : info@virtualrealitysystems.net
    Copyright (C) 2017  Virtual Reality Systems

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

""" This app is used to remove naming confliction with other app in settings.py"""

from django.apps import AppConfig


class PlatformWin(AppConfig):
    name = 'platform.windows'
    label = 'platform_windows'  # <-- this is the important line - change it to anything other than the default, which is the module name ('foo' in this case)
    #
    # class PlatformConfig(AppConfig):
    #     name = 'platform'
    #     label = 'platform'
