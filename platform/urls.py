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

from django.conf.urls import url, include
from rest_framework import routers

from api.viewsets import UserViewSet, UploadViewSet
from platform.views import Upload, Extract

app_name = "platform"

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'uploads', UploadViewSet)

urlpatterns = [
    url(r'^json/', include(router.urls)),
    url(r'^upload/$', Upload.as_view()),
    url(r'^extract/', Extract.as_view()),
    url(r'^windows/', include('platform.windows.urls'))

]
