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

import urllib2
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

from api.views import Register
from platform.models import RegFlag

holddata = None


def index(request):
    offline_register(request)

    if request.user.is_authenticated():
        request.session['username'] = request.user.username
        request.session['uid'] = request.user.pk
    else:
        request.session['uid'] = -1

    print(">>>>>>>", request.session.get('newdump'));
    # if request.session.get('newdump'):
    #      dumpid = request.session.get('newdump')
    #  return render(request,'index.html',context={"dump":dumpid})
    return render_to_response("index.html", locals(), context_instance=RequestContext(request))
    # contex = {
    #     "request":RequestContext(request),
    #     "dump":dumpid
    # }
    # return render(request,'index.html',contex)


def thread(request):
    if request.POST.get("t_pid") and request.POST.get("t_dump_id"):
        contex = {
            "pid": request.POST.get("t_pid"),
            "dumpid": request.POST.get("t_dump_id")
        }
        return render(request, "thread.html", contex)
    else:
        return render(request, "thread.html", {"msg": "no pid or dump id set"})


def handles(request):
    if request.POST.get("h_pid") and request.POST.get("h_dump_id"):
        contex = {
            "pid": request.POST.get("h_pid"),
            "dumpid": request.POST.get("h_dump_id")
        }

        return render(request, "handles.html", contex)
    else:
        return render(request, "handles.html", {"msg": "no pid or dump id set"})


def dll(request):
    if request.POST.get("d_pid") and request.POST.get("d_dump_id"):
        contex = {
            "pid": request.POST.get("d_pid"),
            "dumpid": request.POST.get("d_dump_id")
        }
        return render(request, "dll.html", contex)
    else:
        return render(request, "dll.html", {"msg": "no pid or dump id set"})


def network_connections(request):
    return render(request, "networkconnection.html", {})


def registry_hives(request):
    return render(request, "registryhives.html", {})


def login(request):
    return render(request, "login.html", {})


def logout(request):
    auth.logout(request)
    return render(request, "login.html", {})


def register(request):
    return render_to_response("register.html", {}, context_instance=RequestContext(request))


def process_data(request):
    return render_to_response("processdetail.html", {}, context_instance=RequestContext(request))


def process_detail(request):
    context = {}
    try:
        if request.POST.get("setPid") and request.POST.get("setDumpid"):

            context = {
                "pid": request.POST.get("setPid"),
                "dumpid": request.POST.get("setDumpid"),
                "dumpname": request.POST.get("dumpName")
            }
        else:
            raise Exception("No Process Id or Dump Id Specified")

    except Exception as ex:
        raise Exception(ex)
    return render_to_response("singleprocess.html", context, context_instance=RequestContext(request))


def uploades(request):
    return render(request, "uploades.html", {})


@csrf_exempt
def scanResult(request):
    if request.POST.get("scanid"):
        contex = {
            "scanid": request.POST.get("scanid"),
            "pk": request.POST.get("setPk"),
            "dump": request.POST.get("setdumpname")
        }
    else:
        contex = {}
    return render(request, "scandetails.html", contex)


def scanReport(request):
    return render(request, "scanReport.html", {})


def imageInfo(request):
    if request.POST.get("uploadid") and request.POST.get("uploadname"):
        contex = {
            "uploadid": request.POST.get("uploadid"),
            "uploadname": request.POST.get("uploadname")
        }
    else:
        contex = {"uploadid": 0}
    return render(request, "imgInfo.html", contex)


def team(request):
    return render(request, "team.html", {})


def help(request):
    return render(request, "help.html", {})


def offline_register(request):
    try:
        urllib2.urlopen('http://virtualrealitysystems.net/webility/api/register.php', timeout=1)

        obj = Register()
        flag = RegFlag.objects.get(user_id=request.user.pk)
        if flag.flag == 0:
            info = User.objects.get(id=request.user.pk)
            data = {
                "name": flag.name,
                "company": flag.company,
                "username": info.username,
                "email": info.email
            }

            obj.register_local(data)
            flag.flag = 1
            flag.save()

        else:
            pass

    except urllib2.URLError as err:
        print (err)

    except Exception as ex:
        print (ex)


def contactus(request):
    return render(request, "contactus.html", {})


def email(request):
    try:
        if request.POST.get("firstname") or request.POST.get("lastname") or request.POST.get("email"):

            name = str(request.POST.get("firstname") + ' ' + request.POST.get("lastname"))
            from_email = str(request.POST.get("email"))
            subject = str('Aumfor New' + ' ' + str(request.POST.get("subject")))

            # body = 'message from ' + name + "\n\n" + "\t\t" + str(request.POST.get("msg"))
            msg = str(request.POST.get("msg"))

            body = '''
				Hello Admin, <br>
				you have received new <b>%s</b> From AUMFOR and here is the detials ,<br>
				<b>From</b>    : %s <br>
				<b>Email</b>   : %s <br>
				<b>Subject</b> : %s <br>
				<b>Message</b> : <br>
				<span style="margin-left:5em;"><span> % s''' % (
            str(request.POST.get("subject")), name, from_email, subject, msg)

            email = EmailMessage(str(subject), str(body), str(from_email), to=['info@virtualrealitysystems.net'])

            for file in request.FILES.getlist("pic"):
                email.attach(filename=file.name, content=file.read(), mimetype=file.content_type)
            email.content_subtype = "html"
            email.send()
            return render_to_response('contactus.html', {"msg": "Your Response Submitted Successfully"},
                                      context_instance=RequestContext(request))
        else:
            return render_to_response('contactus.html', {"msg": "Values are not set"},
                                      context_instance=RequestContext(request))


    except Exception as ex:
        print(ex)
        return render_to_response('contactus.html', {"msg": ex}, context_instance=RequestContext(request))


# --------------------------- 404 Page Error ---------------------- #

def handler404(request):
    responce = render_to_response('404.html', context_instance=RequestContext(request))
    responce.status_code = 404
    return responce
    # return render(request,"404.html",{})


def handler500(request):
    responce = render_to_response('500.html', context_instance=RequestContext(request))
    responce.status_code = 500
    return responce
