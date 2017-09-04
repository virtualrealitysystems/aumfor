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

from subprocess import check_output

from platform.windows import models


class Thread(object):
    """ Contains information and functionality related to process threads. """

    def __init__(self, dump):

        """
        Initializes an instance of Thread object.

        :param dump: Dump from which thread data will be obtained.
        :param process: Parent process of the thread to be obtained.
        """

        # Initializing instance objects.
        self.dump = dump

    def save(self):

        """ Saves threads of the process to the database. """

        try:

            command = ('python ./volatility/vol.py threads -f "%s"  --profile="%s" --output=greptext'
                       % (self.dump.location, self.dump.profile))

            # print(command)
            raw_thread_data = check_output(command, shell=True).split("\n")
            # print (raw_thread_data)

            error = "No suitable address space mapping found"

            if raw_thread_data[0] == error or raw_thread_data[1] == error:
                raise Exception("Could not analyze the dump. Either the profile, the dump or both are invalid.")
            else:
                self.greptext_op(raw_thread_data)
                # If there is some thread data...

        # Ignoring any exceptions (for now).
        except Exception as ex:
            self.parse_manual(ex)

    def separate_thread_data(self, data):

        """
        Separates supplied data in a specific format for thread fields.

        :param data: Data to be separated.
        :return: Separated data.

        """

        # Getting data for individual fields.
        parts = [(None if part.strip() == "" else part.strip()) for part in data[2:].strip(">").split("|")]

        # Creating a dictionary.
        return {
            "offset": parts[0],
            "pid": int(parts[1]),
            "tid": int(parts[2]),
            "tags": parts[3],
            "create_time": None if not parts[4] else " ".join(parts[4].split(" ")[0:2]),
            "exit_time": None if not parts[5] else " ".join(parts[5].split(" ")[0:2]),
            "owning_process": parts[6],
            "attached_process": parts[7],
            "state": parts[8],
            "state_reason": parts[9],
            "base_priority": parts[10],
            "priority": parts[11],
            "teb": parts[12],
            "start_address": parts[13],
            "owner_name": parts[14],
            "win32_start_address": parts[15],
            "win32_thread": parts[16],
            "cross_thread_flags": parts[17],
            "eip": parts[18],
            "eax": parts[19],
            "ebx": parts[20],
            "ecx": parts[21],
            "edx": parts[22],
            "esi": parts[23],
            "edi": parts[24],
            "esp": parts[25],
            "ebp": parts[26],
            "errcode": parts[27],
            "segcs": parts[28],
            "segss": parts[29],
            "segsd": parts[30],
            "seges": parts[31],
            "seggs": parts[32],
            "segfs": parts[33],
            "eflags": parts[34],
            "dr0": parts[35],
            "dr1": parts[36],
            "dr2": parts[37],
            "dr3": parts[38],
            "dr6": parts[39],
            "dr7": parts[40],
            "ssdt": parts[41],
            "entry_number": parts[42],
            "descriptor_service_table": parts[43],
            "hook_number": parts[44],
            "function_name": parts[45],
            "function_address": parts[46],
            "module_name": parts[47],
            "disassembly": parts[48]
        }

    def greptext_op(self, raw_thread_data):
        print ("grep text op")
        if raw_thread_data:

            # Initialing an empty object.
            sep = None

            # Appending > to the taw threads list.
            raw_thread_data.append(">")

            # IF the profile is Windows XP...
            if self.dump.profile.startswith("WinXP"):
                # Remove 3rd and 2nd elements.
                del raw_thread_data[2], raw_thread_data[1]

            # Removing the first element.
            del raw_thread_data[0]

            # Iterating through the raw data...
            for line in raw_thread_data:

                # If current line is and ending of thread description...
                if line.strip().startswith(">"):

                    # If sep is not empty, that means a thread
                    # data has been read partially.
                    if sep:
                        # Add the parent process to the thread data.
                        sep["dump"] = self.dump.model

                        # Save the thread to the dataabse.
                        models.Thread(**sep).save()

                        # Set the flag/thread variable to none.
                        sep = None

                    # If sep is not empty and it's not end of the raw thread data.
                    if not sep and line.strip(">") != "":
                        # Separating the thread data.
                        sep = self.separate_thread_data(line)

                # If current line is not empty...
                elif line.strip() != "":

                    # Add the thread disassembly data to the dictionary.
                    sep["disassembly"] += line

    def parse_manual(self, ex):
        print ("manual parse")
        try:
            # split the error message to confurm action
            error = ex.output.split("\n")
            if error[2] == "Finding appropriate address space for tables...":
                command = ('python ./volatility/vol.py threads -f "%s"  --profile="%s"'
                           % (self.dump.location, self.dump.profile))

                output = check_output(command, shell=True)
                output = output.split("------")
                #  parse the data into appropiate formate
                for i in range(len(output)):
                    thread_list = []
                    last_line_list = []
                    disassembly_str = "disassembly:"
                    if i != 0:
                        for item in (output[i].split("\n")):
                            if item:
                                if ":" in item:
                                    if "ETHREAD" in item:
                                        item1 = item.split(" ")
                                        list_i = "".join(map(str, item1[0:2]))
                                        if list_i:
                                            thread_list.append(list_i)
                                        list_i = "".join(map(str, item1[2:4]))
                                        if list_i:
                                            thread_list.append(list_i)

                                        list_i = "".join(map(str, item1[4:6]))
                                        if list_i:
                                            thread_list.append(list_i)
                                    else:
                                        if "CrossThreadFlags" in thread_list[-1]:
                                            if ":" in item:
                                                item_split = item.split(":")
                                                if "Eip" in item_split[0]:
                                                    thread_list.append(item)
                                                else:
                                                    disassembly_str = disassembly_str + str(item).strip(",")
                                        else:
                                            thread_list.append(item)
                                else:
                                    if "CrossThreadFlags" in thread_list[-1]:

                                        disassembly_str = disassembly_str + str(item).strip(",")

                                    else:

                                        thread_list[-1] = thread_list[-1] + ',' + item.strip()

                    if thread_list:
                        lstline = thread_list[-1]
                        # print (lstline)
                        if "Eip" in lstline:
                            # seprate the last line by , and make new list
                            newlist = lstline.split(",")
                            # get the value of eip
                            eip = str((newlist[0]))
                            last_line_list.append(eip)

                            # get row eax values list
                            eaxlist = ((newlist[1]).split(" "))
                            for b in range(len(eaxlist)):
                                last_line_list.append(str(eaxlist[b]).replace("=", ":"))

                            if (len(newlist)) >= 3:
                                esplsit = ((newlist[2]).split(" "))
                                for b in range(len(esplsit)):
                                    last_line_list.append(str(esplsit[b]).replace("=", ":"))

                            if (len(newlist)) >= 4:

                                cslist = ((newlist[3]).split(" "))
                                for b in range(len(cslist)):
                                    last_line_list.append(str(cslist[b]).replace("=", ':'))

                            if (len(newlist)) >= 5:

                                drlist = ((newlist[4]).split(" "))
                                for b in range(len(drlist)):
                                    last_line_list.append(str(drlist[b]).replace("=", ":"))

                            if (len(newlist)) >= 6:
                                # print (newlist)
                                disassembly_list = ((newlist[5:-1]))
                                temp_list = ["disassembly"]
                                dis_value = str(str(disassembly_list).replace(",", " ")[1:-1]).strip('"')
                                temp_list.append(dis_value)
                                temp_list = ":".join(temp_list)
                                # print (temp_list)
                                # append the value of disassembly field into last line fiels
                                last_line_list.append(temp_list)

                        if "CrossThreadFlags" in thread_list[-1]:
                            # print (disassembly_str)
                            # print (thread_list[-1])
                            thread_list.append(disassembly_str)
                            # print ("add disemb",thread_list)

                    if last_line_list:
                        del thread_list[-1]
                        for value in last_line_list:
                            thread_list.append(value)

                    # call save method to save thread data into model
                    self.save_non_greptext(thread_list)

        except Exception as error:
            print (error)
            return False

    def save_non_greptext(self, threadlist):
        """ this method save manual parsed normal screen data into database"""
        raw_data = threadlist
        if raw_data:
            raw_data_parts = [part for part in raw_data]

            #  list accroding to databse "key" postion
            dbkey_list = ["offset", "pid", "tid", "tags", "create_time", "exit_time",
                          "owning_process", "attached_process", "state", "base_priority",
                          "priority", "teb", "start_address", "win32_start_address", "descriptor_service_table",
                          "win32_thread", "cross_thread_flags",
                          "eip", "eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp", "errcode",
                          "segcs", "segss", "segsd", "seges", "seggs", "segfs", "eflags", "dr0", "dr1",
                          "dr2", "dr3", "dr6", "dr7", "disassembly"]

            #  list as per get normal data statical maintained
            manulaparse_key_list = ["ETHREAD", "Pid", "Tid", "Tags", "Created", "Exited",
                                    "Owning Process", "Attached Process", "State", "BasePriority",
                                    "Priority", "Teb", "StartAddress", "Win32StartAddress", "ServiceTable",
                                    "Win32Thread",
                                    "CrossThreadFlags",
                                    "Eip", "eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp", "err",
                                    "cs", "ss", "ds", "es", "gs", "fs", "efl", "dr0", "dr1",
                                    "dr2", "dr3", "dr6", "dr7", "disassembly"]

            #  maintain key and update
            data = {"dump": self.dump.model}
            for i in range(len(raw_data_parts)):

                # get key from raw data
                key = raw_data_parts[i].split(":")[0]
                value = None
                try:
                    #  check whther key is alredy in normal data key list
                    if key in manulaparse_key_list:
                        # if it is available get the index of it
                        keyofparse = manulaparse_key_list.index(key)
                        # as per index find the value from db key list
                        diskey = dbkey_list[keyofparse]
                        # if field is create and exit time parse the date
                        if i == 4 or i == 5:
                            date = (raw_data_parts[4].split(" "))
                            date = str(" ".join(date[1:]))
                            value = date
                            data.update({diskey: value})
                            # print (data)
                        else:
                            value = raw_data_parts[i].split(":")[1].strip(" ")
                            data.update({diskey: value})
                except Exception as error:
                    raise Exception(error)

            try:
                # save data in database
                models.Thread(**data).save()
            except Exception as save_err:
                raise Exception(save_err)
