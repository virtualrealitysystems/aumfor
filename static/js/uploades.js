function get_data_datatable(user_id) {

    $("#upload").addClass("active");
    $("#ddmenu1").removeClass("active");
    $("#bredcum").append('<li><a href="/dumps/">Uploded Dumps</a></li>');

    var dt = $('#Dt_upload').DataTable({
        "drawCallback": function(settings) {
            document.getElementById("rowsCount").innerText = settings.aoData.length;
        },
        "language": {
            "emptyTable": "Table is empty",
            "loadingRecords": "Loading...",
            "processing": "Processing...",
            "search": "Search:",
            "zeroRecords": "No matching records found",
        },

        "ajax": {
            // "url": "{% static 'js/data.json'  %}",
            "url": "/platform/json/uploads/?user=" + user_id + "",
            "dataSrc": ""
        },
        "columns": [{
            "data": null
        }, {
            "data": "id",
            "render": function(data, type, row, meta) {
                var res = row["dump_location"].split("/")[4];
                res = res.split("-")[2];
                var a = '<a href="#" onclick="gotoimageinfo(this.innerText,\'' + res + '\')" >' + data + '</a>';
                return a;
            }
        }, {
            "data": "dump_location",
            "render": function(data, type, row, meta) {
                var res = data.split("/")[4];
                res2 = res.split("-")[2];
                var a = '<a href="#" onclick="gotoimageinfo(' + row["id"] + ',this.innerText)" >' + res2 + '</a>';
                return a;
            }
        }, {
            "data": "status"
        }, {
            "data": "uploaded_on"
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
    $('#frm-upload').on('submit', function(e) {
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
            // $('#example-console-rows').text(ID);
            // Create a hidden element 
            $(form).append(
                $('<input>')
                .attr('type', 'hidden')
                .attr('name', 'id[]')
                .val(rowId)
            );
        });
        window.location.href = "/platform/windows/process/uploadreport/?uploadid=" + ID.join(",") + "";
        ID = [];
        e.preventDefault();


    });

}

function gotoimageinfo(e, f) {
    console.log(e, f)
    document.getElementById("uploadid").value = e;
    document.getElementById("uploadname").value = f;
    $('#form').submit();
}
