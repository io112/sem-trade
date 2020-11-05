document.getElementById('input-clientname').addEventListener("input", submitClient)

var sid = ""

function submitClient() {
    if (sid === "") {
        var url = new URL(window.location.href);
        sid = url.searchParams.get("sid");
        alert(sid)
    }

    name = document.getElementById("input-clientname").value;
    data = {"name": name}
    res = send("/api/update_session", data);
}

function send(endpoint, data) {
    var request = {"data": JSON.stringify(data), "sid": sid}
    console.log(sid)
    $.ajax({
        type: "POST",
        url: endpoint,
        data: request,
        success: function (e) {
            return e
        },
        fail: function (e) {
            return e
        }
    })
}