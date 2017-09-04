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


function get_data_Datatable(scan_id) 
{
    $.ajax({
        type: "GET",
        // contentType: "application/json; charset=utf-8", 
        url: "/platform/windows/json/scan-results/?scan_information=" + scan_id +"",

        "headers": {
            "X-CSRFToken": getCookie('csrftoken')
        },
        // dataType: "json",
        success: function(data) {
           
            // console.log(data[0].detected);
            var counter = 0;
            for (var i = 0; i < data.length; i++) {
                if (data[i].detected == true) {
                    counter = counter + 1;
                }
            }
            document.getElementById("detectedThread").innerText = counter;

            var scanid = data[0].scan_information;
            // console.log(data[0].scan_information);
            $.ajax({
                type: "GET",
                // contentType: "application/json; charset=utf-8", 
                url: "/platform/windows/json/scans/" + scanid + "/",

                "headers": {
                    "X-CSRFToken": getCookie('csrftoken')
                },
                // dataType: "json",
                success: function(data) {
                   
                    $.ajax({
                        type: "GET",
                        // contentType: "application/json; charset=utf-8", 
                        url: "/platform/windows/json/processes/" + data.process + "/",

                        "headers": {
                            "X-CSRFToken": getCookie('csrftoken')
                        },
                        // dataType: "json",
                        success: function(data) {
                            // console.log(data);
                            document.getElementById("processName").innerText = data.name;

                            document.getElementById("setPid").value = data.pid;
                            document.getElementById("setDumpid").value = data.dump.id;
                        }
                    });

                }
            });
        }
    });

    $("#ddmenu2").children("ul").children("li").children("a").addClass("demo");
    $("#ddmenu1").removeClass("active");
    $("#scandata").addClass("active");
    $("#bredcum").append('<li><a href="/scandata/">Scaned Process</a></li>');
    $("#bredcum").append('<li>Scaned Process Report</li>');

    var counter = 0;
    var dt = $('#example').DataTable({
        "drawCallback": function(settings) {
            document.getElementById("rowsCount").innerText = settings.aoData.length;
        },
        "processing": true,
        // "retrieve": true,
        "destroy": true,
        "scrollY": false,
        "paging": false,
        "language": {
            "emptyTable": "Table is empty",
            "loadingRecords": "Loading...",
            "processing": "Processing...",
            "search": "Search:",
            "zeroRecords": "No matching records found",
        },
        "createdRow": function(row, data, dataIndex) {
            // console.log(data.detected);
            if (data.detected == true) {
                $(row).addClass('selected');
            }
        },

        "ajax": {
            "type": "GET",
            "url": "/platform/windows/json/scan-results/?scan_information=" + scan_id + "",
            "dataSrc": "",
            // complete : function(.){alert(JSON.stringify(data))},
            // error: function(data) { alert(JSON.stringify(data)) },
        },
        "columns": [{
            "data": null
        }, {
            "data": "id",
            "visible": false,
        }, {
            "data": "anti_virus_name"
        }, {
            "data": "detected"
        }, {
            "data": "version"
        }, {
            "data": "result"
        }, {
            "data": "update"
        }, {
            "data": "scan_information",
            "visible": false,
        }, ],
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

    var ID = [];
    $('#frm-example').on('submit', function(e) {
        document.getElementById('modelScan').style.display = "block";
        var form = this;
        var rows_selected = dt.column(0).checkboxes.selected();

        // Iterate over all selected checkboxes
        var selectedIds = dt.columns().checkboxes.selected()[0].length;
        if (selectedIds == 0) {

            dt.column(0).checkboxes.select();
            rows_selected = dt.column(0).checkboxes.selected();
        }

        $.each(rows_selected, function(index, rowId) {
            ID.push(rows_selected[index].id);
            $('#example-console-rows').text(ID);
            // Create a hidden element 
            $(form).append(
                $('<input>')
                .attr('type', 'hidden')
                .attr('name', 'id[]')
                .val(rowId)
            );
        });

        window.location.href = "/platform/windows/process/scanreport/?scanid=" + ID.join(",") + "";

        ID = [];
        e.preventDefault();
        document.getElementById('modelScan').style.display = "none";
    });
}

function setDemo(e, f) {
    $('#form').submit();
}