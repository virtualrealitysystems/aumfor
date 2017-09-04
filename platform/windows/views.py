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

import time
from datetime import datetime
from json import loads
from os import remove

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from platform.common.upload import Upload
from platform.windows import models
from platform.windows.dumps.dump import Dump
from platform.windows.dumps.networkconnection import NetworkConnection
from platform.windows.dumps.registryhive import RegistryHive
from platform.windows.processes.dll import DLL
from platform.windows.processes.handle import Handle
from platform.windows.processes.process import Process
from platform.windows.processes.thread import Thread

start_at = 0
start_time = 0
end_time = 0


class AnalyzeDumpInfo(APIView):
    """ Analyzes the memory image and retrieves it's basic information. """

    def post(self, request):
        global start_time
        start_time = time.time()
        global start_at
        start_at = datetime.now().ctime()
        try:

            # Getting the data from POST-ed data.
            data = request.data.get("data")

            # Checking if data is not specified.
            if not data:
                raise Exception("No data was specified.")

            # Getting the User ID.
            platform = request.data.get("platform")

            # Checking if User ID was not specified.
            if not platform:
                raise Exception("No platform was specified.")

            # Converting JSON string to dictionary.
            data = loads(data)

            # Getting User and Zip object from data.
            user = User.objects.get(pk=request.session["api_user"])

            # Saving upload information in the database.
            upload = Upload(user, data["dump_location"], platform)
            upload.save()

            # Saving dump information in the database.
            dump = Dump(upload)
            dump.save()

            # Returning the response.
            return HttpResponse('{"success":1, "status":"Basic image analysis complete.", "data":%s}'
                                % ('{"upload":%s, "dump":%s}' % (upload.serialize().replace("\\", "/"),
                                                                 dump.serialize().replace("\\", "/"))))

        except Exception as ex:

            # Returning any exception messages.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))

        finally:
            pass


class AnalyzeProcesses(APIView):
    """ Analyzes the memory image and retrieves running processes. """

    def post(self, request):

        try:

            # Getting the data from POST-ed data.
            data = request.data.get("data")

            # Checking if data is not specified.
            if not data:
                raise Exception("No data was specified.")

            # Converting JSON string to dictionary.
            data = loads(data)

            # Getting dump from POST-ed data and deserializing back into object.
            dump = Dump.deserialize(data["dump"])

            # Saving the processes from dump.
            Process(dump).save()

            # Returning the response.
            return HttpResponse('{"success":1, "status":"Process analysis complete."}')

        except Exception as ex:

            # Returning any exception messages.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class AnalyzeThreads(APIView):
    """ Analyze Threads of Dumps in a single traction """

    def post(self, request):

        try:
            # Getting data from api request
            data = request.data.get("data")

            if not data:
                raise Exception("No data was specified.")

            # converting JSON string to dictionary.
            data = loads(data)

            # get data form post req and deserialize it into the dump object
            dump = Dump.deserialize(data["dump"])

            Thread(dump).save()

            return HttpResponse('{"success":1, "status":"Thread Analyzes complete."}')

        except Exception as ex:
            # Returning any exception messages.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class AnalyzeDll(APIView):
    """ Analyze Dll of Dumps in a single traction """

    def post(self, request):

        try:
            # Getting data from api request
            data = request.data.get("data")

            if not data:
                raise Exception("No data was specified.")

            # converting JSON string to dictionary.
            data = loads(data)

            # get data form post req and deserialize it into the dump object
            dump = Dump.deserialize(data["dump"])

            DLL(dump).save()

            return HttpResponse('{"success":1, "status":"Dll Analyzes complete."}')

        except Exception as ex:
            # Returning any exception messages.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))

        finally:
            pass


class AnalyzeHandle(APIView):
    """ Analyze Dll of Dumps in a single traction """

    def post(self, request):

        try:
            # Getting data from api request
            data = request.data.get("data")

            if not data:
                raise Exception("No data was specified.")

            # converting JSON string to dictionary.
            data = loads(data)

            # get data form post req and deserialize it into the dump object
            dump = Dump.deserialize(data["dump"])

            Handle(dump).save()

            return HttpResponse('{"success":1, "status":"Handles Analyzes complete."}')

        except Exception as ex:
            # Returning any exception messages.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))

        finally:
            pass


class AnalyzeRegistryHives(APIView):
    """ Analyzes the memory image and saves registry hives to the database. """

    def post(self, request):

        try:

            # Getting the data from POST-ed data.
            data = request.data.get("data")

            # Checking if data is not specified.
            if not data:
                raise Exception("No data was specified.")

            # Converting JSON string to dictionary.
            data = loads(data)

            # Getting dump from POST-ed data and deserializing back into object.
            dump = Dump.deserialize(data["dump"])

            # Saving the Registry Hives.
            RegistryHive(dump).save()

            # Returning the response.
            return HttpResponse('{"success":1, "status":"Registry Hive analysis complete."}')

        except Exception as ex:

            # Returning any exception messages.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class AnalyzeNetworkConnections(APIView):
    """ Analyzes the memory image and retrieves network connections. """

    def post(self, request):

        try:
            # print (request.data.get("data"))
            # Getting the data from POST-ed data.
            data = request.data.get("data")

            # Checking if data is not specified.
            if not data:
                raise Exception("No data was specified.")

            # Converting JSON string to dictionary.
            data = loads(data)

            # Getting dump from POST-ed data and deserializing back into object.
            dump = Dump.deserialize(data["dump"])

            # Checking if Operating System of the dump is Windows XP.
            print(dump.profile.startswith("Win"))
            if dump.profile.startswith("Win"):
                # pass
                # Saving open network connections data.
                NetworkConnection(dump).save()

            # Getting JSON data of upload from data and deserializing into object.
            upload = Upload.deserialize(data["upload"])

            # Changing status of dump to "analyzed" in the database.
            upload.update_status()

            dump.update_endtime();

            # Returning the response.
            # session['newdump'] = 17
            request.session['newdump'] = dump.model.pk
            return HttpResponse('{"success":1, "status":"Done!", "dump":%s}' % dump.model.pk)

        except Exception as ex:

            # Returning any exception messages.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))

        finally:

            # Removing session variables.
            if request.session.get("api_user") is not None:
                del request.session["api_user"]


class AnalyzeSummary(APIView):
    """
        this class gives summary about uploded dump Analysis
            - no of process , threads , dll , hadles , network-connections
              reg hives an time taken to analyze all things
    """

    def post(self, request):

        #  convert date into appropriate format
        temp = time.time() - start_time
        hours = temp // 3600
        temp = temp - 3600 * hours
        minutes = int(temp // 60)
        sec = int(temp - 60 * minutes)

        # end time of dump analuzed completely
        end_time = datetime.now().ctime()

        try:
            # get data from request
            print (type(request.data))
            # print (request.data.get("data"))
            # data = loads(request.data)
            print("data", request.data)
            data = request.data.get("data")

            if not data:
                raise Exception("no data provided")

            # convert json data into dictionary
            data = loads(data)

            # Getting dump from POST-ed data and deserialize back into object.
            dump = Dump.deserialize(data["dump"])

            if dump:
                process = models.Process.objects.filter(dump=dump.model)
                total_process = len(process)

                thread = models.Thread.objects.filter(dump=dump.model)
                total_thread = len(thread)

                dll = models.DLL.objects.filter(dump=dump.model)
                total_dll = len(dll)

                handles = models.Handle.objects.filter(dump=dump.model)
                total_handles = len(handles)

                reghives = models.RegistryHive.objects.filter(dump=dump.model)
                total_reghives = len(reghives)

                network = models.NetworkConnection.objects.filter(dump=dump.model)
                total_network = len(network)

                # Returning the response.
                return HttpResponse('{"success":1, "status":"analysis complete." , "data":%s}' % (
                    '{"total_process":%s,"total_thread":%s,"total_dll":%s,"total_handles":%s,"total_reghives":%s,"total_network":%s,"time_min":%s,"time_sec":%s,"start_time":"%s","end_time":"%s"}' % (
                        total_process, total_thread, total_dll, total_handles, total_reghives, total_network, minutes,
                        sec,
                        start_at, end_time)))

        except Exception as ex:
            # Returning any exception messages.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class DownloadProcess(APIView):
    """ Downloads a process executable as a ZIP archive. """

    def get(self, request):

        try:

            # Getting Process ID.
            process = request.GET.get("process")

            # Checking if Process ID is None.
            if not process:
                raise Exception("No Process ID was specified.")

            # Compressing the process executable and getting archive path.
            zip_with_path, name = Process.compress(process)

            try:

                # Opening the archive in read mode.
                with open(zip_with_path, "rb") as fsock:

                    # Specifying the content and the content type of response.
                    response = HttpResponse(content=fsock, content_type="application/zip")

                    # Specifying the response type as an attachment and name of the file to be downloaded.
                    response["Content-Disposition"] = "attachment; filename=%s.zip" % name

                    # Specifying the length of the file in response header.
                    response["Content-Length"] = fsock.tell()

                    # Returning the response.
                    return response

            except Exception as ex:
                return HttpResponse('{" something went wrong%s"}' % str(ex))

            finally:
                # Deleting the compressed executable.
                remove(zip_with_path)

        except Exception as ex:
            print(str(ex))
            # output = '<html><body><script >alert("%s")</script></body></html>'%(str(ex).replace("'","")).replace('"',"")
            # Returning any exception messages.
            # return HttpResponse('{"success":0, "error":"%s"}' % str(ex))
            output = '<html><body><script >alert("%s");window.location.href = "/process/";</script></body></html>' % (
                "can not download the process because of some information is missing")
            return HttpResponse(output)
            # finally:
            #     pass


class ScanProcess(APIView):
    """ Scans specified process for threats. """

    def post(self, request):

        try:

            # Getting Process ID.
            process = request.data.get("process")

            # Checking if no list is specified.
            if not process:
                raise Exception("Process ID was not specified.")

            # Scanning the process, saving the results to the database
            # and getting Scan ID..
            scan_id = Process.scan(process)

            # Reporting success.
            return HttpResponse('{"success":1, "scan":%s}' % scan_id)

        except Exception as ex:

            # Reporting errors if any.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))

    @staticmethod
    @api_view(['POST'])
    def get_scanned_processes(request):

        """ Gets scanned processes based on specified dump. """

        try:

            # Getting the dump.
            dump = request.data.get("dump")

            # Checking if no dump is specified.
            if dump is None:
                raise Exception("No dump was specified.")

            # Getting the scanned processes from database.
            scanned_processes = Process.get_scanned_processes(dump)

            # Returning the response with success.
            return HttpResponse('{"success":1, "data":%s}' % scanned_processes)

        except Exception as ex:

            # Returning the response with error.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class Report(APIView):
    """ Generates report of specified processes. """

    def get(self, request):

        try:

            # Getting the list of Process IDs.
            raw_process_list = request.GET.get("processes")

            # Checking if a non-empty process list is specified.
            if raw_process_list and raw_process_list != "":

                # Getting location of the report file (PDF) for specified processes.
                location, dumpname = Process.get_report(str(raw_process_list))

            else:

                raise Exception("No processes or report ID were specified.")

            # Opening the PDF in read-binary mode.
            with open(location, "rb") as fsock:

                # Initializing a new object of HttpResponse class, with the file as content.
                response = HttpResponse(content=fsock, content_type="application/pdf")

                # Specifying the Content as attachment.
                now = datetime.now()
                response["Content-Disposition"] = "attachment; filename=AnalyzedProcess_%s_%s/%s/%s.pdf" % (
                    str(dumpname), str(now.strftime("%Y")), str(now.strftime("%m")), str(now.strftime("%d")))

                # Returning the response.
                return response

        except Exception as ex:

            # Reporting errors if any.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class userDump(APIView):
    """
        This API return Dump Info Of currently Logedin user info
    """

    def post(self, request):

        try:

            data = request.data.get("user")
            L = []
            if data is None:
                raise Exception("No loged user Specified Please Login")

            if models.Upload.objects.filter(user=data):
                for i in models.Upload.objects.filter(user=data):
                    # list = [i.pk, i.dump_location]
                    # print(list[0])
                    L.append({"id": i.pk, "name": i.dump_location})
            # return HttpResponse('{"success":1, "status":"Done!", "data":%s}' %d )
            return Response(L)
        except Exception as e:
            return HttpResponse('{"success":0, "error":%s}' % e)


class ScanReport(APIView):
    """ Generates report of specified processes. """

    def get(self, request):

        try:

            # Getting the list of Process IDs.
            raw_process_list = request.GET.get("scanid")

            # Checking if a non-empty process list is specified.
            if raw_process_list and raw_process_list != "":

                # Getting location of the report file (PDF) for specified processes.
                location, p_name, dumpname = Process.get_scanreport(str(raw_process_list))
            else:

                # Getting the Report ID.
                report_id = request.data.get("report")

                # Checking if a Report ID is specified.
                if report_id:

                    # Getting report from the database.
                    location, p_name, dumpname = Process.get_scanreport(int(report_id))

                # Checking if no process or report ID was specified.
                else:
                    raise Exception("No processes or report ID were specified.")

            # Opening the PDF in read-binary mode.
            with open(location, "rb") as fsock:

                # Initializing a new object of HttpResponse class, with the file as content.
                response = HttpResponse(content=fsock, content_type="application/pdf")

                # Specifying the Content as attachment.
                now = datetime.now()
                response["Content-Disposition"] = "attachment; filename=Scanned_%s_%s_%s/%s/%s.pdf" % (
                    str(dumpname), str(p_name), str(now.strftime("%Y")), str(now.strftime("%m")),
                    str(now.strftime("%d")))

                # Returning the response.
                return response

        except Exception as ex:
            # Reporting errors if any.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class RegistryReport(APIView):
    """ Generates report of specified processes. """

    def get(self, request):

        try:

            # Getting the list of Process IDs.
            raw_process_list = request.GET.get("regid")

            # Checking if a non-empty process list is specified.
            if raw_process_list and raw_process_list != "":

                # Getting location of the report file (PDF) for specified processes.
                location, dumpname = Process.get_regreport(str(raw_process_list))
            else:

                # Getting the Report ID.
                report_id = request.data.get("report")

                # Checking if a Report ID is specified.
                if report_id:

                    # Getting report from the database.
                    location, dumpname = Process.get_regreport(int(report_id))

                # Checking if no process or report ID was specified.
                else:
                    raise Exception("No processes or report ID were specified.")

            # Opening the PDF in read-binary mode.
            with open(location, "rb") as fsock:

                # Initializing a new object of HttpResponse class, with the file as content.
                response = HttpResponse(content=fsock, content_type="application/pdf")

                # Specifying the Content as attachment.
                now = datetime.now()
                response["Content-Disposition"] = "attachment; filename=RegistryhivesReport-%s-%s/%s/%s.pdf" % (
                    str(dumpname), str(now.strftime("%Y")), str(now.strftime("%m")), str(now.strftime("%d")))

                # Returning the response.
                return response

        except Exception as ex:
            # Reporting errors if any.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class NetworkReport(APIView):
    """ Generates report of specified processes. """

    def get(self, request):

        try:

            # Getting the list of Process IDs.
            raw_process_list = request.GET.get("netid")

            # Checking if a non-empty process list is specified.
            if raw_process_list and raw_process_list != "":

                # Getting location of the report file (PDF) for specified processes.
                location, dumpname = Process.get_networkreport(str(raw_process_list))
            else:

                # Getting the Report ID.
                report_id = request.data.get("report")

                # Checking if a Report ID is specified.
                if report_id:

                    # Getting report from the database.
                    location, dumpname = Process.get_networkreport(int(report_id))

                # Checking if no process or report ID was specified.
                else:
                    raise Exception("No processes or report ID were specified.")

            # Opening the PDF in read-binary mode.
            with open(location, "rb") as fsock:

                # Initializing a new object of HttpResponse class, with the file as content.
                response = HttpResponse(content=fsock, content_type="application/pdf")

                # Specifying the Content as attachment.
                now = datetime.now()
                response["Content-Disposition"] = "attachment; filename=NetworkConnection-%s-%s/%s/%s.pdf" % (
                    str(dumpname), str(now.strftime("%Y")), str(now.strftime("%m")), str(now.strftime("%d")))

                # Returning the response.
                return response

        except Exception as ex:
            # Reporting errors if any.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class UploadReport(APIView):
    """ Generates report of specified processes. """

    def get(self, request):

        try:

            # Getting the list of Process IDs.
            raw_process_list = request.GET.get("uploadid")

            # Checking if a non-empty process list is specified.
            if raw_process_list and raw_process_list != "":

                # Getting location of the report file (PDF) for specified processes.
                location = Process.get_uploadkreport(str(raw_process_list))
            else:

                # Getting the Report ID.
                report_id = request.data.get("report")

                # Checking if a Report ID is specified.
                if report_id:

                    # Getting report from the database.
                    location = Process.get_uploadkreport(int(report_id))

                # Checking if no process or report ID was specified.
                else:
                    raise Exception("No processes or report ID were specified.")

            # Opening the PDF in read-binary mode.
            with open(location, "rb") as fsock:

                # Initializing a new object of HttpResponse class, with the file as content.
                response = HttpResponse(content=fsock, content_type="application/pdf")

                # Specifying the Content as attachment.
                now = datetime.now()
                response["Content-Disposition"] = "attachment; filename=Uploaded-Dumps_%s/%s/%s.pdf" % (
                    str(now.strftime("%Y")), str(now.strftime("%m")), str(now.strftime("%d")))

                # Returning the response.
                return response

        except Exception as ex:
            # Reporting errors if any.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))


class threadReport(APIView):
    """ Generates report of specified processes. """

    def get(self, request):

        try:

            # Getting the list of Process IDs.
            raw_process_list = request.GET.get("threadid")

            # Checking if a non-empty process list is specified.
            if raw_process_list and raw_process_list != "":

                # Getting location of the report file (PDF) for specified processes.
                location, dumpname = Process.get_threadreport(str(raw_process_list))
            else:

                # Getting the Report ID.
                report_id = request.data.get("report")

                # Checking if a Report ID is specified.
                if report_id:

                    # Getting report from the database.
                    location, dumpname = Process.get_threadreport(int(report_id))

                # Checking if no process or report ID was specified.
                else:
                    raise Exception("No processes or report ID were specified.")

            # Opening the PDF in read-binary mode.
            with open(location, "rb") as fsock:

                # Initializing a new object of HttpResponse class, with the file as content.
                response = HttpResponse(content=fsock, content_type="application/pdf")

                # Specifying the Content as attachment.
                now = datetime.now()
                response["Content-Disposition"] = "attachment; filename=ThreadReport-%s-%s/%s/%s.pdf" % (
                    str(dumpname), str(now.strftime("%Y")), str(now.strftime("%m")), str(now.strftime("%d")))

                # Returning the response.
                return response

        except Exception as ex:
            # Reporting errors if any.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))

        finally:
            pass


class handleReport(APIView):
    """ Generates report of specified processes. """

    def get(self, request):

        try:

            # Getting the list of Process IDs.
            raw_process_list = request.GET.get("handleid")

            # Checking if a non-empty process list is specified.
            if raw_process_list and raw_process_list != "":

                # Getting location of the report file (PDF) for specified processes.
                location, process_name, dumpname = Process.get_handlereport(str(raw_process_list))
            else:

                # Getting the Report ID.
                report_id = request.data.get("report")

                # Checking if a Report ID is specified.
                if report_id:

                    # Getting report from the database.
                    location, process_name, dumpname = Process.get_handlereport(int(report_id))

                # Checking if no process or report ID was specified.
                else:
                    raise Exception("No processes or report ID were specified.")

            # Opening the PDF in read-binary mode.
            with open(location, "rb") as fsock:

                # Initializing a new object of HttpResponse class, with the file as content.
                response = HttpResponse(content=fsock, content_type="application/pdf")

                # Specifying the Content as attachment.
                now = datetime.now()
                response["Content-Disposition"] = "attachment; filename=Handels-%s-%s-%s/%s/%s.pdf" % (
                    str(dumpname), str(process_name), str(now.strftime("%Y")), str(now.strftime("%m")),
                    str(now.strftime("%d")))

                # Returning the response.
                return response

        # except Exception as ex:
        #     # Reporting errors if any.
        #     return HttpResponse('{"success":0, "error":"%s"}' % str(ex))

        finally:
            pass


class dllReport(APIView):
    """ Generates report of specified processes. """

    def get(self, request):

        try:

            # Getting the list of Process IDs.
            raw_process_list = request.GET.get("dllid")

            # Checking if a non-empty process list is specified.
            if raw_process_list and raw_process_list != "":

                # Getting location of the report file (PDF) for specified processes.
                location, process_name, dumpname = Process.get_dlllereport(str(raw_process_list))
            else:

                # Getting the Report ID.
                report_id = request.data.get("report")

                # Checking if a Report ID is specified.
                if report_id:

                    # Getting report from the database.
                    location, process_name, dumpname = Process.get_dlllereport(int(report_id))

                # Checking if no process or report ID was specified.
                else:
                    raise Exception("No processes or report ID were specified.")

            # Opening the PDF in read-binary mode.
            with open(location, "rb") as fsock:

                # Initializing a new object of HttpResponse class, with the file as content.
                response = HttpResponse(content=fsock, content_type="application/pdf")

                # Specifying the Content as attachment.
                now = datetime.now()
                response["Content-Disposition"] = "attachment; filename=Dll-%s-%s-%s/%s/%s.pdf" % (
                    str(dumpname), str(process_name), str(now.strftime("%Y")), str(now.strftime("%m")),
                    str(now.strftime("%d")))

                # Returning the response.
                return response

        except Exception as ex:
            # Reporting errors if any.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))

        finally:
            pass
