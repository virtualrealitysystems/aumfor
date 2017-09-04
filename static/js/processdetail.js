dumpid = 0;

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

function get_data_Datatable(uid) {
    $("#analyzedprocess")
        .addClass("active");
    $("#ddmenu1")
        .removeClass("active");
    $("#bredcum")
        .append('<li><a href="/process/">Analyzed Processes </a></li>');

    $(".select2")
        .select2();

    $.ajax({
        type: "GET",
        // contentType: "application/json; charset=utf-8",
        url: "/platform/json/uploads/?user=" + uid + "",
        "headers": {
            "X-CSRFToken": getCookie('csrftoken')
        },
        // dataType: "json",
        success: function (data) {

            var upload_data = data;
            var len = data.length;
            for (var i = 0; i < len; i++) {
                $.ajax({
                    type: "GET",
                    // contentType: "application/json; charset=utf-8",
                    url: "/platform/windows/json/dumps/?upload=" + data[i].id + "",
                    "headers": {
                        "X-CSRFToken": getCookie('csrftoken')
                    },
                    success: function (data) {

                        for (var i = 0; i < data.length; i++) {

                            // console.log(data[i].upload.dump_location);
                            var res = data[i].upload.dump_location.split("/")[4];
                            res = res.split("-")[2];
                            // console.log(res);
                            var ddoptid = "dd" + i; // set id of every options
                            var appenddata = '<option value=' + data[i].id + ' id=' + ddoptid + '> ' + res + ' </option>';
                            $('#ddlcas')
                                .append(appenddata);
                            $("#dd0")
                                .attr('selected', 'selected');

                            var dumpid = $("#ddlcas option:selected").val();
                            showData(dumpid);
                        }
                    }
                });
            }
        }
    });


}

function getThread(pid, dumpid) {

    document.getElementById("t_pid").value = pid;
    document.getElementById("t_dump_id").value = dumpid;
    // return false;
    $("#frmThread").submit();
}

function getDll(pid, dumpid) {

    document.getElementById("d_pid").value = pid;
    document.getElementById("d_dump_id").value = dumpid;
    // return false;
    $("#frmDll").submit();
}

function getHandle(pid, dumpid) {

    document.getElementById("h_pid").value = pid;
    document.getElementById("h_dump_id").value = dumpid;
    // return false;
    $("#frmHandle").submit();
}

function showData(e) {

    document.getElementById("dumpProfile")
        .innerText = $("select")
            .find(":selected")
            .text();
    document.getElementById("setdumpname")
        .value = $("select")
            .find(":selected")
            .text();


    // function for thread handle and dll button
    function format(d) {
        // console.log(d.pid,d.dump.id);
        // `d` is the original data object for the row
        return '<a href="#" onclick="getThread(' + d.pid + ',' + d.dump.id + ');" class="btn btn-success"> Thread </a>' + '     ' +
            '<a href="#" onclick="getHandle(' + d.pid + ',' + d.dump.id + ');" class="btn btn-success"> Handles </a>' + '      ' +
            '<a href="#" onclick="getDll(' + d.pid + ',' + d.dump.id + ');" class="btn btn-success"> Dlls </a>';
    }


    var dt = $('#Dt_process')
        .DataTable({
            "drawCallback": function (settings) {
                // console.log(settings.aoData.length);
                document.getElementById("rowsCount")
                    .innerText = settings.aoData.length;
            },
            "language": {
                "emptyTable": "There is no Data available.",
                "loadingRecords": "Loading...",
                "processing": "Processing...",
                "search": "Search:",
                "zeroRecords": "No matching records found",
            },
            "processing": true,
            // "retrieve": true,
            "destroy": true,
            "scrollX": false,
            "ajax": {
                "url": "/platform/windows/json/processes/?dump=" + e + "",
                "dataSrc": ""
            },
            "columns": [{
                "data": null
            }, {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            }, {
                "data": "id",
                "visible": false,
            }, {
                "data": "pid",
                "render": function (data, type, row, meta) {

                    document.getElementById("setDumpid")
                        .value = row["dump"];

                    var a = '<a href="#" onclick="gotodetial(this.innerText,' + e + ')" >' + data + '</a>';
                    return a;

                }
            }, {
                "data": "name",
                "render": function (data, type, row, meta) {

                    var a = '<a href="/platform/windows/process/download/?process=' + row["id"] + '" >' + data + '</a>';
                    return a;

                }
            }, {
                "data": "ppid",
                "render": function (data, type, row, meta) {

                    // document.getElementById("setDumpid").value = e;
                    //var a = '<a href="#" onclick="$(\'#form\').submit();" >'+data+'</a>';
                    var a = '<a href="#" onclick="gotodetial(this.innerText,' + e + ')" >' + data + '</a>';
                    return a;
                }
            }, {
                "data": "thread_count",
                "render": function (data, type, row, meta) {
                    document.getElementById("setDumpid")
                        .value = e;

                    var a = '<a href="#" onclick="getThread(' + row["pid"] + ',' + row["dump"].id + ')">' + data + '</a>';
                    return a;
                }
            }, {
                "data": "handle_count",
                "render": function (data, type, row, meta) {
                    document.getElementById("setDumpid")
                        .value = e;

                    var a = '<a href="#" onclick="getHandle(' + row["pid"] + ',' + row["dump"].id + ')">' + data + '</a>';
                    return a;
                }
            }, {
                "data": "creation_time"
            }, {
                "data": "termination_time",
                "visible": false
            }, {
                "data": "offset_v",
                "visible": false
            }, {
                "data": "offset_p"
            }, {
                "data": "pdb"
            }, {
                data: null,
                className: "center",
                defaultContent: '',
                buttons: true,
                "render": function (data, type, row, meta) {
                    // var a = '<a href="#" onclick="startScan(' + row["id"] + ')" >Scan</a>';
                    var a = '<input class="btn btn-success" type="button" onclick="startScan(' + row["id"] + ')" value="Scan">'
                    // var a = '<button onclick="startScan(' + row["id"] + ')"> <a href="#">Scan</a></button>';
                    return a;
                }
            },],
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
                [1, 'asc']
            ]

        });

    // ----------------------------------------------------------------------------------
    // Handle form submission event 
    var ID = [];
    $('#frm-process-report')
        .on('submit', function (e) {

            var form = this;
            var rows_selected = dt.column(0)
                .checkboxes.selected();

            var selectedIds = dt.columns()
                .checkboxes.selected()[0].length;
            if (selectedIds == 0) {

                dt.column(0)
                    .checkboxes.select();
                rows_selected = dt.column(0)
                    .checkboxes.selected();
            }

            // Iterate over all selected checkboxes
            $.each(rows_selected, function (index, rowId) {
                ID.push(rows_selected[index].id);

                // Create a hidden element 
                $(form)
                    .append(
                    $('<input>')
                        .attr('type', 'hidden')
                        .attr('name', 'id[]')
                        .val(rowId)
                    );
            });
            window.location.href = "/platform/windows/process/report/?processes=" + ID.join(",") + "";
            ID = [];
            e.preventDefault();

        });

    // ------------------------------------------------------------------------------------
    // var table = $('#Dt_process')
    //     .DataTable();
    // $('#Dt_process tbody')
    //     .on('click', 'tr', function() {
    //         var data = table.row(this)
    //             .data();
    //         dumpid = data["dump"];
    //         document.getElementById("setDumpid")
    //             .value = dumpid;

    //     });

    $('#Dt_process tbody')
        .on('click', 'td.details-control', function () {
            var tr = $(this)
                .closest('tr');
            var row = dt.row(tr);

            if (row.child.isShown()) {
                // This row is already open - close it
                row.child.hide();
                tr.removeClass('shown');
            } else {
                // Open this row
                row.child(format(row.data()))
                    .show();
                tr.addClass('shown');
            }
        });
}

function gotodetial(e, f) {
    document.getElementById("setPid")
        .value = e;
    document.getElementById("setDumpid")
        .value = f;
    document.getElementById("dumpName")
        .value = $("select")
            .find(":selected")
            .text();
    $('#form')
        .submit();
}

function startScan(x) {
    document.getElementById('modelScan')
        .style.display = "block";
    $.post("/platform/windows/process/scan/", {
        "process": x,
        "csrfmiddlewaretoken": getCookie('csrftoken'),
        "contentType": false,
    }, function (json) {
        var data = jQuery.parseJSON(json);
        if (data["success"] == "1") {
            document.getElementById('modelScan')
                .style.display = "none";
            document.getElementById("scanid")
                .value = data["scan"];
            $('#frmScan')
                .submit();
        } else {

            document.getElementById('modelScan')
                .style.display = "none";
        }
    })
}