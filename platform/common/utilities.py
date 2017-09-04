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


class Utilities(object):
    """ Contains common functionality used by all other applications in this project. """

    @staticmethod
    def get_output(dump_location, plugin, profile=None, suggested_profile=None, args=None):

        """
        Performs the specified command (plugin) on the specified dump.

        :param dump_location: Location of the dump to be analyzed.
        :param plugin: Command to be fired upon the dump file.
        :param profile: Profile of the dump.
        :param args: Additional command-line arguments.

        :return: Output of the command.

        """

        try:

            # Checking if no profile is specified.
            if profile is None:

                # Executing the command without any profile specified.
                command = ('python ./volatility/vol.py %s -f "%s"' % (plugin, dump_location))

            # Checking if a profile is specified...
            else:
                command = None
                # iterate throw all the suggested proflie
                if suggested_profile:

                    profile_list = []
                    for i_profile in suggested_profile.split(","):
                        if "(" in i_profile:
                            test = i_profile.split("(")
                            if test:
                                profile_list.append(test[0].strip())
                        else:
                            profile_list.append(i_profile.strip())

                    if profile_list:
                        print (profile_list)
                        for prof in profile_list:
                            # Exboomer-win2003-2006-03-17.imge cuting the command with any profile specified.
                            command = ('python ./volatility/vol.py %s -f "%s" --profile="%s" --output=greptext'
                                       % (plugin, dump_location, prof))

                            if args:
                                # Appending them to the command string.
                                command += " %s" % args

                            output = check_output(command, shell=True).split("\n")
                            # print(output)
                            if output[0] == "No suitable address space mapping found":
                                continue
                            else:
                                break

                    else:
                        command = ('python ./volatility/vol.py %s -f "%s" --profile="%s"'
                                   % (plugin, dump_location, profile))

            # Checking if additional arguments are specified...
            if args:
                # Appending them to the command string.
                command += " %s" % args

            # Firing the command and splitting by newlines.
            output = check_output(command, shell=True).split("\n")
            # print (output)
            # Checking if the first line is "No suitable address space mapping found".

            if output[0] == "No suitable address space mapping found":
                raise Exception("Could not analyze the dump. Either the profile, the dump or both are invalid.")

            # Returning the output.
            return output

        # In case of errors...
        except Exception as e:
            raise Exception("An error occurred while firing '%s' command on '%s' under '%s' profile : %s"
                            % (plugin, dump_location.split("/")[-1], profile, str(e)))

    @staticmethod
    def separate_raw_data(output_list):

        """
        Separates the output list into collection of lists.

        :param output_list: List of output to be separated.

        :return: Output separated into a list.

        """

        try:

            # Initialing an empty list.
            separated = []

            # Iterating each items of the output list.
            for lst in output_list:

                # Initialing an empty temp list.
                temp = []

                # Iterating each element in "lst" from the first index.
                for line in lst[1:]:

                    # Separating the data using pipe sign and stripping away any > signs.
                    # > usually means starting of a row.
                    parts = [None if part.strip() == "" else part.strip() for part in line.strip(">").split("|")]

                    # If "parts" is not empty.
                    if parts:
                        # Appending the parts in the temp list except the first element which is always None.
                        temp.append(parts[1:])

                # Append the temp list elements in separated list.
                separated.append(temp)

            # Returning the separated list.
            return separated

        # In case of any exceptions...
        except Exception as e:
            raise Exception("An error occurred while separating data: " + str(e))
