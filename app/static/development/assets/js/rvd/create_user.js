function create_user() {
    let res = {}
    let form = $('#create-user-form').serializeArray()
    form.forEach(item => {
        if (item.value !== "")
            res[item.name] = item.value
    })
    console.log(res)
    send('/api/create_user', res).then(resp => alert('Пользователь успешно создан!'))
}

async function send(endpoint, data = {}) {
    if (data === undefined)
        data = []
    var request = data
    return await $.ajax({
        type: "POST",
        url: endpoint,
        data: request,
        dataType: 'json',
        success: function (e) {
            return e
        },
        error: function (e) {
            alert(e.responseText)
            return e
        }
    });
}