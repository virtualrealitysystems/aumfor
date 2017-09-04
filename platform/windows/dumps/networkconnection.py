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


class NetworkConnection(object):
    """ Contains information and functionality related to Network Connections. """

    def __init__(self, dump):

        """
        Initializes an instance of Dump object.

        :param dump: Dump from which Network data will be obtained.

        """

        # Initializing instance objects.
        self.dump = dump

    def save(self):

        """ Saves the NetworkConnection object to the database. """

        try:

            # Getting the network connections using "sockets" command based on Process ID.
            raw_network_data = Utilities.get_output(self.dump.location, "sockets", self.dump.profile,
                                                    self.dump.suggested_profiles,
                                                    " --output=greptext")

            print (raw_network_data)
            # Checking if data was obtained...
            if raw_network_data:

                # Iterating through the separated handle data.
                for parts in Utilities.separate_raw_data([raw_network_data]):

                    # Iterating through each element of the line.
                    for line in parts:

                        # Checking if line is not None
                        if line:
                            # Creating dictionary for NetworkConnection model.
                            data = {
                                "offset_v": line[0],
                                "pid": line[1],
                                "port": line[2],
                                "proto": line[3],
                                "protocol": line[4],
                                "address": line[5],
                                "create_time": " ".join(line[6].split(" ")[0:2]),
                                "dump": self.dump.model
                            }

                            # Saving the data into the database.
                            models.NetworkConnection(**data).save()

        # Ignoring any exceptions (for now).
        except:
            pass
