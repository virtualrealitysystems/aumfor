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

function get_data_datatable(user_id) {

    $("#ddmenu2").children("ul").children("li").children("a").addClass("demo");
    $("#scandata").addClass("active");
    $("#ddmenu1").removeClass("active");
    $("#bredcum").append('<li><a href="/scandata/">Scaned Process</a></li>');
    $(".select2").select2();

    $.ajax({
        type: "GET",
        // contentType: "application/json; charset=utf-8",
        url: "/platform/json/uploads/?user=" + user_id + "",
        "headers": {
            "X-CSRFToken": getCookie('csrftoken')
        },
        // dataType: "json",
        success: function(data) {

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
                    success: function(data) {
                        
                        for (var i = 0; i < data.length; i++) {

                            // console.log(data[i].upload.dump_location);
                            var res = data[i].upload.dump_location.split("/")[4];
                            res = res.split("-")[2];
                            console.log(res);
                            var ddoptid = "dd" + i; // set id of every options
                            var appenddata = '<option value=' + data[i].id + ' id=' + ddoptid + '> ' + res + ' </option>';
                            $('#ddlcas')
                                .append(appenddata);
                            $("#dd0")
                                .attr('selected', 'selected');

                            var dumpid = $( "#ddlcas option:selected" ).val();
                            showData(dumpid);
                        }
                    }
                });
            }
        }
    });
};

function showData(e) {
    var str;
    str = $("select").find(":selected").text();
    document.getElementById("dumpProfile").innerText = str;
    document.getElementById("setdumpname").value = str;
    $('#dt_scan').DataTable({
        "drawCallback": function(settings) {
            document.getElementById("rowsCount").innerText = settings.aoData.length;
        },
        "processing": true,
        // "retrieve": true,
        "destroy": true,
        "language": {
            "emptyTable": "No data available for selected dump please select another dump",
            "loadingRecords": "Loading...",
            "processing": "Processing...",
            "search": "Search:",
            "zeroRecords": "No matching records found",
        },
        "ajax": {
            "type": "POST",
            "url": "/platform/windows/process/scanned/",
            "data": {
                "dump": e
            },
            "dataSrc": "data",
            "headers": {
                "X-CSRFToken": getCookie('csrftoken')
            },
            // complete : function(.){alert(JSON.stringify(data))},
            // error: function(data) {
            //     alert(JSON.stringify(data))
            // },
        },
        "columns": [{
            "data": "id",
            "visible": false,
        }, {
            "data": "process",
            "render": function(data, type, row, meta) {
                var a = '<a href="#" onclick="goto_proceses_detail(this.innerText,' + e + ')" >' + data + '</a>';
                return a;
            }
        }, {
            "data": "process_name",
            "render": function(data, type, row, meta) {
                var a = '<a href="#" onclick="goto_proceses_detail(' + row["process"] + ',' + e + ')" >' + data + '</a>';
                return a;
            }
        }, {
            "data": "total"
        }, {
            "data": "scan_date"
        }, {
            "data": "positives"
        }, {
            "data": "null",
            "render": function(data, type, row, meta) {
                var a = '<input type="button" class="btn btn-success" onclick="startScan(' + row["id"] + ')" value="Get Report">'
                return a;
            }
        }],
    });
    // table.ajax.reload();
    // table.destroy();
}

function startScan(x) {
    document.getElementById("modelMSG").style.display = "block";
    $.post("/platform/windows/process/scan/", {
        "process": x,
        "csrfmiddlewaretoken": getCookie('csrftoken'),
        "contentType": false,
    }, function(json) {
        console.log(json);
        var data = jQuery.parseJSON(json);
        console.log(data["success"]);
        if (data["success"] == "1") {
            document.getElementById("scanid").value = data["scan"];
            document.getElementById("setPk").value = x;
            $('#frmScan').submit();
            document.getElementById("modalBlock").style.display = "none";
        } else {
            alert(data["error"]);
            document.getElementById("modalBlock").style.display = "none";
        }
    })
}

function goto_proceses_detail(e, f) {
    document.getElementById("setPid").value = e;
    document.getElementById("setDumpid").value = f;
    document.getElementById("dumpName").value = $("select").find(":selected").text()
    $('#formprocessdetail').submit();
}
