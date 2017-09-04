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
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from platform.models import Upload


# To serializ user data into json format
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")


# To serializ upload data into json format
class UploadSerializer(ModelSerializer):
    class Meta:
        model = Upload
        fields = "__all__"
