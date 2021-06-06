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


function tryParseFloat(val) {
    let res = val
    let regex = /^[+-]?([0-9]*([.]|[,]))?[0-9]+$/;
    if (regex.test(res) && res.length > 0) {
        res = parseFloat(val)
        console.log(res)
    }
    return res
}


async function send(endpoint, data = {}) {
    if (data === undefined)
        data = []
    var request = {"data": JSON.stringify(data)}
    return await $.ajax({
        type: "POST",
        url: endpoint,
        data: request,
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

function clean_form(mas) {
    let res = []
    mas.forEach(i => {
        if (i.value !== '') {
            res.push(i)
        }
    })
    return res
}

function formToDict(mas) {
    let res = {}
    mas.forEach(i => {
        if (i.value !== '') {
            let val = tryParseFloat(i.value)
            res[i.name] = val
        }
    })
    return res
}