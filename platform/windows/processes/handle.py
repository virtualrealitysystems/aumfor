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


class Handle(object):
    """ Contains information and functionality related to process handles. """

    def __init__(self, dump):

        """
        Initializes an instance of Handle object.

        :param dump: Dump from which handles data will be obtained.
        :param process: Parent process of the handle to be obtained.
        """

        # Initializing instance objects.
        self.dump = dump
        # self.process = process

    def save(self):

        """ Saves process handles in the database. """

        try:

            # Get the handles using "handles" command based on Process ID.
            raw_handle_data = Utilities.get_output(self.dump.location, "handles", self.dump.profile,
                                                   self.dump.suggested_profiles)
            # If data was obtained...
            if raw_handle_data:
                # Iterating through the separated handle data.
                for parts in Utilities.separate_raw_data([raw_handle_data]):
                    # Iterating through each line of the list.
                    for line in parts:
                        # If the line is not empty...
                        if line:
                            # print (line)
                            # Saving the data into the database.
                            models.Handle(**
                                          {
                                              "offset_v": line[0],
                                              "pid": line[1],
                                              "handle": line[2],
                                              "access": line[3],
                                              "type": line[4],
                                              "details": None if len(line) == 5 else line[5],
                                              "dump": self.dump.model,
                                          }).save()

        # Ignoring any exceptions (for now).
        except Exception as ex:
            raise Exception(ex)
