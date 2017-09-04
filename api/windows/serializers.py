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

from rest_framework.serializers import ModelSerializer

from platform.windows.models import *

""" this all serializer convert the data into json formate"""
class DumpSerializer(ModelSerializer):
    class Meta:
        model = Dump
        fields = "__all__"
        depth = 1


class ProcessSerializer(ModelSerializer):
    class Meta:
        model = Process
        fields = "__all__"
        depth = 2 # use depth = int value to go in depth of relation of two model


class ThreadSerializer(ModelSerializer):
    class Meta:
        model = Thread
        fields = "__all__"


class HandleSerializer(ModelSerializer):
    class Meta:
        model = Handle
        fields = "__all__"


class DLLSerializer(ModelSerializer):
    class Meta:
        model = DLL
        fields = "__all__"


class RegistryHiveSerializer(ModelSerializer):
    class Meta:
        model = RegistryHive
        fields = "__all__"


class NetworkConnectionSerializer(ModelSerializer):
    class Meta:
        model = NetworkConnection
        fields = "__all__"


class ScanInformationSerializer(ModelSerializer):
    class Meta:
        model = ScanInformation
        fields = "__all__"


class ScanResultSerializer(ModelSerializer):
    class Meta:
        model = ScanResult
        fields = "__all__"


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
