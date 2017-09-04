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

function get_data_Datatable(user_id) {

    // $("#ddmenu2").children("ul").children("li").children("a").addClass("demo");
    $("#registryhives").addClass("active");
    $("#ddmenu1").removeClass("active");
    $("#bredcum").append('<li><a href="/registryhives/">Registery Hives</a></li>');

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

                            console.log(data[i].upload.dump_location);
                            var res = data[i].upload.dump_location.split("/")[4];
                            res = res.split("-")[2];
                            // console.log(res);
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
    var dt = $('#Dt_reg').DataTable({
        "drawCallback": function(settings) {
            document.getElementById("rowsCount").innerText = settings.aoData.length;
        },
        "destroy": true,
        "language": {
            "emptyTable": "Please select Dump",
            "loadingRecords": "Loading...",
            "processing": "Processing...",
            "search": "Search:",
            "zeroRecords": "No matching records found",
        },
        "ajax": {
            "type": "GET",
            //"url":"handles.json",
            "url": "/platform/windows/json/registry-hives/?dump=" + e + "",
            "dataSrc": "",
            // complete : function(data){alert(JSON.stringify(data))},
            //error: function(data) { alert(JSON.stringify(data)) },
        },
        "columns": [{
            "data": null
        }, {
            "data": "id",
            "visible": false,
        }, {
            "data": "name"
        }, {
            "data": "virtual"
        }, {
            "data": "physical"
        }, {
            "data": "dump",
            // "visible": false
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
    $('#frm-reg-print').on('submit', function(e) {
        document.getElementById('modelScan').style.display = "block";
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

            console.log(ID.join(","));


            // Create a hidden element 
            $(form).append(
                $('<input>')
                .attr('type', 'hidden')
                .attr('name', 'id[]')
                .val(rowId)
            );

        });

        window.location.href = "/platform/windows/process/regeport/?regid=" + ID.join(",") + "";

        ID = [];
        e.preventDefault();
        document.getElementById('modelScan').style.display = "none";
    });

};
