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

from platform.common.utilities import Utilities
from platform.windows import models


class DLL(object):
    """ Contains information and functionality related to process DLLs. """

    def __init__(self, dump):

        """
        Initializes an instance of DLL object.

        :param dump: Dump from which DLL data will be obtained.
        :param process: Parent process of the DLL to be obtained.
        
        """

        # Initializing instance objects.
        self.dump = dump
        # self.process = process

    def save(self):

        """ Saves DLLs of the process to the database. """

        try:
            # Get the handles using "dlllist" command based on Process ID.
            raw_dll_data = Utilities.get_output(self.dump.location, "dlllist", self.dump.profile,
                                                self.dump.suggested_profiles)
            # If data was obtained...
            if raw_dll_data:
                # Iterating through the separated handle data.
                for parts in Utilities.separate_raw_data([raw_dll_data]):
                    # print (parts)
                    for line in parts:
                        # print (line)
                        if line and line[4] != "Error reading PEB for pid":
                            # Saving the data into the database.
                            models.DLL(**
                                       {
                                           "pid": line[0],
                                           "base": line[1],
                                           "size": line[2],
                                           "load_count": line[3],
                                           "path": line[4],
                                           "dump": self.dump.model

                                       }).save()

        # Ignoring any exceptions (for now).
        except Exception as ex:
            raise Exception(ex)
