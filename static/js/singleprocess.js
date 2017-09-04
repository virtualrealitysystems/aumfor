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

function get_data_Datatable(dumpid,pid) {
    $("#analyzedprocess").addClass("active");
    $("#ddmenu1").removeClass("active");
    $("#bredcum").append('<li><a href="/process/">Analyzed Processes </a></li>');
    $("#bredcum").append('<li>Process Detail</li>');


    $.ajax({
        'type': "GET",
        // contentType: "application/json; charset=utf-8",
        'url': "/platform/windows/json/processes/?dump=" + dumpid + "&pid= " + pid +"",
        "headers": {
            "X-CSRFToken": getCookie('csrftoken')
        },
        // dataType: "json",
        success: function(data) {
            // console.log(data);
            if (data) {
                dump = data[0].dump.upload.dump_location;
                dump = dump.split("/")[4];
                dump = dump.split("-")[2];
                document.getElementById("dumpProfile").innerText = dump;
                $.each(data[0], function(key, value) {
                    if (key == "id") {

                    } else {
                        if (key == "as_layer2") {

                        } else {
                            if (key == "dump") {

                            } else {
                                $("#example tbody").append('<tr><td>' + value + '</td></tr>');
                            }

                        }
                    }
                });
            } else {
                alert("no data found:")
            }

        },

        error: function(data) {
            console.log(data);
        }

    });
}
