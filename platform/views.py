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
from os import path, makedirs

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.views import APIView

from platform.common.zip import Zip
from platform.models import Upload as upload
from platform.windows.models import Dump


class Upload(APIView):
    """ Saves uploaded file on the server. """

    def post(self, request):

        try:

            # Getting the uploaded file data.
            uploaded_file = request.data.get("filDump")

            # Checking if a file was not uploaded.
            if not uploaded_file:
                raise Exception("No file was uploaded.")

            # Getting the User ID.
            user_id = request.data.get("user")

            # Checking if User ID was not specified.
            if not user_id:
                raise Exception("No User was specified.")

            # Getting User from database.
            user = User.objects.get(pk=user_id)

            # Checking if the user does not exist.
            if user is None:
                raise Exception("User does not exist.")

            # Getting name of the file.
            uploaded_file_name = uploaded_file.name

            # Specifying upload directory.
            upload_dir = "./media/%s" % user_id

            # Checking if the directory does not exist.
            if not path.exists(upload_dir):
                # Making the directory.
                makedirs(upload_dir)

            # Specifying the upload location.
            upload_location = "%s/%s-%s" % (
                upload_dir,
                datetime.now().strftime("%Y%m%d-%H%M%S"),
                uploaded_file_name
            )

            # Opening the destination file in write-binary mode.
            with open(upload_location, "wb") as filDump:

                # Dividing the file data in chunks and iterating through each chunk.
                for chunk in uploaded_file.chunks():
                    # Saving the chunk.
                    filDump.write(chunk)

            # Setting User's ID in the session.
            request.session["api_user"] = user_id

            self.checkStatus(user_id)  # delete the dump which is not analayzed completely
            # Returning the HTTP Response with success and location of uploaded file..
            return HttpResponse('{"success": 1, "location": "%s"}' % upload_location)

        except Exception as ex:

            # Returning the HTTP Response with error.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))

    # to flush data of any dump which is not anayzed completely before upload new
    @staticmethod
    def checkStatus(user_id):

        try:
            upload_all = upload.objects.filter(user_id=user_id)
            for i in upload_all:
                if i.status == "Analyzing":
                    del_id = i.pk
                    upload.objects.filter(pk=del_id).delete()
                    Dump.objects.filter(upload=del_id).delete()

        except Exception as ex:
            raise Exception(ex)


class Extract(APIView):
    """ Extracts the uploaded zip archive. """

    def post(self, request):

        try:

            # Getting the ZIP archive location from POST-ed data.
            zip_location = request.data.get("zip_location")

            # Checking if ZIP location is not specified.
            if not zip_location:
                raise Exception("No file was uploaded.")

            # Initializing a new object of Zip class wtih zip location and extracting it.
            zip_object = Zip(zip_location)
            zip_object.extract()

            # Returning the response.
            return HttpResponse('{"success":1, "status":"Extraction complete.", "data":%s}'
                                % '{"dump_location":"%s"}'
                                % zip_object.dump_location.replace("\\", "/"))

        except Exception as ex:

            # Returning any exception messages.
            return HttpResponse('{"success":0, "error":"%s"}' % str(ex))
