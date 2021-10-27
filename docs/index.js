var xmlhttp = new XMLHttpRequest();
xmlhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        var myObj = JSON.parse(this.responseText);
        document.getElementById("ip-log").innerHTML = '<pre>' + JSON.stringify(myObj, null, 2) + '</pre>';
    }
};

xmlhttp.open("GET", "./ip_log.json", true);
xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
xmlhttp.send();
