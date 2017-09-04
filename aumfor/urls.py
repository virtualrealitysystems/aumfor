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

from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [

    url(r'^', include('main.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^platform/', include('platform.urls')),
    # url(r'^api/linux/', include('api.linux.urls')),
    # url(r'^api/mac/', include('api.mac.urls')),
    url(r'^admin/', include(admin.site.urls)),

]

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'

