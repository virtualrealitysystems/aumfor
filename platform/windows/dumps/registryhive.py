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


class RegistryHive(object):

    """ Contains information and functionality related to Registry Hives. """

    def __init__(self, dump):

        """
        Initializes an instance of RegistryHive object.

        :param dump: Dump from which Registry Hives will be retrieved.

        """

        # Initializing instance objects.
        self.dump = dump

    def save(self):

        """ Extracts Registry Hives from the specified dump and saves it to database. """

        try:

            # Getting the handles using "hivelist" command based on Process ID.
            raw_hive_data = Utilities.get_output(self.dump.location, "hivelist", self.dump.profile,self.dump.suggested_profiles,
                                                 " --output=greptext")

            # Checking if data was obtained.
            if raw_hive_data:

                # Iterating through the separated hive data.
                for parts in Utilities.separate_raw_data([raw_hive_data]):

                    # Iterating through each part.
                    for line in parts:

                        # Checking if line is not empty or None.
                        if line:

                            # Saving the data into the database.
                            models.RegistryHive(**{
                                "virtual": line[0],
                                "physical": line[1],
                                "name": line[2],
                                "dump": self.dump.model
                            }).save()

        # Ignoring any exceptions (for now).
        except:
            pass
