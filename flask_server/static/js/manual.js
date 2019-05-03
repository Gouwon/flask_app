$( document ).ready(function() {
    var main_url = document.location.href
    console.log(">>>>>>", main_url);
    if(main_url == "http://localhost:5000/cover/") {
        console.log("this is cover page.");
    } else if(main_url == "http://localhost:5000/test") {
        console.log("this is test page. be concern to ajax.")

        var objectData =
                {
                    methods : "POST"       
                };

        var objectDataString = JSON.stringify(objectData);

        $.ajax({
                    type: "POST",
                    url: "/users/",
                    dataType: "application/json;charset=UTF-8",
                    data: {
                        o: objectDataString
                    },
                    success: function (data) {
                    alert('Success');

                    },
                    error: function () {
                    alert('Error');
                    }
                });
    };
});
