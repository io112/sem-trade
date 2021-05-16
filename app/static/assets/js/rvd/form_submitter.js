'use strict'

document.addEventListener("DOMContentLoaded", init);
let as = ''
let fs = ''
let fs1 = ''
let fs2 = ''

let sid = ""
let current_selection = {
    "items": {
        "arm": {},
        "fiting1": {},
        "fiting2": {},
        "clutch1": {},
        "clutch2": {},
    },
    "subtotal": {},
}
let parameters = {
    "arm": {},
    "fiting1": {},
    "fiting2": {},
    "clutch1": {},
    "clutch2": {},
}
let candidates = {
    "arm": {},
    "fiting1": {},
    "fiting2": {},
    "clutch1": {},
    "clutch2": {},
}

let current_offer = {
    "selection": current_selection,
    "candidates": candidates,
    "parameters": parameters
}


function init() {
    sid = Cookies.get('current_order');
    console.log(sid)
    init_cw()
    as = $('#arm_section');
    fs = $('#fiting_section');
    fs1 = $('#fiting_1_section');
    fs2 = $('#fiting_2_section');
    as.on('change', submitArm);
    fs1.on('change', submitFits);
    fs2.on('change', submitFits);
    getCurrentSelection().then(() => {
        updateArmSection();
        updateFitSections();
        update_cart();
        init_sessions();
    })
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

function submitArm() {
    let formRes = as.serializeArray()
    formRes.forEach(i => {
        let val = tryParseFloat(i.value)
        if (i.value !== "")
            current_selection["items"]["arm"][i.name] = val
        else
            delete current_selection["items"]["arm"][i.name]
        if (i.name === "diameter") {
            current_selection["items"]["clutch1"] = {'diameter': val}
            current_selection["items"]["clutch2"] = {'diameter': val}
        }

    })
    writeToSession(sid, current_selection).then(() => {
        getCurrentSelection().then(() => {
            updateArmSection()
            updateFitSections()
        })
    })
}

function submitFits() {
    let fit1 = fs1.serializeArray()
    let fit2 = fs2.serializeArray()
    fit1.forEach(i => {
        let val = tryParseFloat(i.value)
        if (i.value !== "") {
            if (i.name === "clutch_name")
                current_selection["items"]["clutch1"]["id"] = val
            else
                current_selection["items"]["fiting1"][i.name] = val
        } else {
            if (i.name === "clutch_name")
                delete current_selection["items"]["clutch1"]["id"]
            else
                delete current_selection["items"]["fiting1"][i.name]
        }
    })
    fit2.forEach(i => {
        let val = tryParseFloat(i.value)
        if (i.value !== "") {
            if (i.name === "clutch_name")
                current_selection["items"]["clutch2"]["id"] = val
            else
                current_selection["items"]["fiting2"][i.name] = val
        } else {
            if (i.name === "clutch_name")
                delete current_selection["items"]["clutch2"]["id"]
            else
                delete current_selection["items"]["fiting2"][i.name]
        }
    })
    writeToSession(sid, current_selection).then(() => getCurrentSelection().then(() => updateFitSections()))
}

function dropArm() {
    current_selection["items"]["arm"] = {}
    current_selection["items"]["clutch1"] = {}
    current_selection["items"]["clutch2"] = {}

    let resp = writeToSession(sid, current_selection).then(() => getCurrentSelection().then(() => updateArmSection()))
}

function dropFits() {
    current_selection["items"]["fiting1"] = {}
    current_selection["items"]["fiting2"] = {}

    let resp = writeToSession(sid, current_selection).then(() => getCurrentSelection().then(() => updateFitSections()))
}

function dropClutches() {
    current_selection["items"]["clutch1"] = {}
    current_selection["items"]["clutch2"] = {}

    writeToSession(sid, current_selection).then(() => getCurrentSelection().then(() => updateFitSections()))
}

function writeToSession(sid, data) {
    return send("/api/make_order/update_selection_items", data)
}

function updateArmSection() {
    let resp = current_offer;
    const diameter_select = $('#input-arm-diameter')
    const braid_select = $('#input-arm-braid')
    const type_select = $('#input-arm-type')
    const length_select = $('#input-arm-length')
    const arm_select = $('#input-arm')
    diameter_select.empty().append(new Option("Выберите диаметр", ""));
    braid_select.empty().append(new Option("Выберите оплетку", ""));
    type_select.empty().append(new Option("Выберите тип рукава", ""));
    arm_select.empty().append(new Option("Выберите рукав", ""));
    console.log(resp)
    let offer = resp['parameters']['arm']
    let selection = current_selection["items"]['arm']
    if (selection === undefined) {
        selection = {}
    }
    if (selection['amount'] !== undefined) {
        length_select.val(current_selection["items"]["arm"]['amount'])
    } else {
        length_select.val(0);
    }
    offer['diameter'].forEach((diameter) => {
        diameter_select.append(new Option(diameter + ' мм', diameter));
    })
    offer['braid'].forEach((braid) => {
        braid_select.append(new Option(braid, braid));
    })
    offer['arm_type'].forEach((type) => {
        type_select.append(new Option(type, type));
    })
    resp['candidates']['arm'].forEach((arm) => {
        arm_select.append(new Option(`${arm['name']}: ${arm['amount']}`, arm['_id']));
    })
    if (selection['diameter'] !== undefined) {
        $("#input-arm-diameter option:last").attr("selected", "selected");
    }
    if (selection['braid'] !== undefined) {
        $("#input-arm-braid option:last").attr("selected", "selected");
    }
    if (selection['arm_type'] !== undefined) {
        $("#input-arm-type option:last").attr("selected", "selected");
    }
    if (selection['id'] !== undefined) {
        $("#input-arm option:last").attr("selected", "selected");
    }

    document.getElementById('input-arm-diameter').fstdropdown.rebind()
    document.getElementById('input-arm-type').fstdropdown.rebind()
    document.getElementById('input-arm-braid').fstdropdown.rebind()
    document.getElementById('input-arm').fstdropdown.rebind()
    updateFitSections();
}

function updateFitSections() {
    let resp = current_offer;
    ['1', '2'].forEach((num) => updateFitSection(num, resp));
}

function updateFitSection(num, resp) {
    const standart_select = $('#input-fit-std-' + num)
    const diameter_select = $('#input-fit-d-' + num)
    const fit_select = $('#input-fit-' + num)
    const muf_select = $('#input-muf-' + num)
    diameter_select.empty().append(new Option("Выберите диаметр", ""));
    standart_select.empty().append(new Option("Выберите стандарт фитинга", ""));
    fit_select.empty().append(new Option("Выберите фитинг", ""));
    muf_select.empty().append(new Option("Выберите муфту", ""));
    let offer = resp['parameters']['fiting' + num]
    let selection = current_selection["items"]['fiting' + num]
    if (selection === undefined) {
        selection = {}
    }
    offer['diameter'].forEach((diameter) => {
        diameter_select.append(new Option(diameter + ' мм', diameter));
    })
    offer['fiting_type'].forEach((standart) => {
        standart_select.append(new Option(standart, standart));
    })
    resp['candidates']['fiting' + num].forEach((fit) => {
        fit_select.append(new Option(`${fit["name"]}: ${fit["amount"]}`, fit["_id"]));
    })
    resp['candidates']['clutch1'].forEach((muf) => {
        muf_select.append(new Option(`${muf["name"]}: ${muf["amount"]}`, muf["_id"]));
    })
    if (selection['fiting_type'] !== undefined) {
        $('#input-fit-std-' + num + " option:last").attr("selected", "selected");
    }
    if (selection['diameter'] !== undefined) {
        $("#input-fit-d-" + num + " option:last").attr("selected", "selected");
    }
    if (selection['id'] !== undefined) {
        $("#input-fit-" + num + " option:last").attr("selected", "selected");
    }
    if (current_selection["items"]['clutch' + num] !== undefined && current_selection["items"]['clutch' + num]['id'] !== undefined) {
        $("#input-muf-" + num + " option:last").attr("selected", "selected");
    }

    document.getElementById('input-fit-std-' + num).fstdropdown.rebind()
    document.getElementById('input-fit-d-' + num).fstdropdown.rebind()
    document.getElementById('input-fit-' + num).fstdropdown.rebind()
    document.getElementById('input-muf-' + num).fstdropdown.rebind()
}


async function send(endpoint, data = {}) {
    if (data === undefined)
        data = []
    var request = {"data": JSON.stringify(data), "sid": sid}
    return await $.ajax({
        type: "POST",
        url: endpoint,
        data: request,
        dataType: 'json',
        success: function (e) {
            return e
        },
        fail: function (e) {
            alert(e)
            return e
        }
    });
}

async function getCurrentSelection() {
    let resp = await send('/api/make_order/get_offer');
    if (resp !== 'NaN') {
        console.log(resp)
        current_selection = resp['selection']
        parameters = resp['parameters']
        candidates = resp['candidates']
        current_offer = resp
        normalize_selection()
    }
    updateSelectionSubtotal()
    return resp;
}

function normalize_selection() {
    let names = ['arm', 'fiting1', 'fiting2', 'clutch1', 'clutch2']
    names.forEach(name => {
        if (current_selection['items'][name] === undefined) {
            current_selection['items'][name] = {}
        }
    })
}

function changeSelectAmount() {
    current_selection["subtotal"]["amount"] = parseInt($('#subtotal_amount').val());
    let resp = writeToSession(sid, current_selection).then(() => {
        getCurrentSelection()
    })

}

function updateSelectionSubtotal() {
    let name = current_selection["subtotal"]["name"]
    let price = current_selection["subtotal"]["price"]
    let amount = current_selection["subtotal"]["amount"]
    let total_price = current_selection["subtotal"]["total_price"]
    $('#select_subtotal tbody').empty().append('<tr>\n' +
        '<td>\n' +
        '<span class="name mb-0 text-sm">' + name + '</span>\n' +
        '</td>\n' +
        '<td class="number">\n' +
        '<input class="form-control" id="subtotal_amount" onchange="changeSelectAmount()" type="number" placeholder="количество" value="' + amount + '">\n' +
        '</td>\n' +
        '<td class="price">\n' + price +
        ' ₽\n' +
        '</td>\n' +
        '<td class="fullprice">\n' + total_price +
        ' ₽\n' +
        '</td>\n' +
        '</tr>'
    );
}

function updateAllSections() {
    getCurrentSelection().then(() => {
        updateFitSections()
        updateArmSection()
        updateSelectionSubtotal()
    })
}

function addToCart() {
    send("/api/make_order/submit_selection", {'sid': sid}).then(
        (ans) => {
            if (ans === 'success') {
                updateAllSections()
                $('#addModal').modal('hide');
            } else {
                alert(ans)
            }
            update_cart();
        }
    );


}

