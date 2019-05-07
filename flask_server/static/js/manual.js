$( document ).ready(function() {
    var main_url = document.location.href
    console.log(">>>>>>", main_url);
    if(main_url == "http://localhost:5000/cover/") {
        console.log("this is cover page.");
    } else if(main_url == "http://localhost:5000/") {
        $('#summernote').summernote({
            placeholder: 'Hello bootstrap 4',
            height: 300,                 // set editor height
            minHeight: null,             // set minimum height of editor
            maxHeight: null,             // set maximum height of editor
            focus: true                  // set focus to editable area after initializing summernote
          });
          
     
    }
    else if(main_url == "http://localhost:5000/test") {
        console.log("this is test page. be concern to ajax.")

        var objectData =
                {
                    methods : "POST",
                    data : { email : "a@com",
                            passwd : "a",
                            nickname : "gun"}       
                };

        var objectDataString = JSON.stringify(objectData);

        $.ajax({
                    type: "POST",
                    url: "/users/d/2",
                    contentType: 'application/json',
                    dataType: "json",
                    data: JSON.stringify(objectData),
                    success: function (data) {
                        console.log("data>>", data)
                    },
                    error: function () {
                        console.log(...arguments)
                    }
                });
    };
});


function gwclks(from) {
    if (from === "save_post") {
        var head = $('#head').val();
        var content = $('#summernote').val();

        send_ajax('/posts/add', 'POST', { "data" : { "head" : head, "content" : content }}, 'json', function (res1) {
            console.log("res1>>>>>>>>>> ", res1)
        });

    }
}


function send_ajax(url, method, data, dataType, fn) {
    var options = {
        url: url,
        data: JSON.stringify(data),
        type: method,
        contentType : "application/json",
        dataType: dataType
    };

    if (dataType == 'ajson')
        options.contentType= 'application/json';

    $.ajax(options).done(function (res) {
        if (fn)
            fn(res)

    }).fail(function (xhr, status, errorThrown) {
        console.error("Sorry, there was a problem!", xhr, status, errorThrown);

    }).always(function (xhr, status) {
        console.log("The request is complete!");
    });
}