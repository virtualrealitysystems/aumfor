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

from django.core.validators import validate_comma_separated_integer_list
from django.db.models import *

from platform.models import Upload


class Dump(Model):
    profile = CharField(max_length=100)
    suggested_profiles = CharField(max_length=100, null=True)
    as_layer1 = TextField(null=True)
    as_layer2 = TextField(null=True)
    pae_type = CharField(max_length=100, null=True)
    dtb = CharField(max_length=100, null=True)
    kdbg = CharField(max_length=100, null=True)
    number_of_processors = IntegerField(null=True)
    service_pack = IntegerField(null=True)
    kuser_shared_data = CharField(max_length=100, null=True)
    image_date_and_time = DateTimeField(null=True)
    image_local_date_and_time = DateTimeField(null=True)
    start_time = CharField(null=True, max_length=100)
    end_time = CharField(null=True, max_length=100)
    upload = OneToOneField(Upload, on_delete=CASCADE, related_name='dump')


class RegistryHive(Model):
    virtual = CharField(max_length=100)
    physical = CharField(max_length=100)
    name = CharField(max_length=256)
    dump = ForeignKey(Dump, on_delete=CASCADE, related_name='registry_hives')


# class CommandHistory(Model):
#     process = IntegerField()
#     command_process = CharField(max_length=100)
#     command_history = CharField(max_length=100)
#     application = CharField(max_length=100)
#     flags = CharField(max_length=100)
#     command_count = IntegerField()
#     last_added = IntegerField()
#     last_displayed = IntegerField()
#     first_command = IntegerField()
#     command_count_max = IntegerField()
#     process_handle = CharField(max_length=100)
#     dump = ForeignKey(Dump, on_delete=CASCADE, related_name='commandhistory')


class NetworkConnection(Model):
    offset_v = CharField(max_length=100, null=True)
    pid = IntegerField(null=True)
    port = IntegerField(null=True)
    proto = IntegerField(null=True)
    protocol = CharField(max_length=10)
    address = CharField(max_length=15)
    create_time = DateTimeField()
    dump = ForeignKey(Dump, on_delete=CASCADE, related_name='networkconnections')


class Process(Model):
    pid = IntegerField()
    name = CharField(max_length=30, null=True)
    ppid = IntegerField()
    thread_count = IntegerField(null=True)
    handle_count = IntegerField(null=True)
    session = IntegerField(null=True)
    wow64 = NullBooleanField(null=True)
    creation_time = DateTimeField(null=True)
    termination_time = DateTimeField(null=True)
    offset_v = CharField(max_length=100, null=True)
    offset_p = CharField(max_length=100, null=True)
    pdb = CharField(max_length=100, null=True)
    dump = ForeignKey(Dump, on_delete=CASCADE)

    # def __unicode__(self):
    #     return '%s , %s' % (self.name, self.pid)


class Thread(Model):
    pid = IntegerField(null=True)
    tid = IntegerField(null=True)
    offset = CharField(max_length=100, null=True)
    tags = CharField(max_length=100, null=True)
    create_time = CharField(max_length=100, null=True)
    exit_time = CharField(max_length=100, null=True)
    owning_process = CharField(max_length=100, null=True)
    attached_process = CharField(max_length=100, null=True)
    state = CharField(max_length=100, null=True)
    state_reason = CharField(max_length=100, null=True)
    base_priority = CharField(max_length=100, null=True)
    priority = CharField(max_length=100, null=True)
    teb = CharField(max_length=100, null=True)
    start_address = CharField(max_length=100, null=True)
    owner_name = CharField(max_length=100, null=True)
    win32_start_address = CharField(max_length=100, null=True)
    win32_thread = CharField(max_length=100, null=True)
    cross_thread_flags = CharField(max_length=100, null=True)
    eip = CharField(max_length=100, null=True)
    eax = CharField(max_length=100, null=True)
    ebx = CharField(max_length=100, null=True)
    ecx = CharField(max_length=100, null=True)
    edx = CharField(max_length=100, null=True)
    esi = CharField(max_length=100, null=True)
    edi = CharField(max_length=100, null=True)
    esp = CharField(max_length=100, null=True)
    ebp = CharField(max_length=100, null=True)
    errcode = CharField(max_length=100, null=True)
    segcs = CharField(max_length=100, null=True)
    segss = CharField(max_length=100, null=True)
    segsd = CharField(max_length=100, null=True)
    seges = CharField(max_length=100, null=True)
    seggs = CharField(max_length=100, null=True)
    segfs = CharField(max_length=100, null=True)
    eflags = CharField(max_length=100, null=True)
    dr0 = CharField(max_length=100, null=True)
    dr1 = CharField(max_length=100, null=True)
    dr2 = CharField(max_length=100, null=True)
    dr3 = CharField(max_length=100, null=True)
    dr6 = CharField(max_length=100, null=True)
    dr7 = CharField(max_length=100, null=True)
    ssdt = CharField(max_length=100, null=True)
    entry_number = CharField(max_length=100, null=True)
    descriptor_service_table = CharField(max_length=100, null=True)
    hook_number = CharField(max_length=100, null=True)
    function_name = CharField(max_length=100, null=True)
    function_address = CharField(max_length=100, null=True)
    module_name = CharField(max_length=100, null=True)
    disassembly = TextField(null=True)
    dump = ForeignKey(Dump, on_delete=CASCADE, related_name='threads')
    # process = ForeignKey(Process, on_delete=CASCADE, related_name='threads')


class Handle(Model):
    offset_v = CharField(max_length=100, null=True)
    pid = IntegerField(null=True)
    handle = CharField(max_length=100, null=True)
    access = CharField(max_length=100, null=True)
    type = CharField(max_length=100, null=True)
    details = TextField(null=True)
    dump = ForeignKey(Dump, on_delete=CASCADE, related_name='handles')
    # process = ForeignKey(Process, on_delete=CASCADE, related_name='handles')


class DLL(Model):
    pid = IntegerField(null=True)
    base = CharField(max_length=100, null=True)
    size = CharField(max_length=100, null=True)
    load_count = CharField(max_length=100, null=True)
    path = TextField(null=True)
    dump = ForeignKey(Dump, on_delete=CASCADE, related_name='dlls')
    # process = ForeignKey(Process, on_delete=CASCADE, related_name='dlls')


class ScanInformation(Model):
    scan_id = CharField(null=True, max_length=500)
    scan_date = DateTimeField(null=True)
    response_code = IntegerField(null=True)
    resource = CharField(null=True, max_length=500)
    verbose_msg = CharField(null=True, max_length=500)
    md5 = CharField(null=True, max_length=32)
    sha1 = CharField(null=True, max_length=40)
    sha256 = CharField(null=True, max_length=64)
    permalink = CharField(null=True, max_length=500)
    positives = IntegerField(null=True)
    total = IntegerField(null=True)
    process = OneToOneField(Process, on_delete=CASCADE, related_name='scan_info')


class ScanResult(Model):
    anti_virus_name = CharField(null=True, max_length=100)
    detected = NullBooleanField(null=True)
    version = CharField(null=True, max_length=50)
    result = CharField(null=True, max_length=200)
    update = CharField(null=True, max_length=20)
    scan_information = ForeignKey(ScanInformation, on_delete=CASCADE, related_name="scan_results")


class Report(Model):
    location = CharField(null=True, max_length=100)
    report_type = CharField(null=True, max_length=50)
    date = DateTimeField(null=True)
    processes = TextField(validators=[validate_comma_separated_integer_list])
