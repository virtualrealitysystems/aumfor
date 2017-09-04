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

function get_data_Dt(dll_pid,dll_dumpid) {

    $.ajax({
        type: "GET",
        // contentType: "application/json; charset=utf-8",
        url: "/platform/windows/json/processes/?dump=" + dll_dumpid + "&pid=" + dll_pid + "",
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
    $("#bredcum").append('<li>Dll</li>');

    var dt = $('#Dt_dll').DataTable({
        "drawCallback": function(settings) {
            document.getElementById("rowsCount").innerText = settings.aoData.length;
        },
        "ajax": {
            "type": "GET",
            "url": "/platform/windows/json/dlls/?pid="+dll_pid+"&dump="+dll_dumpid+"",
            "dataSrc": "",
            // complete : function(data){alert(JSON.stringify(data))},
            error: function(data) {
                alert(JSON.stringify(data))
            },
        },
        "columns": [{
            "data": null
        }, {
            "data": "id",
            "visible": false,
        }, {
            "data": "base"
        }, {
            "data": "size"
        }, {
            "data": "load_count"
        }, {
            "data": "path"
        }],
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
    $('#frm-print-dll').on('submit', function(e) {
        // document.getElementById('myModal').style.display = "block";
        var form = this;
        var rows_selected = dt.column(0).checkboxes.selected();

        var selectedIds = dt.columns().checkboxes.selected()[0].length;
        if (selectedIds == 0) {

            dt.column(0).checkboxes.select();
            rows_selected = dt.column(0).checkboxes.selected();
        }

        // Iterate over all selected checkboxes
        $.each(rows_selected, function(index, rowId) {
            ID.push(rows_selected[index].id);

            // Create a hidden element 
            $(form).append(
                $('<input>')
                .attr('type', 'hidden')
                .attr('name', 'id[]')
                .val(rowId)
            );
        });
        window.location.href = "/platform/windows/process/dllreport/?dllid=" + ID.join(",") + "";
        ID = [];
        e.preventDefault();
        // document.getElementById('myModal').style.display = "none";
    });
}

function goto_process_detail(e, f) {
    $('#form').submit();
}
