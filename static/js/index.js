function upload_image(request_uid) {
    var bar = $('#bar');
    var percent = $('#percent');

    $('#fileUpload').ajaxForm({
        beforeSubmit: function() {
            document.getElementById('progress_div').style.display = 'block';
            var percentVal = '0%';
            bar.width(percentVal);
            percent.html(percentVal);
            document.getElementById('status').style.display = 'block';
            document.getElementById('statusUpload').innerText = 'Uploading Dump ... ';
            document.getElementById('modelBlock').style.display = 'block';
        },
        uploadProgress: function(event, position, total, percentComplete) {
            // var percentVal = percentComplete + '%';
            var percentVal = '10%';
            bar.width(percentVal);
            percent.html(percentVal);
        },
        success: function() {
            var percentVal = '15%';
            bar.width(percentVal);
            percent.html(percentVal);
            document.getElementById('statusUpload').innerHTML = 'Uploading Dump... <i class="material-icons">check</i>';
        },
        complete: function() {
            console.log('complete');

            // var request_uid = {{ request.session.uid }};
            //console.log("request_uid", request_uid, "bar", bar, "percent", percent)
            apiCall(request_uid, bar, percent);
            $('#fileUpload').submit(function(e) {
                e.preventDefault();
            });

        },
        error: function(jqXHR, exception) {
            console.log(jqXHR);
            console.log(exception);
            sweetAlert("Oops...", jqXHR, "error");
            location.reload(true);
            // getErrorMessage(jqXHR, exception);
        },
    });
} // ------------------------- this function call all api one by one based on each other sucess responce and perform all task

function apiCall(request_uid, bar, percent) {
    function getCookie(cname) {
        var name = cname + '=';
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
        return '';
    }
    var dumpdata;
    var formData = new FormData();
    formData.append('filDump', $('#fileDump')[0].files[0]);
    formData.append('user', request_uid);
    $.ajax({
        url: '/platform/upload/',
        type: 'POST',
        cache: false,
        contentType: false,
        processData: false,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        data: formData,
        success: function(data) {
            var percentVal = '20%';
            bar.width(percentVal);
            percent.html(percentVal);
            document.getElementById('status').style.display = 'block';
            var data = jQuery.parseJSON(data);
            if (data['success'] == '1') {
                document.getElementById('statusExtract').innerText = 'Extracting Dump...';
                $.post('/platform/extract/', {
                    zip_location: data['location'],
                    csrfmiddlewaretoken: getCookie('csrftoken'),
                }, function(json) {
                    var data = jQuery.parseJSON(json);
                    if (data['success'] == '1') {
                        var percentVal = '25%';
                        bar.width(percentVal);
                        percent.html(percentVal);
                        document.getElementById('statusExtract').innerHTML = 'Extracting Dump... <i class="material-icons">check</i>';
                        document.getElementById('statusAnalyzeDump').innerText = 'Analyzing Dump ...';
                        $.post('/platform/windows/analyze/info/', {
                            data: JSON.stringify(data['data']),
                            platform: 'Windows',
                            csrfmiddlewaretoken: getCookie('csrftoken'),
                        }, function(json) {
                            // console.log(json);
                            var data = jQuery.parseJSON(json);
                            dataInfo = JSON.stringify(data['data']);
                            dumpdata = JSON.stringify(data['data']);
                            if (data['success'] == '1') {
                                var percentVal = '36%';
                                bar.width(percentVal);
                                percent.html(percentVal);
                                document.getElementById('statusAnalyzeDump').innerHTML = 'Analyzing Dump...<i class="material-icons">check</i>';
                                document.getElementById('statusAnalyzeProcess').innerText = 'Analyzing Process ...';
                                $.post('/platform/windows/analyze/processes/', {
                                    data: JSON.stringify(data['data']),
                                    csrfmiddlewaretoken: getCookie('csrftoken'),
                                }, function(json) {
                                    var data = jQuery.parseJSON(json);
                                    if (data['success'] == '1') {
                                        var percentVal = '47%';
                                        bar.width(percentVal);
                                        percent.html(percentVal);
                                        document.getElementById('statusAnalyzeProcess').innerHTML = 'Analyzing Process ... <i class="material-icons">check</i>';
                                        document.getElementById('statusAnalyzeThread').innerText = 'Analyzing Threads ... ';
                                        $.post('/platform/windows/analyze/threads/ ', {
                                            data: dumpdata,
                                            csrfmiddlewaretoken: getCookie('csrftoken'),
                                        }, function(json) {
                                            var data = jQuery.parseJSON(json);
                                            if (data['success'] == '1') {
                                                var percentVal = '58%';
                                                bar.width(percentVal);
                                                percent.html(percentVal);
                                                document.getElementById('statusAnalyzeThread').innerHTML = 'Analyzing Threads ... <i class="material-icons">check</i>';
                                                document.getElementById('statusAnalyzeDll').innerText = 'Analyzing Dll ... ';
                                                $.post('/platform/windows/analyze/dll/ ', {
                                                    data: dumpdata,
                                                    csrfmiddlewaretoken: getCookie('csrftoken'),
                                                }, function(json) {
                                                    var data = jQuery.parseJSON(json);
                                                    if (data['success'] == '1') {
                                                        var percentVal = '60%';
                                                        bar.width(percentVal);
                                                        percent.html(percentVal);
                                                        document.getElementById('statusAnalyzeDll').innerHTML = 'Analyzing Dll ... <i class="material-icons">check</i>';
                                                        document.getElementById('statusAnalyzeHandle').innerText = 'Analyzing Handles ... ';
                                                        $.post('/platform/windows/analyze/handles/', {
                                                            data: dumpdata,
                                                            csrfmiddlewaretoken: getCookie('csrftoken'),
                                                        }, function(json) {
                                                            var data = jQuery.parseJSON(json);
                                                            if (data['success'] == '1') {
                                                                var percentVal = '81%';
                                                                bar.width(percentVal);
                                                                percent.html(percentVal);
                                                                document.getElementById('statusAnalyzeHandle').innerHTML = 'Analyzing Handles ... <i class="material-icons">check</i>';
                                                                document.getElementById('statusAnalyzeRegisteryHives').innerText = 'Analyzing RegisteryHives ... ';
                                                                $.post('/platform/windows/analyze/registry-hives/ ', {
                                                                    data: dumpdata,
                                                                    csrfmiddlewaretoken: getCookie('csrftoken'),
                                                                }, function(json) {
                                                                    var data = jQuery.parseJSON(json);
                                                                    if (data['success'] == '1') {
                                                                        var percentVal = '91%';
                                                                        bar.width(percentVal);
                                                                        percent.html(percentVal);
                                                                        document.getElementById('statusAnalyzeRegisteryHives').innerHTML = 'Analyzing RegisteryHives ... <i class="material-icons">check</i>';
                                                                        document.getElementById('statusAnalyzeNetwork').innerText = 'Analyzing Network Connections';
                                                                        $.post('/platform/windows/analyze/network-connections/ ', {
                                                                            data: dumpdata,
                                                                            csrfmiddlewaretoken: getCookie('csrftoken'),
                                                                        }, function(json) {
                                                                            var data = jQuery.parseJSON(json);
                                                                            if (data['success'] == '1') {
                                                                                var percentVal = '100%';
                                                                                bar.width(percentVal);
                                                                                percent.html(percentVal);
                                                                                document.getElementById('statusAnalyzeNetwork').innerText = 'All Process Done Data will be Shown soon in bellow Table';
                                                                                document.getElementById('NewDumpid').value = data['dump'];
                                                                                var NewDumpid = data['dump'];
                                                                                summary(dumpdata, NewDumpid); // call this function to show summary of analyzed data;

                                                                                document.getElementById('progress_div').style.display = "none";
                                                                                // document.getElementById('fileUpload').reset();
                                                                                $('#fileUpload').clearForm();
                                                                                // code for clear the progress bar and file upload
                                                                                // location.reload(true);
                                                                            } else {
                                                                                swal({
                                                                                    title: 'Oops',
                                                                                    text: data['error'],
                                                                                    type: "error",
                                                                                    confirmButtonColor: "#f0ad4e",
                                                                                    confirmButtonText: "Try Again!",
                                                                                    closeOnConfirm: false,
                                                                                }, function() {

                                                                                    // swal("Deleted!", "Your imaginary file has been deleted.", "success");
                                                                                    location.reload(true)

                                                                                });
                                                                            }
                                                                        });
                                                                    } else {

                                                                        swal({
                                                                            title: 'Oops',
                                                                            text: data['error'],
                                                                            type: "error",
                                                                            confirmButtonColor: "#f0ad4e",
                                                                            confirmButtonText: "Try Again!",
                                                                            closeOnConfirm: false,
                                                                        }, function() {

                                                                            // swal("Deleted!", "Your imaginary file has been deleted.", "success");
                                                                            location.reload(true)

                                                                        });
                                                                    }
                                                                });
                                                            } else {

                                                                swal({
                                                                    title: 'Oops',
                                                                    text: data['error'],
                                                                    type: "error",
                                                                    confirmButtonColor: "#f0ad4e",
                                                                    confirmButtonText: "Try Again!",
                                                                    closeOnConfirm: false,
                                                                }, function() {

                                                                    // swal("Deleted!", "Your imaginary file has been deleted.", "success");
                                                                    location.reload(true)

                                                                });
                                                            }
                                                        });
                                                    } else {

                                                        swal({
                                                            title: 'Oops',
                                                            text: data['error'],
                                                            type: "error",
                                                            confirmButtonColor: "#f0ad4e",
                                                            confirmButtonText: "Try Again!",
                                                            closeOnConfirm: false,
                                                        }, function() {

                                                            // swal("Deleted!", "Your imaginary file has been deleted.", "success");
                                                            location.reload(true)

                                                        });
                                                    }
                                                });
                                            } else {

                                                swal({
                                                    title: 'Oops',
                                                    text: data['error'],
                                                    type: "error",
                                                    confirmButtonColor: "#f0ad4e",
                                                    confirmButtonText: "Try Again!",
                                                    closeOnConfirm: false,
                                                }, function() {

                                                    // swal("Deleted!", "Your imaginary file has been deleted.", "success");
                                                    location.reload(true)

                                                });
                                            }
                                        });
                                    } else {

                                        swal({
                                            title: 'Oops',
                                            text: data['error'],
                                            type: "error",
                                            confirmButtonColor: "#f0ad4e",
                                            confirmButtonText: "Try Again!",
                                            closeOnConfirm: false,
                                        }, function() {

                                            // swal("Deleted!", "Your imaginary file has been deleted.", "success");
                                            location.reload(true)

                                        });
                                    }
                                });
                            } else {

                                swal({
                                    title: 'Oops',
                                    text: data['error'],
                                    type: "error",
                                    confirmButtonColor: "#f0ad4e",
                                    confirmButtonText: "Try Again!",
                                    closeOnConfirm: false,
                                }, function() {

                                    // swal("Deleted!", "Your imaginary file has been deleted.", "success");
                                    location.reload(true)

                                });
                            }
                        });
                    } else {

                        swal({
                            title: 'Oops',
                            text: data['error'],
                            type: "error",
                            confirmButtonColor: "#f0ad4e",
                            confirmButtonText: "Try Again!",
                            closeOnConfirm: false,
                        }, function() {

                            // swal("Deleted!", "Your imaginary file has been deleted.", "success");
                            location.reload(true)

                        });
                    }
                });
            } else {

                document.getElementById('error').style.display = 'block';
                document.getElementById('error').innerText = data['error'];
                document.getElementById('modelBlock').style.display = 'none';
                document.getElementById('percent').innerText = "0%";
                document.getElementById('bar').style.width = 0;
                // document.getElementById('fileUpload').reset();
            }
        }
    });
} //  Call api for Analyze Summary

function summary(dumpdata, NewDumpid) {
    // console.log(dumpdata);
    $.post('/platform/windows/analyze/summary/ ', {
        data: dumpdata,
        csrfmiddlewaretoken: getCookie('csrftoken'),
    }, function(data) {
        document.getElementById('status').style.display = 'none';
        document.getElementById('modelBlock').style.display = 'none';
        // console.log(data);
        // var data = json;
        data = JSON.parse(data);

        if (data["success"] == 1) {
            var row1 = '<center><table style="text-align: center;">' + ' <tr> <td style="text-align:center;"> Start Time </td> <td style="text-align: center;margin-left:10px;"><span style="color:#F8BB86"> ' + data.data['start_time'] + ' </span> </td> </tr> ' + ' <tr> <td style="text-align:center;"> End Time </td> <td style="text-align: center;margin-left:10px;"><span style="color:#F8BB86"> ' + data.data['end_time'] + ' </span> </td> </tr> ' + ' <tr> <td style="text-align:center;"> Total Execution time </td> <td style="text-align: center;margin-left:10px;"><span style="color:#F8BB86"> ' + data.data['time_min'] + ' : ' + data.data['time_sec'] + ' min:sec </span> </td> </tr> ' + ' <tr> <td style="text-align:center;"> Process </td> <td style="text-align: center;margin-left:10px;"><span style="color:#F8BB86"> ' + data.data['total_process'] + ' </span> </td> </tr> ' + '<tr> <td style="text-align:center;"> Threads </td> <td style="text-align: center; margin-left:10px;"><span style="color:#F8BB86"> ' + data.data['total_thread'] + ' </span> </td> </tr> ' + '<tr> <td style="text-align:center;"> DLL </td> <td style="text-align: center; margin-left:10px;"><span style="color:#F8BB86"> ' + data.data['total_dll'] + ' </span> </td> </tr> ' + '<tr> <td style="text-align:center;"> Handles </td> <td style="text-align: center; margin-left:10px;"><span style="color:#F8BB86"> ' + data.data['total_handles'] + ' </span> </td> </tr> ' + '<tr> <td style="text-align:center;">  Registry Hives </td> <td style="text-align: center; margin-left:10px;"><span style="color:#F8BB86"> ' + data.data['total_reghives'] + ' </span> </td> </tr> ' + '<tr> <td style="text-align:center;"> Network-Connection </td> <td style="text-align: center; margin-left:10px;"><span style="color:#F8BB86"> ' + data.data['total_network'] + ' </span> </td> </tr> ';
            swal({
                title: 'Analyze Summary !',
                text: row1,
                html: true,
                type: "success",
                confirmButtonColor: "#5cb85c",
                confirmButtonText: "Show Process Details",
                closeOnConfirm: false,
            }, function() {

                // swal("Deleted!", "Your imaginary file has been deleted.", "success");
                location.reload(true)

            });
            // $('#formDumpId').submit();
            // console.log("set new dump >>>",NewDumpid);
            // localStorage.setItem("NewDumpid", NewDumpid);
            // get_data_Datatable(NewDumpid);
            // location.reload(true);
            // return true;
        } else {
            return false;
        }
    });

} //  --------------- this functio helps to resolve 403 error regarding to csrf token

function getCookie(cname) {
    var name = cname + '=';
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
    return '';
} // ------------------ this function bind json responce into data table

function getThread(pid, dumpid) {
    document.getElementById('t_pid').value = pid;
    document.getElementById('t_dump_id').value = dumpid;
    // return false;
    $('#frmThread').submit();
}

function getDll(pid, dumpid) {
    document.getElementById('d_pid').value = pid;
    document.getElementById('d_dump_id').value = dumpid;
    // return false;
    $('#frmDll').submit();
}

function getHandle(pid, dumpid) {
    document.getElementById('h_pid').value = pid;
    document.getElementById('h_dump_id').value = dumpid;
    // return false;
    $('#frmHandle').submit();
}

function format(d) {
    // console.log(d.pid,d.dump.id);
    // `d` is the original data object for the row
    return '<a href="#" onclick="getThread(' + d.pid + ',' + d.dump.id + ');" class="btn btn-success"> Thread </a>' + '     ' +
        '<a href="#" onclick="getHandle(' + d.pid + ',' + d.dump.id + ');" class="btn btn-success"> Handles </a>' + '      ' +
        '<a href="#" onclick="getDll(' + d.pid + ',' + d.dump.id + ');" class="btn btn-success"> Dlls </a>';
}

function get_data_Datatable(dump) {
    document.getElementById("newData").style.display = "block"
    var dt = $('#example').DataTable({
        'processing': true,
        // "stateSave": true,
        'language': {
            'processing': 'there is some problem while fetching data',
        },
        'ajax': {
            // "type":"POST",
            // "url": "{% static 'js/data.json'  %}",
            'url': '/platform/windows/json/processes/?dump=' + dump + '&format=json',
            // "url": "/platform/windows/json/processes/?dump=1&format=json",
            'headers': {
                'X-CSRFToken': getCookie('csrftoken')
            },
            'dataSrc': '',
            error: function(data) {
                alert(JSON.stringify(data));
            },
        },
        'columns': [{
                'data': null
            },
            {
                'className': 'details-control',
                'orderable': false,
                'data': null,
                'defaultContent': ''
            },
            {
                'data': 'id',
                'visible': false,
            },
            {
                'data': 'pid',
                'render': function(data, type, row, meta) {
                    // document.getElementById("setDumpid").value = row["dump"];
                    var a = '<a href="#" onclick="setDemo(this.innerText,' + row['dump'].id + ')" >' + data + '</a>';
                    return a;
                }
            },
            {
                'data': 'ppid',
                'render': function(data, type, row, meta) {
                    // document.getElementById("setDumpid").value = row["dump"];
                    var a = '<a href="#" onclick="setDemo(this.innerText,' + row['dump'].id + ')" >' + data + '</a>';
                    return a;
                }
            },
            {
                'data': 'name',
                'render': function(data, type, row, meta) {
                    var a = '<a href="/platform/windows/process/download/?process=' + row['id'] + '">' + data + '</a>';
                    return a;
                }
            },
            {
                'data': 'thread_count'
            },
            {
                'data': 'handle_count'
            },
            {
                data: null,
                className: 'center',
                defaultContent: '',
                'render': function(data, type, row, meta) {
                    var a = '<input class="btn btn-success" type="button" onclick="startScan(' + row['id'] + ')" value="Scan">'
                    return a;
                }
            },
        ],
        'columnDefs': [{
            'targets': 0,
            'checkboxes': {
                'selectRow': false
            }
        }],
        'select': {
            'style': 'multi'
        },
        'order': [
            [1,
                'asc'
            ]
        ]
    });
    // Handle form submission event
    var ID = [];
    $('#frm-example').on('submit', function(e) {
        document.getElementById('modelScan').style.display = 'block';
        var form = this;
        var rows_selected = dt.column(0).checkboxes.selected();
        var selectedIds = dt.columns().checkboxes.selected()[0].length;
        if (selectedIds == 0) {
            dt.column(0).checkboxes.select();
            rows_selected = dt.column(0).checkboxes.selected();
        } // Iterate over all selected checkboxes

        $.each(rows_selected, function(index, rowId) {
            ID.push(rows_selected[index].id);
            // console.log(ID.join(','));
            $('#example-console-rows').text(ID);
            // Create a hidden element
            $(form).append($('<input>').attr('type', 'hidden').attr('name', 'id[]').val(rowId));
        });
        $.get('/platform/windows/process/report/?processes=' + ID.join(',') + '', {
            csrfmiddlewaretoken: getCookie('csrftoken'),
        }, function(json) {});
        window.location.href = '/platform/windows/process/report/?processes=' + ID.join(',') + '';
        ID = [];
        e.preventDefault();
        document.getElementById('modelScan').style.display = 'none';
    });
    // ---------------------------------------------------------------------------
    // Add event listener for opening and closing details
    $('#example tbody').on('click', 'td.details-control', function() {
        var tr = $(this).closest('tr');
        var row = dt.row(tr);
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        } else {
            // Open this row
            row.child(format(row.data())).show();
            tr.addClass('shown');
        }
    });
}

function setDemo(e, f) {
    document.getElementById('setPid').value = e;
    document.getElementById('setDumpid').value = f;
    $('#formProcess').submit();
}

function startScan(x) {
    document.getElementById('modelScan').style.display = 'block';
    $.post('/platform/windows/process/scan/', {
        'process': x,
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'contentType': false,
    }, function(json) {
        // console.log(json);
        var data = jQuery.parseJSON(json);
        // console.log(data['success']);
        if (data['success'] == '1') {
            document.getElementById('scanid').value = data['scan'];
            // document.getElementById('setdumpname').value = dump;
            $('#frmScan').submit();
            document.getElementById('modelScan').style.display = 'none';
        } else {
            alert(data['error']);
            document.getElementById('modelScan').style.display = 'none';
        }
    })
}

//  Code for chekc Extension of File uplode
var _validFileExtensions = [".zip", ];

function ValidateSingleInput(oInput) {
    if (oInput.type == "file") {
        var sFileName = oInput.value;
        if (sFileName.length > 0) {
            var blnValid = false;
            for (var j = 0; j < _validFileExtensions.length; j++) {
                var sCurExtension = _validFileExtensions[j];
                if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
                    blnValid = true;
                    break;
                }
            }

            if (!blnValid) {
                alert("Sorry, " + sFileName + " is invalid, allowed extensions are: " + _validFileExtensions.join(", "));
                oInput.value = "";
                return false;
            }
        }
    }
    return true;
}


function onLoad(NewDumpid) {
    // localStorage.setItem("NewDumpid", NewDumpid);
    // var NewDumpid = localStorage.getItem("NewDumpid");
    // console.log("get new dump >>>",NewDumpid);

    get_data_Datatable(NewDumpid);

}