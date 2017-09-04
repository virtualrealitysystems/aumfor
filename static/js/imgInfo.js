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

function get_data(upload_id)
{
     $.ajax({
        'type': "GET",
        // contentType: "application/json; charset=utf-8",
        'url': "/platform/windows/json/dumps/?upload="+ upload_id +"",
        "headers": {
            "X-CSRFToken": getCookie('csrftoken')
        },
        // dataType: "json",
        success: function(data) {
            var len = data.length;
            if (data) {
                $.each(data[0], function(key, value) {
                    if (key == "as_layer2") {

                    } else {
                        if (key == "id") {

                        } else {

                            if (key == "upload") {

                            } else {
                                if (key == "suggested_profiles")
                                {
                                    $("#example tbody").append('<tr><td style="height:65px">' + value + '</td></tr>');    
                                }
                                else if( key == "start_time" || key == "end_time" )
                                {

                                }
                                else
                                {
                                    $("#example tbody").append('<tr><td>' + value + '</td></tr>');
                                }
                            }
                        }
                    }
                });
            } else {
                alert("no data found:")
            }

        },

        error: function(data) {
            alert(data)
        }

    });
}