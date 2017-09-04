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

from django.contrib.auth.models import User

from platform import models


class Upload(object):
    """ Contains information and functionality related to uploads. """

    def __init__(self, user, dump_location, platform=None):
        """
        Initializes a new object of Upload class.

        :param user: The uploader.
        :param dump_location: Physical location of the memory dump.

        """

        # Initializing instance variables.
        self.user = user
        self.dump_location = dump_location
        self.platform = platform
        self.model = None

    def save(self):
        """ Saves upload information to the database. """

        # Initializing a new object of Upload model.
        self.model = models.Upload(**{
            "user": self.user,
            "dump_location": self.dump_location,
            "status": "Analyzing",
            "platform": self.platform,
            "uploaded_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # Saving the data to database.
        self.model.save()

    def update_status(self):
        """ Updates the status of memory image. """

        # Setting the status.
        self.model.status = "Analyzed"

        # Updating the database.
        self.model.save()

    def serialize(self):
        """
        Serializes this object to JSON.

        :return: Serialized object as a dictionary.

        """

        # Converting the data to JSON.
        return dumps({
            "user": self.user.pk,
            "dump_location": self.dump_location,
            "model": self.model.pk
        })

    @staticmethod
    def deserialize(data):
        """
        Deserializes specified dictionary into object.

        :param data: Data to be deserialized.

        :return: Deserialized object.

        """

        # Getting objects from data.
        user = User.objects.get(pk=data["user"])
        dump_location = data["dump_location"]

        # Returning a new instance of Upload class.
        upload = Upload(user, dump_location)
        upload.model = models.Upload.objects.get(pk=data["model"])

        return upload
