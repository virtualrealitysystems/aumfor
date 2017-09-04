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

from django import template
register = template.Library()

@register.filter(name='split')
def split(value):
    ans = value.split("/")[4]
    ans = ans.split("-")[2]
    return ans


@register.filter(name='counter')
def counter():
    ans = 0
    if ans == 16:
        ans = 0
    else:
        ans = ans + 1
        # print(ans)
 	return ans		

@register.filter(name='save')
def save():
    value=1;
    return int(value)
