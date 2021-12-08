const {createApp, ref, watch} = Vue;
const emitter = mitt();

async function request(endpoint, data = {}) {
    if (data === undefined)
        data = []
    var request = JSON.stringify(data)
    return await fetch(endpoint, {
        method: "POST",
        body: request,
        headers: {'Content-Type': 'application/json'},
    }).then(function (response) {
        return response.json();
    })
        .catch(function (error) {
            console.log('Request failed', error);
        });
}

async function get(endpoint, data = {}) {
    if (data === undefined)
        data = {}
    let search = new URLSearchParams(data).toString();
    return await fetch(endpoint + '?' + search, {
        method: "GET",
    }).then(function (response) {
        return response.json();
    })
        .catch(function (error) {
            console.log('Request failed', error);
        });
}

async function del(endpoint, data = {}) {
    if (data === undefined)
        data = {}
    let search = new URLSearchParams(data).toString();
    return await fetch(endpoint + '?' + search, {
        method: "DELETE",
    }).then(function (response) {
        return response.json();
    })
        .catch(function (error) {
            console.log('Request failed', error);
        });
}

async function put(endpoint, data = {}) {
    if (data === undefined)
        data = {}
    var request = JSON.stringify(data)
    return await fetch(endpoint, {
        method: "PUT",
        body: request,
        headers: {'Content-Type': 'application/json'},
    }).then(function (response) {
        return response.json();
    })
        .catch(function (error) {
            console.log('Request failed', error);
        });
}

async function textRequest(endpoint, data = {}) {
    if (data === undefined)
        data = []
    var request = JSON.stringify(data)
    return await fetch(endpoint, {
        method: "POST",
        body: request,
        headers: {'Content-Type': 'application/json'},
    }).then(function (response) {
        return response.text();
    })
        .catch(function (error) {
            console.log('Request failed', error);
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


const send = async function (endpoint, data = {}) {
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
            return e;
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