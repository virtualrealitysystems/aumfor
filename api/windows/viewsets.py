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

from rest_framework.viewsets import ModelViewSet

from api.windows.serializers import *


# this all viewset get all the field of database and filter it to cover it into json form by serilizer
class DumpViewSet(ModelViewSet):
    queryset = Dump.objects.all()
    serializer_class = DumpSerializer
    filter_fields = "__all__"


class ProcessViewSet(ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    filter_fields = "__all__"


class ThreadViewSet(ModelViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    filter_fields = "__all__"


class HandleViewSet(ModelViewSet):
    queryset = Handle.objects.all()
    serializer_class = HandleSerializer
    filter_fields = "__all__"


class DLLViewSet(ModelViewSet):
    queryset = DLL.objects.all()
    serializer_class = DLLSerializer
    filter_fields = "__all__"


class RegistryHiveViewSet(ModelViewSet):
    queryset = RegistryHive.objects.all()
    serializer_class = RegistryHiveSerializer
    filter_fields = "__all__"


class NetworkConnectionViewSet(ModelViewSet):
    queryset = NetworkConnection.objects.all()
    serializer_class = NetworkConnectionSerializer
    filter_fields = "__all__"


class ScanInformationViewSet(ModelViewSet):
    queryset = ScanInformation.objects.all()
    serializer_class = ScanInformationSerializer
    filter_fields = "__all__"


class ScanResultViewSet(ModelViewSet):
    queryset = ScanResult.objects.all()
    serializer_class = ScanResultSerializer
    filter_fields = "__all__"


class ReportViewSet(ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_fields = "__all__"
