document.addEventListener("DOMContentLoaded", init);
as = ''
fs = ''
fs1 = ''
fs2 = ''

let sid = ""
let current_selection = ""

function init() {
    let url = new URL(window.location.href);
    sid = url.searchParams.get("sid");
    $('#input-clientname').on("input", submitClient)
    as = $('#arm_section')
    fs = $('#fiting_section')
    fs1 = $('#fiting_1_section')
    fs2 = $('#fiting_2_section')
    as.on('change', submitArm)
    fs1.on('change', submitFits)
    fs2.on('change', submitFits)
    updateArmSection();
    updateFitSections()
}

function submitClient() {
    name = document.getElementById("input-clientname").value;
    let data = [{"name": name}]
    writeToSession(sid, data)
}

function submitArm() {
    let data = {"selection": {"arm": {}}}
    let formRes = as.serializeArray()
    formRes.forEach(i => {
        if (i.value !== "")
            data["selection"]["arm"][i.name] = i.value
    })
    let resp = writeToSession(sid, data).then(() => updateArmSection())
}

function submitFits() {
    let data = {"selection": {"fitings": {}}}
    let fit1 = fs1.serializeArray()
    let fit2 = fs2.serializeArray()
    data["selection"]["fitings"]['1'] = {}
    data["selection"]["fitings"]['2'] = {}
    fit1.forEach(i => {
        if (i.value !== "")
            data["selection"]["fitings"]['1'][i.name] = i.value
    })
    fit2.forEach(i => {
        if (i.value !== "")
            data["selection"]["fitings"]['2'][i.name] = i.value
    })
    let resp = writeToSession(sid, data).then(() => updateFitSections())
}

function submitFit(dict, name) {
    let data = {"selection": {"fitings": {}}}
    let formRes = dict
    console.log(formRes)
    data["selection"]["fitings"][name] = {}
    formRes.forEach(i => {
        if (i.value !== "")
            data["selection"]["fitings"][name][i.name] = i.value
    })
    let resp = writeToSession(sid, data).then(() => updateFitSections())
}

function dropArm() {
    let data = {"selection": {"arm": {}}}

    let resp = writeToSession(sid, data).then(() => updateArmSection())
}

function dropFits() {
    let data = {"selection": {"fitings": {}}}
    data["selection"]["fitings"]['1'] = {}
    data["selection"]["fitings"]['2'] = {}

    let resp = writeToSession(sid, data).then(() => updateFitSections())
}

function writeToSession(sid, data) {
    let res = send("/api/update_session", data);
    return res
}

function updateArmSection() {
    send('/api/update_selection').then((resp) => {
        resp = JSON.parse(resp)
        const diameter_select = $('#input-arm-diameter')
        const braid_select = $('#input-arm-braid')
        const type_select = $('#input-arm-type')
        diameter_select.empty().append(new Option("Выберите диаметр", ""));
        braid_select.empty().append(new Option("Выберите оплетку", ""));
        type_select.empty().append(new Option("Выберите тип рукава", ""));
        let offer = createUniqueArmOffer(resp)
        let selection = resp['selection']['arm']
        if (selection === undefined) {
            selection = {}
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
        if (selection['diameter'] !== undefined) {
            $("#input-arm-diameter option:last").attr("selected", "selected");
        }
        if (selection['braid'] !== undefined) {
            $("#input-arm-braid option:last").attr("selected", "selected");
        }
        if (selection['arm_type'] !== undefined) {
            $("#input-arm-type option:last").attr("selected", "selected");
        }

        document.getElementById('input-arm-diameter').fstdropdown.rebind()
        document.getElementById('input-arm-type').fstdropdown.rebind()
        document.getElementById('input-arm-braid').fstdropdown.rebind()
    })

}

function updateFitSections() {
    send('/api/update_selection').then((resp) => {
        resp = JSON.parse(resp);
        ['1', '2'].forEach((num) => updateFitSection(num, resp));
    })
}

function updateFitSection(num, resp) {
    const standart_select = $('#input-fit-std-' + num)
    const diameter_select = $('#input-fit-d-' + num)
    const fit_select = $('#input-fit-' + num)
    diameter_select.empty().append(new Option("Выберите диаметр", ""));
    standart_select.empty().append(new Option("Выберите стандарт фитинга", ""));
    fit_select.empty().append(new Option("Выберите фитинг", ""));
    let offer = createUniqueFitOffer(resp, num)
    let selection = resp['selection']['fitings']
    if (selection === undefined) {
        selection = {'1': {}, '2': {}}
    }
    selection = selection[num]
    offer[0].forEach((diameter) => {
        diameter_select.append(new Option(diameter + ' мм', diameter));
    })
    offer[1].forEach((standart) => {
        standart_select.append(new Option(standart, standart));
    })
    offer[2].forEach((fit) => {
        fit_select.append(new Option(fit, fit));
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

    document.getElementById('input-fit-std-' + num).fstdropdown.rebind()
    document.getElementById('input-fit-d-' + num).fstdropdown.rebind()
    document.getElementById('input-fit-' + num).fstdropdown.rebind()
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

async function send(endpoint, data) {
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
            return e
        }
    });
}