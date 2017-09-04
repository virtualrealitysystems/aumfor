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

from datetime import datetime
from json import dumps

from platform.common.utilities import Utilities
from platform.windows import models


class Dump(object):
    """ Contains information and functionality related to memory dumps. """

    def __init__(self, upload=None):

        """
        Initializes an instance of Dump object.

        :param upload: The Upload object containing upload information.

        """

        # Checking if an upload object is supplied.
        if upload is not None:
            # Initializing instance objects.
            self.upload = upload
            self.location = upload.dump_location
            self.profile = None
            self.model = None
            self.suggested_profile = None

    def save(self):

        """ Saves dump information ot the database. """

        # Getting the basic image information using "imageinfo" command.
        output = Utilities.get_output(dump_location=self.location, plugin="imageinfo", args="--output=greptext")

        # Splitting the header row of the output to get a list.
        header_parts = [(None if part.strip() == "" else part.strip())
                        for part in output[0].strip(">").split("|")]

        # Splitting the content row of the output to get a list.
        parts = [(None if part.strip() == "" else part.strip())
                 for part in output[1].strip(">").split("|")][1:]

        # Checking if the image is not identified.
        if parts[0].startswith("No suggestion"):
            raise Exception("No profile found for this image.")

        # Iterating through the each element of both header and content lists.
        for i in range(len(parts) - 1, 0, -1):

            # Checking if the current header list element starts with "KPCR for CPU".
            if header_parts[i].startswith("KPCR for CPU"):
                # Remove the element on the i-th position from both header and content lists.
                header_parts.pop(i)
                parts.pop(i)

        # Getting the dump profile.
        self.profile = parts[0].split(",", 2)[0]
        self.suggested_profile = parts[0]

        # Setting the Dump model data.
        data = {
            "profile": self.profile,
            "suggested_profiles": parts[0],
            "as_layer1": parts[1],
            "as_layer2": parts[2],
            "pae_type": parts[3],
            "dtb": parts[4],
            "kdbg": parts[5],
            "number_of_processors": int(parts[6]),
            "service_pack": int(parts[7]),
            "kuser_shared_data": parts[8],
            "image_date_and_time": None if not parts[9] else " ".join(parts[9].split(" ")[0:2]),
            "image_local_date_and_time": None if not parts[10] else " ".join(parts[10].split(" ")[0:2]),
            "start_time": datetime.now().strftime("%H:%M:%S"),
            "end_time": "",
            "upload": self.upload.model
        }

        # Initializing Dump model object with obtained data.
        self.model = models.Dump(**data)

        # Saving the Dump information to the database.
        self.model.save()

    def serialize(self):

        """
        Serializes this object to JSON.

        :return: Serialized object as a dictionary.

        """

        # Converting the data to JSON and returning it.
        return dumps({
            "location": self.location,
            "profile": self.profile,
            "model": self.model.pk,
            "suggested_profile": self.suggested_profile
        })

    @staticmethod
    def deserialize(data):

        """
        Deserializes a specified dictionary into this class' object.

        :param data: Data to be deserialized.

        :return: Deserialized object

        """

        # Putting dictionary values to object.
        dump = Dump(None)
        dump.location = data["location"]
        dump.profile = data["profile"]
        dump.suggested_profiles = data["suggested_profile"]
        dump.model = models.Dump.objects.get(pk=data["model"])

        # Returning the dump object
        return dump

    def update_endtime(self):
        """ Updates the end time of memory analysis. """
        # Setting the date.
        item = models.Dump.objects.get(pk=self.model.pk)
        item.end_time = datetime.now().strftime("%H:%M:%S")
        item.save()
