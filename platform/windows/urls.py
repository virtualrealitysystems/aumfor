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

import api.windows.viewsets
import views

app_name = "platform.windows"

router = routers.DefaultRouter()
router.register(r'dumps', api.windows.viewsets.DumpViewSet)
router.register(r'processes', api.windows.viewsets.ProcessViewSet)
router.register(r'threads', api.windows.viewsets.ThreadViewSet)
router.register(r'handles', api.windows.viewsets.HandleViewSet)
router.register(r'dlls', api.windows.viewsets.DLLViewSet)
router.register(r'registry-hives', api.windows.viewsets.RegistryHiveViewSet)
# router.register(r'command-history', api.windows.viewsets.CommandHistoryViewSet)
router.register(r'network-connections', api.windows.viewsets.NetworkConnectionViewSet)
router.register(r'scans', api.windows.viewsets.ScanInformationViewSet)
router.register(r'scan-results', api.windows.viewsets.ScanResultViewSet)
router.register(r'reports', api.windows.viewsets.ReportViewSet)

urlpatterns = [
    url(r'^json/', include(router.urls)),
    url(r'^analyze/info/', views.AnalyzeDumpInfo.as_view()),
    url(r'^analyze/processes/', views.AnalyzeProcesses.as_view()),
    url(r'^analyze/threads/', views.AnalyzeThreads.as_view()),
    url(r'^analyze/dll/', views.AnalyzeDll.as_view()),
    url(r'^analyze/handles/', views.AnalyzeHandle.as_view()),
    url(r'^analyze/registry-hives/', views.AnalyzeRegistryHives.as_view()),
    url(r'^analyze/network-connections/', views.AnalyzeNetworkConnections.as_view()),
    url(r'^analyze/summary/', views.AnalyzeSummary.as_view()),
    url(r'^process/download/', views.DownloadProcess.as_view()),
    url(r'^process/scan/', views.ScanProcess.as_view()),
    url(r'^process/scanned/', views.ScanProcess.get_scanned_processes),
    url(r'^process/report/', views.Report.as_view()),
    url(r'^process/userupload/', views.userDump.as_view()),
    url(r'^process/regeport/', views.RegistryReport.as_view()),
    url(r'^process/netreport/', views.NetworkReport.as_view()),
    url(r'^process/uploadreport/', views.UploadReport.as_view()),
    url(r'^process/scanreport/', views.ScanReport.as_view()),
    url(r'^process/threadreport/', views.threadReport.as_view()),
    url(r'^process/handlesreport', views.handleReport.as_view()),
    url(r'^process/dllreport', views.dllReport.as_view()),

]
