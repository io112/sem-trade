document.addEventListener("DOMContentLoaded", init);
as = ''

var sid = ""

function init() {
    $('#input-clientname').on("input", submitClient)
    as = $('#arm_section')
    as.on('change', submitArm)
    var url = new URL(window.location.href);
    sid = url.searchParams.get("sid");
    updateArmSection();
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
    console.log(data)
    let resp = writeToSession(sid, data).then(() => updateArmSection())
}

function dropArm() {
    let data = {"selection": {"arm": {}}}
    let formRes = as.serializeArray()
    formRes.forEach(i => {
        if (i.value !== "")
            delete data["selection"]["arm"][i.name]
    })
    console.log(data)
    let resp = writeToSession(sid, data).then(() => updateArmSection())
}

function writeToSession(sid, data) {
    let res = send("/api/update_session", data);
    return res
}

function updateArmSection() {
    send('/api/update_arm_section').then((resp) => {
        resp = JSON.parse(resp)
        console.log(resp)
        const diameter_select = $('#input-arm-diameter')
        const braid_select = $('#input-arm-braid')
        const vendor_select = $('#input-arm-vendor')
        diameter_select.empty().append(new Option("Выберите диаметр", ""));
        braid_select.empty().append(new Option("Выберите оплетку", ""));
        vendor_select.empty().append(new Option("Выберите производителя", ""));
        var offer = createUniqueArmOffer(resp)
        let selection = resp['selection']['arm']
        offer[0].forEach((diameter) => {
            diameter_select.append(new Option(diameter + ' мм', diameter));
        })
        offer[1].forEach((braid) => {
            braid_select.append(new Option(braid, braid));
        })
        offer[2].forEach((vendor) => {
            vendor_select.append(new Option(vendor, vendor));
        })
        if (selection['diameter'] !== undefined) {
            $("#input-arm-diameter option:last").attr("selected", "selected");
        }
        if (selection['braid'] !== undefined) {
            $("#input-arm-braid option:last").attr("selected", "selected");
        }
        if (selection['vendor'] !== undefined) {
            $("#input-arm-vendor option:last").attr("selected", "selected");
        }

        document.getElementById('input-arm-diameter').fstdropdown.rebind()
        document.getElementById('input-arm-vendor').fstdropdown.rebind()
        document.getElementById('input-arm-braid').fstdropdown.rebind()
    })

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
    let vendors = []
    dict['arms'].forEach((arm) => {
        let diameter = arm['diameter']
        let braid = arm['braid']
        let vendor = arm['vendor']
        if ($.inArray(diameter, diameters) === -1) {
            diameters.push(diameter);
        }
        if ($.inArray(braid, braids) === -1) {
            braids.push(braid);
        }
        if ($.inArray(vendor, vendors) === -1) {
            vendors.push(vendor);
        }
    })
    return [diameters, braids, vendors]
}

async function send(endpoint, data) {
    if (data === undefined)
        data = []
    var request = {"data": JSON.stringify(data), "sid": sid}
    console.log(sid)
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