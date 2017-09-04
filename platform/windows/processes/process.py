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

from cStringIO import StringIO
from datetime import datetime
from json import dumps
from os import path, makedirs, remove, getcwd, chdir
from shutil import move

from django.conf import settings
from django.shortcuts import render_to_response
from requests import post
from xhtml2pdf import pisa

from platform.common.utilities import Utilities
from platform.common.zip import Zip
from platform.models import Upload
from platform.windows import models


class Process(object):
    """ Contains information and functionality related to processes. """

    def __init__(self, dump):

        """
        Initializes a new instance of Process object.

        :param dump: Dump from which process data will be obtained.

        """

        # Initializing instance objects.
        self.dump = dump
        self.json = ""

    def save(self):

        # Initializing an empty list.
        output = []

        # Iterating the commands.
        for plugin in ('pslist', 'pstree', 'psscan'):
            # Executing the command and appending it's output in the list.
            output.append(Utilities.get_output(self.dump.location, plugin,
                                               self.dump.profile, self.dump.suggested_profiles, "--output=greptext"))

        # Converting the raw string output to list.
        output = Utilities.separate_raw_data(output)

        # Removing redundant data and fields from the output.
        final_list = Process.remove_redundancy(output)

        # Saving the processes' data in database.
        self._save_processes_to_database(final_list)

    @staticmethod
    def remove_redundancy(output_lists):

        """
        Removes redundancy from output fields of the commands.

        :param output_lists: Output lists.

        :return: Filtered data.

        """

        # Creating new references of the lists, just for clarification.
        pslist, pstree, psscan = output_lists[0], output_lists[1], output_lists[2]
        del pslist[-1], pstree[-1], psscan[-1]

        # Looping through the list of pslist command output...
        for i in range(0, len(pslist)):

            # Looping through the list of pstree command output...
            for j in range(0, len(pstree)):

                # If the Process IDs of the two list elements match.
                if pslist[i][2] == pstree[j][2]:
                    # Remove the line from pstree output.
                    del pstree[j]

                    # Break the loop.
                    break

        # If there are still lines left in pstree list...
        if pstree:

            # Looping through the pstree list.
            for j in range(0, len(pstree)):
                # Creating a new row in pslist from pstree list.
                pslist.append([pstree[j][0], pstree[j][1], pstree[j][2], pstree[j][3],
                               pstree[j][4], pstree[j][5], None, '0', pstree[j][6], None])

        # Looping through the pslist list.
        for i in range(0, len(pslist)):

            # Looping through the psscan list.
            for j in range(0, len(psscan)):

                # If the PIDs of two processes match...
                if pslist[i][2] == psscan[j][2]:
                    # Appending the required fields to the current line in pslist.
                    pslist[i].append(psscan[j][0])
                    pslist[i].append(psscan[j][4])

                    # Deleting the line from the psscan list.
                    del psscan[j]

                    # Breaking the loop.
                    break

        # If there are lines left in psscan list.
        if psscan:

            # Iterating through the psscan list.
            for j in range(0, len(psscan)):
                # Creating a row for pslist and appending lst to pslist.
                pslist.append([None, psscan[j][1], psscan[j][2], psscan[j][3],
                               None, None, None, None, psscan[j][5], psscan[j][6],
                               psscan[j][0], psscan[j][4]])

        # Initializing an empty list.
        final_list = []

        # Iterating through elements of pslist.
        for line in pslist:

            # Checking if 8th position is not None.
            if line[8]:
                # Remove the UTC part.
                line[8] = " ".join(line[8].split(" ")[0:2])

            # Checking if 9th position is not None.
            if line[9]:
                # Remove the UTC part.
                line[9] = " ".join(line[9].split(" ")[0:2])

            # Changing the positions of Offset(V) from first to 11th.
            final_list.append(line[1:10] + [line[0]] + line[10:])

        # Deleting the list references.
        del pslist, pstree, psscan

        # Returning the final list.
        return final_list

    def _save_processes_to_database(self, lst):

        """
        Saves the specified list in the database.

        :param lst: List to be saved in the database.

        """

        # Iterating through the list.
        for line in lst:

            # The following "if" condition looks silly and unnecessary...
            # but actually it's a workaround for a very annoying problem.

            # For some reason, 3 rows with NULL as column values were getting
            # inserted in the database and there were no problems with 'lst'.
            # So, it looked like the problem was related to Django's MySQL database drivers.
            # This solution will have to do for now.

            # If the PID is None, skip the iteration, so empty data would
            # not be inserted in the database.
            if line[1] is None:
                continue

            # Creating a new model object.
            process = models.Process(**{
                "name": line[0],
                "pid": int(line[1]),
                "ppid": int(line[2]),
                "thread_count": int(line[3]) if line[3] is not None else None,
                "handle_count": int(line[4]) if line[4] is not None else None,
                "session": int(line[5]) if line[5] is not None else None,
                "wow64": int(line[6]) if line[6] is not None else None,
                "creation_time": line[7] if line[7] is not None else None,
                "termination_time": line[8] if line[8] is not None else None,
                "offset_v": line[9] if line[9] is not None else None,
                "offset_p": line[10] if line[10] is not None else None,
                "pdb": line[11] if line[11] is not None else None,
                "dump": self.dump.model
            })

            # Save it to the database.
            process.save()

            # Generating JSON.
            # self.json += (", " if self.json != "" else "") + JSONRenderer().render(ProcessSerializer(process).data)

    @staticmethod
    def save_process_to_disk(process_pk):

        """
        Saves the specified process to the HDD.

        :param process_pk: Primary Key of the Process object.

        :return: Physical location of the saved executable.

        """

        # Getting the processes based on primary key.
        process = models.Process.objects.get(pk=process_pk)

        # Getting Dump and Upload objects based on Process object.
        dump = process.dump
        upload = dump.upload

        # Specifying destination directory of the executable to be saved.
        des_dir = "%s/executables" % path.dirname(upload.dump_location)

        # Creating the destination directories if they do not exist.
        if not path.exists(des_dir):
            makedirs(des_dir)

        # Saving the process executable using "procdump" command.
        output = Utilities.get_output(upload.dump_location, "procdump", dump.profile, dump.suggested_profiles,
                                      " --pid=%s --dump-dir=%s --output=greptext"
                                      % (process.pid, des_dir))

        # Separating the 2nd line of output with pipe sign,
        # getting the last element and separating it with space.
        parts = output[1].split("|")[-1].split(" ", 2)

        # Checking if the first part starts wtih text "Error",
        # indicating this process can't be downloaded.
        if parts[0].startswith("Error"):
            # print parts[0]
            return None
        # Getting the executable name.
        exe_name = parts[1].strip("\r")

        # Specifying old and new paths of executables.
        exe_old_path = "%s/%s" % (des_dir, exe_name)
        exe_new_path = "%s/%s" % (des_dir, process.name)

        # Renaming the executable to it's original name.
        move(exe_old_path, exe_new_path)

        # Returning the new executable path.
        return exe_new_path

    @staticmethod
    def compress(process):

        """
        Compresses specified process and saves it to the disk.

        :param process: Process to be compressed.

        :return: Location of the compressed processes.

        """

        # Saving the process executable to disk and appending its location to the list
        exe_location = Process.save_process_to_disk(process)
        processname = models.Process.objects.get(pk=process)

        # Checking if process was not saved.
        if exe_location is None:
            raise Exception("Cannot download this process.")

        # Getting the directory of the executables.
        exe_dir = path.dirname(exe_location)

        # Getting the executable name.
        exe_name = path.basename(exe_location)

        # Saving the location of the current working directory.
        current_dir = getcwd()

        # Changing to executables' directory.
        chdir(exe_dir)

        # Specifying the full path of the archive with current timestamp.
        zip_file_path = "%s/%s.zip" % (exe_dir, datetime.now().strftime("%Y%m%d-%H%M%S"))

        # Compressing the executables.
        Zip.compress((exe_name,), path.basename(zip_file_path))

        # Switching back to original directory.
        chdir(current_dir)

        # Returning the zip path.
        return zip_file_path, processname.name

    @staticmethod
    def scan(process_pk):

        scan_model = None

        try:

            # Getting scan results of process if it exists.
            scan_model = models.ScanInformation.objects.get(process=process_pk)

            # Checking if a ScanInformation object is obtained.
            if scan_model is not None:

                # Checking if last scanned date is at least a day old.
                if datetime.now().day > scan_model.scan_date.day:

                    # Raising Does Not Exist exception.
                    raise models.ScanInformation.DoesNotExist()

                else:

                    # Returning it's scan ID.
                    return scan_model.pk

        # In case object is not found, just continue.
        except models.ScanInformation.DoesNotExist:
            pass

        # Saving the process to disk for scanning.
        saved_process_location = Process.save_process_to_disk(process_pk)

        # Checking if process was not saved.
        if saved_process_location is None:
            raise Exception("Process can not be scanned.")

        # Getting the name of executable.
        exe_name = path.basename(saved_process_location)

        # opening the file in read-binary mode.
        with open(saved_process_location, "rb") as executable:
            # specify your virus total public api key put in settigs.py
            # Specifying the API Key.
            print(">>>>>>>>>> API KeY >>>>>>>>> ", settings.API_KEY);
            params = {"apikey": settings.API_KEY}

            # Specifying the executable to be scanned.
            files = {'file': (exe_name, executable)}

            # POST-ing the data to the VirusTotal API.
            response = post("https://www.virustotal.com/vtapi/v2/file/scan", files=files, params=params)

        # Getting the response in JSON.
        json_response = response.json()
        # Specifying the headers.
        headers = {
            "Accept-Encoding": "gzip, deflate",
            "User-Agent": "gzip"
        }

        # Getting the hash of uploaded file.
        params["resource"] = json_response["resource"]

        # POST-ing the hash to get scan results.
        response = post("https://www.virustotal.com/vtapi/v2/file/report", params=params, headers=headers)

        # Getting the Scan Result as dictionary.
        scan_info = response.json()

        # Extracting the individual anti-virus scan results from the dictionary.
        anti_viruses = scan_info.pop("scans")

        # Specifying the process model of the scan results.
        scan_info["process"] = models.Process.objects.get(pk=process_pk)

        # Checking if scan_model is None.
        if scan_model is None:

            # Creating and saving the model.
            scan_model = models.ScanInformation(**scan_info)
            scan_model.save()

        else:

            # Updating the existing model data.
            for key in scan_info:
                setattr(scan_model, key, scan_info[key])

            # Saving the model.
            scan_model.save()

            # Removing anti-virus results.
            models.ScanResult.objects.filter(scan_information=scan_model).delete()

        # Iterating through each dictionary items.
        for key, value in anti_viruses.viewitems():

            # Adding the required fields in the dictionary.
            value["anti_virus_name"] = key
            value["scan_information"] = scan_model

            # Checking if the result is None.
            if value["result"] is None:
                # Setting None text.
                value["result"] = "None"

            # Creating and saving the model.
            models.ScanResult.objects.create(**value)

        # Removing saved process.
        remove(saved_process_location)

        # Returning the Scan ID.
        return scan_model.pk

    @staticmethod
    def get_scanned_processes(dump):

        """
        Gets scanned processes of the speficied dump.

        :param dump: Dump whose scanned processes will be retrieved.

        :return: List of scanned processes as JSON.

        """

        # Initializing an empty list.
        data = []

        # Getting the scanned process models and iterating through them.
        for info in models.ScanInformation.objects.filter(process__dump__pk=dump):
            # Appending them to the list.
            data.append({
                "id": info.process.pk,
                "process": info.process.pid,
                "process_name": info.process.name,
                "scan_date": info.scan_date.strftime("%Y-%m-%d %H:%M:%S"),
                "total": info.total,
                "positives": info.positives
            })

        # Converting the list of dictionaries to JSON and returning it.
        return dumps(data)

    @staticmethod
    def get_report(param):

        """
        Generates a report about specified processes.

        :param param: List of processes to be included in the report.

        :return: Location of the generated PDF document of the report.

        """

        # Checking if the parameter is a string.
        if isinstance(param, str):

            try:

                # Getting report of specified processes from the database.
                report = models.Report.objects.get(processes=param)

                # Checking if a report is found.
                if report is not None:
                    # Returning the location of already-generated report.
                    return report.location

            except models.Report.DoesNotExist:

                # Initializing an empty list.
                processes = []

                # Converting raw (JSON) process list to list and iterating through it.
                for item in param.split(","):

                    # Getting the process data from database.
                    process = models.Process.objects.get(pk=item)

                    # Checking if the process exists:
                    if process:
                        # Adding process to the list.
                        processes.append(process)

                # Getting the current datetime.
                now = datetime.now().strftime("%Y:%m:%d - %H:%M:%S")

                # Getting the dump name.
                dump_location = processes[0].dump.upload.dump_location

                # Rendering the output of report page.
                output = render_to_response('report.html', {
                    "processes": processes,
                    "date": now,
                    "dump": path.basename(dump_location)
                })

                # Specifying the directory where report will be stored;
                # that is, parent directory of dump location.
                location = "%s/reports" % path.dirname(dump_location)

                # Checking if the directory does not exist.
                if not path.exists(location):
                    # Making the directory.
                    makedirs(location)

                # Specifying the name of the PDF as current datetime.
                location = "%s/%s.pdf" % (location, datetime.now().strftime("%Y%m%d"))
                # print (location)
                # Saving the PDF.
                result = StringIO()
                pisa.pisaDocument(StringIO(output.content), dest=result)

                with open(location, "wb") as pdf_file:
                    pdf_file.write(result.getvalue())

                # Returning the location of the saved PDF.

                return location, path.basename(dump_location)

        # Checking if the supplied parameter is an int.
        elif isinstance(param, int):

            # Getting the report from the database.
            report = models.Report.objects.get(pk=param)

            # Checking if the report exists.
            if report:

                # Returning the location.
                return report.location

            else:

                # Raising not found exception.
                raise Exception("Specified report does not exist.")

    @staticmethod
    def get_scanreport(param):

        """
        Generates a report about specified Scan Result.

        :param param: List of Scan Processes Result to be included in the report.

        :return: Location of the generated PDF document of the report.

        """

        # Checking if the parameter is a string.
        if isinstance(param, str):

            # Initializing an empty list.
            scanThrough = 0
            scanarray = []
            processes = None
            # print('param',param) # Converting raw (JSON) process list to list and iterating through it.
            for item in param.split(","):
                # Getting the scan data from database.
                a = models.ScanResult.objects.get(pk=item)
                # Getting the process data from database.
                processes = a.scan_information.process

                # Checking if the scan data exists:
                if a:
                    # Adding process to the list.
                    scanarray.append(a)
                    scanThrough = scanThrough + 1

            # Getting the current datetime.
            now = datetime.now().strftime("%Y:%m:%d - %H:%M:%S")
            # Getting the dump name.
            dump_location = processes.dump.upload.dump_location

            count = 0
            for i in scanarray:
                # print(i.detected)
                if i.detected == True:
                    count = count + 1

            # Rendering the output of report page.
            output = render_to_response('scanprocess.html', {
                "scandata": scanarray,
                "processes": processes,
                "date": now,
                "dump": path.basename(dump_location),
                "total_threat": count,
                "scanThrough": scanThrough,
            })

            # Specifying the directory where report will be stored;
            # that is, parent directory of dump location.
            location = "%s/reports" % path.dirname(dump_location)

            # Checking if the directory does not exist.
            if not path.exists(location):
                # Making the directory.
                makedirs(location)

            # Specifying the name of the PDF as current datetime.
            location = "%s/%s.pdf" % (location, datetime.now().strftime("%Y%m%d"))

            # Saving the PDF.
            result = StringIO()
            pisa.pisaDocument(StringIO(output.content), dest=result)

            with open(location, "wb") as pdf_file:
                pdf_file.write(result.getvalue())

            # Returning the location of the saved PDF.

            return location, processes.name, path.basename(dump_location)

        # Checking if the supplied parameter is an int.
        elif isinstance(param, int):
            # Raising not found exception.
            raise Exception("Specified report does not exist.")

    @staticmethod
    def get_regreport(param):
        """
               Generates a report about specified Registry Hives.

               :param param: List of Registry Hives to be included in the report.

               :return: Location of the generated PDF document of the report.

               """

        # Checking if the parameter is a string.
        if isinstance(param, str):

            # Initializing an empty list.
            dumpinfo = ""
            regarray = []
            count = 0
            # print('param',param) # Converting raw (JSON) process list to list and iterating through it.
            for item in param.split(","):
                # Getting the scan data from database.
                a = models.RegistryHive.objects.get(pk=item)
                # Getting the process data from database.
                dumpinfo = a.dump.upload.dump_location

                # Checking if the scan data exists:
                if a:
                    # Adding process to the list.
                    regarray.append(a)
                    count = count + 1

            # Getting the current datetime.
            now = datetime.now().strftime("%Y:%m:%d - %H:%M:%S")
            # Getting the dump name.
            dump_location = dumpinfo

            # Rendering the output of report page.
            output = render_to_response('regreport.html', {
                "regdata": regarray,
                "dumpinfo": dumpinfo,
                "date": now,
                "count": count,
                "dump": path.basename(dump_location),

            })

            # Specifying the directory where report will be stored;
            # that is, parent directory of dump location.
            location = "%s/reports" % path.dirname(dump_location)

            # Checking if the directory does not exist.
            if not path.exists(location):
                # Making the directory.
                makedirs(location)

            # Specifying the name of the PDF as current datetime.
            location = "%s/%s.pdf" % (location, datetime.now().strftime("%Y%m%d"))

            # Saving the PDF.
            result = StringIO()
            pisa.pisaDocument(StringIO(output.content), dest=result)

            with open(location, "wb") as pdf_file:
                pdf_file.write(result.getvalue())

            # Returning the location of the saved PDF.
            return location, path.basename(dump_location)

        # Checking if the supplied parameter is an int.
        elif isinstance(param, int):
            # Raising not found exception.
            raise Exception("Specified report does not exist.")

    @staticmethod
    def get_networkreport(param):
        """
               Generates a report about specified Network Connections.

               :param param: List of Network Connections to be included in the report.

               :return: Location of the generated PDF document of the report.

               """

        # Checking if the parameter is a string.
        if isinstance(param, str):

            # Initializing an empty list.
            dumpinfo = ""
            netarray = []
            count = 0
            process_name = []
            # print('param',param) # Converting raw (JSON) process list to list and iterating through it.
            for item in param.split(","):
                # Getting the scan data from database.
                a = models.NetworkConnection.objects.get(pk=item)

                # Getting the process data from database.
                dumpinfo = a.dump.upload.dump_location
                dumpid = a.dump.upload.id
                process = models.Process.objects.filter(dump=dumpid)

                # Checking if the scan data exists:
                if a:
                    # Adding process to the list.
                    netarray.append(a)
                    for i in process:
                        if i.pid == a.pid:
                            process_name.append(i)
                    count = count + 1

            # Getting the current datetime.
            now = datetime.now().strftime("%Y:%m:%d - %H:%M:%S")
            # Getting the dump name.
            dump_location = dumpinfo

            # Rendering the output of report page.
            output = render_to_response('netreport.html', {
                "netdata": netarray,
                "process": process_name,
                "dumpinfo": dumpinfo,
                "date": now,
                "count": count,
                "dump": path.basename(dump_location),
            })

            # Specifying the directory where report will be stored;
            # that is, parent directory of dump location.
            location = "%s/reports" % path.dirname(dump_location)

            # Checking if the directory does not exist.
            if not path.exists(location):
                # Making the directory.
                makedirs(location)

            # Specifying the name of the PDF as current datetime.
            location = "%s/%s.pdf" % (location, datetime.now().strftime("%Y%m%d"))

            # Saving the PDF.
            result = StringIO()
            pisa.pisaDocument(StringIO(output.content), dest=result)

            with open(location, "wb") as pdf_file:
                pdf_file.write(result.getvalue())

            # Returning the location of the saved PDF.
            return location, path.basename(dump_location)

        # Checking if the supplied parameter is an int.
        elif isinstance(param, int):

            # Raising not found exception.
            raise Exception("Specified report does not exist.")

    @staticmethod
    def get_uploadkreport(param):
        """
               Generates a report about specified Uploded Dumps.
    
               :param param: List of Network Connections to be included in the report.
    
               :return: Location of the generated PDF document of the report.
    
               """

        # Checking if the parameter is a string.
        if isinstance(param, str):

            # Initializing an empty list.
            uploadarray = []

            count = 0
            # print('param',param) # Converting raw (JSON) process list to list and iterating through it.
            for item in param.split(","):
                # Getting the scan data from database.
                upload = Upload.objects.get(pk=item)

                # check if dump object is available
                if upload:
                    uploadarray.append(upload)
                    count = count + 1

            # Getting the current datetime.
            now = datetime.now().strftime("%Y:%m:%d - %H:%M:%S")
            # Getting the dump name.
            dump_location = uploadarray[0].dump_location

            # Rendering the output of report page.
            output = render_to_response('uploadreport.html', {
                "uploaddata": uploadarray,
                "date": now,
                "count": count,
                "dump": path.basename(dump_location),
            })

            # Specifying the directory where report will be stored;
            # that is, parent directory of dump location.
            location = "%s/reports" % path.dirname(dump_location)

            # Checking if the directory does not exist.
            if not path.exists(location):
                # Making the directory.
                makedirs(location)

            # Specifying the name of the PDF as current datetime.
            location = "%s/%s.pdf" % (location, datetime.now().strftime("%Y%m%d"))

            # Saving the PDF.
            result = StringIO()
            pisa.pisaDocument(StringIO(output.content), dest=result)

            with open(location, "wb") as pdf_file:
                pdf_file.write(result.getvalue())

            # Returning the location of the saved PDF.
            return location

        # Checking if the supplied parameter is an int.
        elif isinstance(param, int):
            # Raising not found exception.
            raise Exception("Specified report does not exist.")

    @staticmethod
    def get_threadreport(param):
        """
               Generates a report about specified Threads.
    
               :param param: List of Threads to be included in the report.
    
               :return: Location of the generated PDF document of the report.
    
               """

        # Checking if the parameter is a string.
        if isinstance(param, str):

            # Initializing an empty list.
            threadarray = []

            count = 0
            # print('param',param) # Converting raw (JSON) process list to list and iterating through it.
            for item in param.split(","):
                # Getting the scan data from database.
                thread = models.Thread.objects.get(pk=item)

                dumpid = thread.process.dump.upload.id

                process = models.Process.objects.filter(dump=dumpid)
                for i in process:
                    if i.pid == thread.pid:
                        process_name = i.name

                # check if dump Thread is available
                if thread:
                    threadarray.append(thread)
                    count = count + 1

            # Getting the current datetime.
            now = datetime.now().strftime("%Y:%m:%d - %H:%M:%S")
            # Getting the dump name.
            dump_location = threadarray[0].process.dump.upload.dump_location
            # Rendering the output of report page.
            output = render_to_response('threadreport.html', {
                "threaddata": threadarray,
                "process": process_name,
                "date": now,
                "count": count,
                "dump": path.basename(dump_location),
            })

            # Specifying the directory where report will be stored;
            # that is, parent directory of dump location.
            location = "%s/reports" % path.dirname(dump_location)

            # Checking if the directory does not exist.
            if not path.exists(location):
                # Making the directory.
                makedirs(location)

            # Specifying the name of the PDF as current datetime.
            location = "%s/%s.pdf" % (location, datetime.now().strftime("%Y%m%d"))

            # Saving the PDF.
            result = StringIO()
            pisa.pisaDocument(StringIO(output.content), dest=result)

            with open(location, "wb") as pdf_file:
                pdf_file.write(result.getvalue())

            # Returning the location of the saved PDF.
            return location, path.basename(dump_location)

        # Checking if the supplied parameter is an int.
        elif isinstance(param, int):

            # Raising not found exception.
            raise Exception("Specified report does not exist.")

    @staticmethod
    def get_handlereport(param):
        """
               Generates a report about specified Handels.

               :param param: List of Handels to be included in the report.

               :return: Location of the generated PDF document of the report.

               """

        # Checking if the parameter is a string.
        if isinstance(param, str):

            # Initializing an empty list.
            handlearray = []
            process_name = None
            count = 0
            # print('param',param) # Converting raw (JSON) process list to list and iterating through it.
            for item in param.split(","):
                # Getting the scan data from database.
                handel = models.Handle.objects.get(pk=item)

                # check if dump Thread is available
                if handel:
                    handlearray.append(handel)
                    count = count + 1

            pid, dump_id = handlearray[0].pid, handlearray[0].dump
            process = models.Process.objects.get(dump=dump_id, pid=pid)
            process_name = process.name

            # Getting the current datetime.
            now = datetime.now().strftime("%Y:%m:%d - %H:%M:%S")
            # Getting the dump name.
            dump_location = handlearray[0].dump.upload.dump_location
            # Rendering the output of report page.
            output = render_to_response('handelreport.html', {
                "handeldata": handlearray,
                "process": process_name,
                "date": now,
                "count": count,
                "dump": path.basename(dump_location),
            })

            # Specifying the directory where report will be stored;
            # that is, parent directory of dump location.
            location = "%s/reports" % path.dirname(dump_location)

            # Checking if the directory does not exist.
            if not path.exists(location):
                # Making the directory.
                makedirs(location)

            # Specifying the name of the PDF as current datetime.
            location = "%s/%s.pdf" % (location, now)

            # Saving the PDF.
            result = StringIO()
            pisa.pisaDocument(StringIO(output.content), dest=result)

            with open(location, "wb") as pdf_file:
                pdf_file.write(result.getvalue())

            # Returning the location of the saved PDF.
            return location, process_name, path.basename(dump_location)

        # Checking if the supplied parameter is an int.
        elif isinstance(param, int):

            # Raising not found exception.
            raise Exception("Specified report does not exist.")

    @staticmethod
    def get_dlllereport(param):
        """
               Generates a report about specified Handels.

               :param param: List of Handels to be included in the report.

               :return: Location of the generated PDF document of the report.

               """

        # Checking if the parameter is a string.
        if isinstance(param, str):

            # Initializing an empty list.
            dllarray = []
            count = 0
            # print('param',param) # Converting raw (JSON) process list to list and iterating through it.
            for item in param.split(","):
                # Getting the scan data from database.
                dll = models.DLL.objects.get(pk=item)

                # check if dump Thread is available
                if dll:
                    dllarray.append(dll)
                    count = count + 1

            pid, dump_id = dllarray[0].pid, dllarray[0].dump
            process = models.Process.objects.get(dump=dump_id, pid=pid)
            process_name = process.name
            # Getting the current datetime.
            now = datetime.now().strftime("%Y:%m:%d - %H:%M:%S")
            # Getting the dump name.
            dump_location = dllarray[0].dump.upload.dump_location
            # Rendering the output of report page.
            output = render_to_response('dllreport.html', {
                "dlldata": dllarray,
                "process": process_name,
                "date": now,
                "count": count,
                "dump": path.basename(dump_location),
            })

            # Specifying the directory where report will be stored;
            # that is, parent directory of dump location.
            location = "%s/reports" % path.dirname(dump_location)

            # Checking if the directory does not exist.
            if not path.exists(location):
                # Making the directory.
                makedirs(location)

            # Specifying the name of the PDF as current datetime.
            location = "%s/%s.pdf" % (location, now)

            # Saving the PDF.
            result = StringIO()
            pisa.pisaDocument(StringIO(output.content), dest=result)

            with open(location, "wb") as pdf_file:
                pdf_file.write(result.getvalue())

            # Returning the location of the saved PDF.
            return location, process_name, path.basename(dump_location)

        # Checking if the supplied parameter is an int.
        elif isinstance(param, int):

            # Raising not found exception.
            raise Exception("Specified report does not exist.")
