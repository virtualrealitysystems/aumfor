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

import urllib
import urllib2
from re import match

from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.views import APIView

from aumfor import settings
from platform.models import RegFlag


class Register(APIView):
    """ Registers a user of the web application. """

    def register_local(self, data):

        my_data = [
            ("name", data["name"]),
            ("company", data["company"]),
            ("username", data["username"]),
            ("email", data["email"])
        ]

        my_data = urllib.urlencode(my_data)

        req = urllib2.Request("http://virtualrealitysystems.net/webility/api/register.php", my_data)
        req.add_header("Content-type", "application/x-www-form-urlencoded")
        try:
            urllib2.urlopen(req).read()
        except Exception as ex:
            print (ex)

    def post(self, request):

        try:

            # Getting data.
            username = request.data.get("username")
            email = request.data.get("email")
            password = request.data.get("password")

            # Checking if any of the data is None.
            if not username:
                raise Exception("Username not specified.")

            if not email:
                raise Exception("Email not specified.")

            if not password:
                raise Exception("Password not specified.")

            # Validating email address.
            if not match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
                raise Exception("Email address is invalid.")

            if settings.LOCAL:

                name = request.data.get("name")
                company = request.data.get("company")

                if not name:
                    raise Exception("Name not specified.")

                if not company:
                    raise Exception("Company was not specified.")

                data = {
                    "name": name,
                    "company": company,
                    "username": username,
                    "email": email
                }

                self.register_local(data)

            # Checking if the user with same username exists.
            if User.objects.filter(username=username).exists():
                raise Exception("Username already taken!")

            # Checking if the user with same email exists.
            if User.objects.filter(email=email).exists():
                raise Exception("This email address is already registered!")

            # Creating the User's entry in the database.
            try:
                urllib2.urlopen('https://www.google.co.in/', timeout=1)
                User.objects.create_user(username=username, email=email, password=password).save()
                user = User.objects.get(username=username)

                RegFlag(user=user, flag="1", name=name, company=company).save()

            except Exception as err:

                User.objects.create_user(username=username, email=email, password=password).save()
                user = User.objects.get(username=username)
                RegFlag(user=user, flag="0", name=name, company=company).save()
                pass

            # Returning the response indicating success.
            return HttpResponse('{"success":"1"}')

        except Exception as ex:
            # Returning the response indicating failure with reason.
            return HttpResponse('{"success":"0", "error":"%s"}' % str(ex))

        except urllib2.URLError as err:
            pass


class Login(APIView):
    """ Logs in a user of the web application. """

    def post(self, request):

        try:

            # Getting Username and Password from POST-ed data.
            username = request.data.get("username")
            password = request.data.get("password")

            # Checking if any of the data is None.
            if not username:
                raise Exception("Username not specified.")

            if not password:
                raise Exception("Password not specified.")

            # Authenticating the user.
            user = auth.authenticate(username=username, password=password)

            # Checking if the User object does not exist.
            if user is None:
                raise Exception("Invalid Username or Password.")

            # Checking if the User is not active.
            if not user.is_active:
                raise Exception("This account has been disabled.")

            # Adding the user object to session.
            auth.login(request, user)

            # Returning the response indicating success.
            return HttpResponse('{"success":"1"}')

        except Exception as ex:

            # Returning the response indicating failure with reason.
            return HttpResponse('{"success":"0", "error":"%s"}' % str(ex))
