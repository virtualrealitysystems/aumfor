function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function get_data_Dt(thread_pid,thread_dumpid) {

     $.ajax({
        type: "GET",
        // contentType: "application/json; charset=utf-8",
        url: "/platform/windows/json/processes/?dump=" + thread_dumpid + "&pid=" + thread_pid + "",
        "headers": {
            "X-CSRFToken": getCookie('csrftoken')
        },
        // dataType: "json",
        success: function(process) {
            // console.log(process[0].dump.id)
            document.getElementById("process").innerText = process[0].name
            document.getElementById("setPid").value = process[0].pid;
            document.getElementById("setDumpid").value = process[0].dump.id;
            
            var res = process[0].dump.upload.dump_location.split("/")[4];
            res = res.split("-")[2];
            console.log(res);
            document.getElementById("dumpName").value = res;

        }
    });
     

    $("#analyzedprocess").addClass("active");
    $("#ddmenu1").removeClass("active");
    $("#bredcum").append('<li><a href="/process/">Analyzed Processes </a></li>');
    $("#bredcum").append('<li>Thread</li>');

    var dt = $('#example').DataTable({
        "drawCallback": function(settings) {
            document.getElementById("rowsCount").innerText = settings.aoData.length;
        },
        "processing": true,
        // "retrieve": true,
        "destroy": true,
        "language": {
            "emptyTable": "There is no Data available.",
            "loadingRecords": "Loading...",
            "processing": "Processing...",
            "search": "Search:",
            "zeroRecords": "No matching records found",
        },
        "scrollX": true,
        "scrollY": "400px",
        "ajax": {

            "type": "GET",
            "url": "/platform/windows/json/threads/?pid="+thread_pid+"&dump="+thread_dumpid+"",
            "dataSrc": "",
            // complete : function(data){alert(JSON.stringify(data))},
            //error: function(data) { alert(JSON.stringify(data)) },
        },
        "columns": [{
            "data": "id",
            "visible": false,
        }, {
            "data": "pid",
            
        }, {
            "data": "tid"
        }, {
            "data": "offset"
        }, {
            "data": "tags"
        }, {
            "data": "create_time"
        }, {
            "data": "exit_time"
        }, {
            "data": "owning_process"
        }, {
            "data": "attached_process"
        }, {
            "data": "state"
        }, {
            "data": "state_reason"
        }, {
            "data": "base_priority"
        }, {
            "data": "priority"
        }, {
            "data": "teb"
        }, {
            "data": "start_address"
        }, {
            "data": "owner_name"
        }, {
            "data": "win32_start_address"
        }, {
            "data": "win32_thread"
        }, {
            "data": "cross_thread_flags"
        }, {
            "data": "eip"
        }, {
            "data": "eax"
        }, {
            "data": "ebx"
        }, {
            "data": "ecx"
        }, {
            "data": "edx"
        }, {
            "data": "esi"
        }, {
            "data": "edi"
        }, {
            "data": "esp"
        }, {
            "data": "ebp"
        }, {
            "data": "errcode"
        }, {
            "data": "segcs"
        }, {
            "data": "segss"
        }, {
            "data": "segsd"
        }, {
            "data": "seges"
        }, {
            "data": "seggs"
        }, {
            "data": "segfs"
        }, {
            "data": "eflags"
        }, {
            "data": "dr0"
        }, {
            "data": "dr1"
        }, {
            "data": "dr2"
        }, {
            "data": "dr3"
        }, {
            "data": "dr6"
        }, {
            "data": "dr7"
        }, {
            "data": "ssdt"
        }, {
            "data": "entry_number"
        }, {
            "data": "descriptor_service_table",
            "render": function(data, type, row, meta) {
                var id = "showLess_" + row["id"];
                var id2 = "showMore_" + row["id"];
                if (data != null)
                {
                    var a = '<div style="display:block" id=' + id + '> ' + data.substr(0, 20) + ' <br /><button class="btn btn-info" onclick="showmore(' + id + ',' + id2 + ')">Show More</button></div>' + '<div style="display:none" id=' + id2 + '>' + data + ' <br> <a href="#" class="btn btn-info" onclick="showless(' + id + ',' + id2 + ')">Show Less</a></div> ';
                    return a;
                }
                else
                {
                    return data;
                }
                
            }
        }, {
            "data": "hook_number"
        }, {
            "data": "function_name"
        }, {
            "data": "function_address"
        }, {
            "data": "module_name"
        }, {
            "data": "disassembly",
            "render": function(data, type, row, meta) {
                var id = "showLess" + row["id"];
                var id2 = "showMore" + row["id"];
                if (data != null)
                {
                    var a = '<div style="display:block" id=' + id + '> ' + data.substr(0, 20) + ' <br /><button class="btn btn-info" onclick="showmore(' + id + ',' + id2 + ')">Show More</button></div>' + '<div style="display:none" id=' + id2 + '>' + data + ' <br> <a href="#" class="btn btn-info" onclick="showless(' + id + ',' + id2 + ')">Show Less</a></div> ';
                    return a;
                }
                else
                {
                    return data;
                }
            }
        }, ]
    });

}

function showmore(e, e2) {
    e.style.display = "none";
    e2.style.display = "block";
}

function showless(e, e2) {
    e.style.display = "block";
    e2.style.display = "none";
}

function goto_process_detail(e, f) {
    $('#form').submit();
}
