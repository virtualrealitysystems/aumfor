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

from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^$', views.index, name='home'),
    url(r'^thread/', views.thread, name='thread'),
    url(r'^handles/', views.handles, name='handles'),
    url(r'^dll/', views.dll, name='dll'),
    url(r'^networkconnection/', views.network_connections, name='networkconnection'),
    url(r'^registryhives/', views.registry_hives, name='registryhives'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^register/', views.register, name='signup'),
    url(r'^process/', views.process_data, name='process'),
    url(r'^dumps/', views.uploades, name='dumps'),
    url(r'^scan/', views.scanResult, name='scan'),
    url(r'^scandata/', views.scanReport, name='scanreport'),
    url(r'^imageinfo/', views.imageInfo, name='imageinfo'),
    url(r'^team/', views.team, name='team'),
    url(r'^help/', views.help, name='help'),
    url(r'^contactus', views.contactus, name='contact'),
    url(r'^processdetail/', views.process_detail, name='processdetail'),
    url(r'^email/', views.email, name='email'),

]
