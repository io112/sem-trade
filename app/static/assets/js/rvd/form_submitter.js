'use strict'

document.addEventListener("DOMContentLoaded", init);
let as = ''
let fs = ''
let fs1 = ''
let fs2 = ''

let sid = ""
let current_selection = {
    "arm": {},
    "fiting1": {},
    "fiting2": {},
    "clutch1": {},
    "clutch2": {},
    "final": {}
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
    updateArmSection();
    updateFitSections();
    update_cart();
    init_sessions();
}

function submitArm() {
    let formRes = as.serializeArray()
    formRes.forEach(i => {
        if (i.value !== "")
            current_selection["arm"][i.name] = i.value
        if (i.name === "diameter") {
            current_selection["clutch1"] = {'diameter': i.value}
            current_selection["clutch2"] = {'diameter': i.value}
        }

    })
    let req = {"selection": current_selection}
    let resp = writeToSession(sid, req).then(() => {
        updateArmSection()
        updateFitSections()
    })
}

function submitFits() {
    let fit1 = fs1.serializeArray()
    let fit2 = fs2.serializeArray()
    fit1.forEach(i => {
        if (i.value !== "") {
            if (i.name === "clutch_name")
                current_selection["clutch1"]["name"] = i.value
            else
                current_selection["fiting1"][i.name] = i.value
        }
    })
    fit2.forEach(i => {
        if (i.value !== "") {
            if (i.name === "clutch_name")
                current_selection["clutch2"]["name"] = i.value
            else current_selection["fiting2"][i.name] = i.value
        }
    })
    let req = {"selection": current_selection}
    let resp = writeToSession(sid, req).then(() => updateFitSections())
}

function dropArm() {
    current_selection["arm"] = {}
    current_selection["clutch1"] = {}
    current_selection["clutch2"] = {}

    let req = {"selection": current_selection}
    let resp = writeToSession(sid, req).then(() => updateArmSection())
}

function dropFits() {
    current_selection["fiting1"] = {}
    current_selection["fiting2"] = {}

    let req = {"selection": current_selection}
    let resp = writeToSession(sid, req).then(() => updateFitSections())
}

function dropClutches() {
    current_selection["clutch1"] = {}
    current_selection["clutch2"] = {}

    let req = {"selection": current_selection}
    let resp = writeToSession(sid, req).then(() => updateFitSections())
}

function writeToSession(sid, data) {
    console.log(data)
    let res = send("/api/make_order/update_session", data);
    return res
}

function updateArmSection() {
    getCurrentSelection().then((resp) => {
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
        let offer = createUniqueArmOffer(resp)
        let selection = current_selection['arm']
        if (selection === undefined) {
            selection = {}
        }
        if (current_selection["arm"] !== undefined && current_selection["arm"]['amount'] !== undefined) {
            length_select.val(parseInt(current_selection["arm"]['amount']))
        } else {
            length_select.val(0);
        }
        offer[0].forEach((diameter) => {
            diameter_select.append(new Option(diameter + ' мм', diameter));
        })
        offer[1].forEach((braid) => {
            braid_select.append(new Option(braid, braid));
        })
        offer[2].forEach((type) => {
            type_select.append(new Option(type, type));
        })
        resp['arms'].forEach((arm) => {
            arm_select.append(new Option(arm['name'], arm['name']));
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
        if (selection['arm_type'] !== undefined) {
            $("#input-arm-type option:last").attr("selected", "selected");
        }

        document.getElementById('input-arm-diameter').fstdropdown.rebind()
        document.getElementById('input-arm-type').fstdropdown.rebind()
        document.getElementById('input-arm-braid').fstdropdown.rebind()
        document.getElementById('input-arm').fstdropdown.rebind()
        updateFitSections();
    })

}

function updateFitSections() {
    getCurrentSelection().then((resp) => {
        ['1', '2'].forEach((num) => updateFitSection(num, resp));
    })
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
    let offer = createUniqueFitOffer(resp, num)
    let selection = current_selection['fiting' + num]
    if (selection === undefined) {
        selection = {}
    }
    offer[0].forEach((diameter) => {
        diameter_select.append(new Option(diameter + ' мм', diameter));
    })
    offer[1].forEach((standart) => {
        standart_select.append(new Option(standart, standart));
    })
    offer[2].forEach((fit) => {
        fit_select.append(new Option(fit, fit));
    })
    resp['clutches'].forEach((muf) => {
        muf_select.append(new Option(muf['name'], muf['name']));
    })
    if (selection['fiting_type'] !== undefined) {
        $('#input-fit-std-' + num + " option:last").attr("selected", "selected");
    }
    if (selection['diameter'] !== undefined) {
        $("#input-fit-d-" + num + " option:last").attr("selected", "selected");
    }
    if (selection['name'] !== undefined) {
        $("#input-fit-" + num + " option:last").attr("selected", "selected");
    }
    if (current_selection['clutch' + num] !== undefined && current_selection['clutch' + num]['name'] !== undefined) {
        $("#input-muf-" + num + " option:last").attr("selected", "selected");
    }

    document.getElementById('input-fit-std-' + num).fstdropdown.rebind()
    document.getElementById('input-fit-d-' + num).fstdropdown.rebind()
    document.getElementById('input-fit-' + num).fstdropdown.rebind()
    document.getElementById('input-muf-' + num).fstdropdown.rebind()
}

function createUniqueDict(dict) {
    var res = []
    dict.forEach((elem) => {
        if ($.inArray(elem, res) === -1) {
            res.push(elem);
        }
    })
}

function createUniqueArmOffer(dict) {
    let diameters = []
    let braids = []
    let types = []
    dict['arms'].forEach((arm) => {
        let diameter = arm['diameter']
        let braid = arm['braid']
        let type = arm['arm_type']
        if ($.inArray(diameter, diameters) === -1) {
            diameters.push(diameter);
        }
        if ($.inArray(braid, braids) === -1) {
            braids.push(braid);
        }
        if ($.inArray(type, types) === -1) {
            types.push(type);
        }
    })
    return [diameters, braids, types]
}

function createUniqueFitOffer(dict, num) {
    let diameters = []
    let standarts = []
    let fits = []
    dict['fitings'][num].forEach((fiting) => {
        let diameter = fiting['diameter']
        let standart = fiting['fiting_type']
        let fit = fiting['name']
        if ($.inArray(diameter, diameters) === -1) {
            diameters.push(diameter);
        }
        if ($.inArray(standart, standarts) === -1) {
            standarts.push(standart);
        }
        if ($.inArray(fit, fits) === -1) {
            fits.push(fit);
        }
    })
    return [diameters, standarts, fits]
}

async function send(endpoint, data = {}) {
    if (data === undefined)
        data = []
    var request = {"data": JSON.stringify(data), "sid": sid}
    return await $.ajax({
        type: "POST",
        url: endpoint,
        data: request,
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
    let resp = await send('/api/make_order/update_selection');
    resp = JSON.parse(resp);
    if (resp['selection'] !== undefined) {
        current_selection = resp['selection']
    }
    updateSelectionSubtotal()
    return resp;
}

function changeSelectAmount() {
    if (current_selection["subtotal"] === undefined) {
        current_selection["subtotal"] = {}
    }
    current_selection["subtotal"]["amount"] = parseInt($('#subtotal_amount').val());
    let req = {"selection": current_selection}
    let resp = writeToSession(sid, req).then(() => {
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
    updateFitSections()
    updateArmSection()
    updateSelectionSubtotal()
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

