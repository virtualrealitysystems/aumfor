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

from glob import glob
from os import path, makedirs, remove
from zipfile import is_zipfile, ZipFile


class Zip(object):
    """ Contains information and functionality related to Zip archives. """

    def __init__(self, zip_location):

        """
        Initializes a new instance of Zip class.

        :param zip_location: Location of a ZIP archive.

        """

        # Initializing an instance variable.
        self.zip_location = zip_location
        self.dump_location = None

    def extract(self):

        """ Extracts the specified ZIP archive. """

        try:

            # Specifying extraction location for ZIP contents.
            extraction_location = "%s/extracted/%s" % (
                path.dirname(self.zip_location),
                path.basename(self.zip_location)
            )

            # Checking the ZIP file does not exist.
            if not path.isfile(self.zip_location):
                raise Exception("'%s' does not exist." % self.zip_location)

            # Checking if specified file is not a ZIP file.
            if not is_zipfile(self.zip_location):
                raise Exception("The uploaded file is not a ZIP archive.")

            # Making the directories of extraction path if it does not exist.
            if not path.exists(extraction_location):
                makedirs(extraction_location)

            # Initializing the ZIP File object.
            with ZipFile(file=self.zip_location, mode="r", allowZip64=True) as zip_file:

                # Extracting the contents of the ZIP.
                zip_file.extractall(path=extraction_location)

            # Deleting the original file.
            remove(self.zip_location)

            # Getting the list of the extracted contents.
            files = glob("%s/*.*" % extraction_location)

            # Searching for files with .vmem and .img extensions; results in a list.
            images = [_file for _file in files if
                      _file.strip().lower().endswith(".vmem") or
                      _file.strip().lower().endswith(".img") or
                      _file.strip().lower().endswith(".bin") or
                      _file.strip().lower().endswith(".mddramimage")]

            # Checing if the list of images is empty.
            if len(images) == 0:
                raise Exception("The uploaded ZIP Archive does not contain any dumps.")

            # Setting the dump path.
            self.dump_location = images[0]

        # Raise any exceptions occurred during the above process.
        except Exception as e:
            raise Exception("Error while extracting ZIP Archive: " + str(e))

    @staticmethod
    def compress(source, destination):

        """
        Compresses specified source files and places the compressed archive at specified location.

        :param source: Source files to be compressed.
        :param destination: Destination of the archive.

        """

        # Initializing ZipFile object in write mode with compression as ZIP_DEFLATED.
        with ZipFile(destination, "w", 8) as zip_file:
            # Iterating through the list of zip files.
            for _file in source:
                # Writing the ZIP file.
                zip_file.write(_file)

                # Deleting the original file.
                remove(_file)
