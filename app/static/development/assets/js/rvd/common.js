async function request(endpoint, data = {}) {
    if (data === undefined)
        data = []
    var request = JSON.stringify(data)
    return await $.ajax({
        type: "POST",
        url: endpoint,
        data: data,
        dataType: 'json',
        success: function (e, textStatus, xhr) {
            console.log(e)
            return e
        },
        error: function (e) {
            alert(e.responseText)
        }
    });
}