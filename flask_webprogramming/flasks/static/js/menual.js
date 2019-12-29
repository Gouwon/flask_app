function _ajax(url, data, method='GET', fn, dataType="application/json"){
    (function (){   // IIFE
        var req = new XMLHttpRequest();
        req.open(method, url);
        req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        req.onreadystatechange = function () { 
            if (req.readyState === 4 && req.status === 200) { 
                result.innerText = this.responseText; 
                if(!!fn){
                    fn(this.response);
                }
            } 
        }; 

        if(dataType=="application/json"){
            data = JSON.stringify(data);
        }
        req.send(data);
    })();
}