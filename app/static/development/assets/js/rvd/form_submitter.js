'use strict'

window.addEventListener("load", init);
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

let selection_items = []

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
    // as = $('#arm_section');
    // fs = $('#fiting_section');
    // fs1 = $('#fiting_1_section');
    // fs2 = $('#fiting_2_section');
    // as.on('change', submitArm);
    // fs1.on('change', submitFits);
    // fs2.on('change', submitFits);
    console.log('cw ended')
    defineSections();
    // updateArmSection();
    // updateFitSections();
    update_cart();
    init_sessions();
    if (current_part !== undefined) {
        render_parts({'current_part': current_part})
    }
}


// function submitArm() {
//     let formRes = as.serializeArray()
//     formRes.forEach(i => {
//         let val = tryParseFloat(i.value)
//         if (i.value !== "")
//             current_selection["items"]["arm"][i.name] = val
//         else
//             delete current_selection["items"]["arm"][i.name]
//         if (i.name === "diameter") {
//             current_selection["items"]["clutch1"] = {'diameter': val}
//             current_selection["items"]["clutch2"] = {'diameter': val}
//         }
//
//     })
//     writeToSession(sid, current_selection).then(() => {
//         getCurrentSelection().then(() => {
//             updateArmSection()
//             updateFitSections()
//         })
//     })
// }

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
    // writeToSession(sid, current_selection).then(() => getCurrentSelection().then(() => updateFitSections()))
}

function dropArm() {
    current_selection["items"]["arm"] = {}
    current_selection["items"]["clutch1"] = {}
    current_selection["items"]["clutch2"] = {}

    // let resp = writeToSession(sid, current_selection).then(() => getCurrentSelection().then(() => updateArmSection()))
}

function dropFits() {
    current_selection["items"]["fiting1"] = {}
    current_selection["items"]["fiting2"] = {}

    // let resp = writeToSession(sid, current_selection).then(() => getCurrentSelection().then(() => updateFitSections()))
}

function dropClutches() {
    current_selection["items"]["clutch1"] = {}
    current_selection["items"]["clutch2"] = {}

    // writeToSession(sid, current_selection).then(() => getCurrentSelection().then(() => updateFitSections()))
}

function writeToSession(sid, data) {
    return request("/api/make_order/update_selection_items", data)
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

async function getCurrentSelection() {
    let only_present = $('#rvd_only_present').is(':checked')
    let resp = await request('/api/make_order/get_offer', {'only_present': only_present});
    if (resp !== 'NaN') {
        current_selection = resp['selection']
        parameters = resp['parameters']
        candidates = resp['candidates']
        current_offer = resp
        current_part = current_selection['part']
    }
    updateSelectionSubtotal()
    return resp;
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
        '<input class="form-control form-control-sm" id="subtotal_amount" onchange="changeSelectAmount()" type="number" placeholder="количество" value="' + amount + '">\n' +
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
    getCurrentSelection().then(updateSections)
}

function addToCart() {
    send("/api/make_order/submit_selection", {'sid': sid}).then(
        (ans) => {
            if (ans === 'success') {
                updateAllSections()
                $('#addModal').modal('hide');
            }
            update_cart();
        }
    );
}

function submitSelection() {
    let data = {}
    for (const item of selection_items) {
        let key = item[0]
        let value = item[1]
        data[key] = value.collectData();
    }
    current_selection['items'] = data;
    console.log(current_selection)
    return send("/api/make_order/update_selection_items", current_selection).then(updateAllSections)
}

function updateSections(data) {
    console.log(data)
    let select = data['selection']['items']
    for (const item of selection_items) {
        let key = item[0]
        let value = item[1]
        if (select[key] !== undefined)
            value.setData(data);
    }
}

const selectionModalParentId = 'rvd-modal-body';
const selectionModalParent = $('#' + selectionModalParentId);

function addSection() {
    let section_type_s = $('#input-section-type').val()
    let section_type = getSectionType(section_type_s)
    let num = getLastSectionNum() + 1
    let section_id = `${section_type_s}-form-${num}`
    const sec = new section_type({}, section_id, selectionModalParentId, num)
    console.log(sec)
    selection_items.push([section_id, sec])
    selectionModalParent.append(sec.HTML)
    sec.setName(`${sec.readable_name} ${sec.num}`)
    setFstDropdown()
    $(`#${section_id}`).on('change', submitSelection);
    submitSelection()
}

function getSectionType(type) {
    let section_type = ArmSection
    if (type === '') {
        alert('Выберите секцию')
        return
    } else {
        switch (type) {
            case 'arm':
                section_type = ArmSection
                break
            case 'fiting':
                section_type = FitingSection
                break
            case 'clutch':
                section_type = ClutchSection
                break
        }
    }
    return section_type;
}

function defineSections() {
    getCurrentSelection().then((resp) => {
        selection_items = []
        for (const [key, val] of Object.entries(current_selection['items'])) {
            let section_type = getSectionType(val['type'])
            let n = parseInt(key.substring(key.lastIndexOf("-") + 1))
            const sec = new section_type({}, key, selectionModalParentId, n)
            sec.setData(resp)
            selection_items.push([key, sec])
        }
        selection_items.sort(function (first, second) {
            return first[1].num - second[1].num;
        });
        console.log(selection_items)
        createSections();
        console.log("sections created")

    })
}


function createSections() {
    selectionModalParent.empty()
    for (const item of selection_items) {
        let key = item[0]
        let value = item[1]
        selectionModalParent.append(value.HTML)
        setFstDropdown();
        value.updateData();
        $(`#${key}`).on('change', submitSelection);
    }
}

function getLastSectionNum() {
    return selection_items.length;
}

function dropSection(sectionId) {
    current_selection['items'][sectionId] = {'type': current_selection['items'][sectionId]['type'],
    'part_name': current_selection['items'][sectionId]['part_name']}
    send("/api/make_order/update_selection_items", current_selection).then(updateAllSections)
}

function deleteSection(sectionId) {
    delete current_selection['items'][sectionId]
    send("/api/make_order/update_selection_items", current_selection).then(defineSections)
}

class BasicSection {
    type = "Base";
    readable_name = "База"
    static template = ``;

    constructor(data, id, parentBlockId, num = 1) {
        this.num = num
        this.data = data
        this.id = id
        this.parentId = parentBlockId
    }

    get HTML() {
        return String.raw``;
    }

    setData(data) {
        this.data = data
        if (document.getElementById(this.id) !== null)
            this.updateData()
    }

    updateData() {

    }


    collectData() {
        const form = $('#' + this.id)
        let res = form.serializeArray()
        return formToDict(res)
    }

    setName(name) {
        console.log(name)
        $(`#${this.id}_input-part-name`).val(name)
    }
}

class FitingSection extends BasicSection {
    type = 'fiting';
    readable_name = "Фитинг"

    constructor(data, id, parentBlockId, num) {
        super(data, id, parentBlockId, num);
    }

    updateData() {
        let resp = this.data;
        const type_select = $(`#${this.id}_input-fit-type`)
        const carving_select = $(`#${this.id}_input-fit-carving`)
        const angle_select = $(`#${this.id}_input-fit-angle`)
        const fit_select = $(`#${this.id}_input-fit`)
        const part_name = $(`#${this.id}_input-part-name`)
        type_select.empty().append(new Option("Выберите тип", ""));
        carving_select.empty().append(new Option("Выберите резьбу", ""));
        angle_select.empty().append(new Option("Выберите угол", ""));
        fit_select.empty().append(new Option("Выберите фитинг", ""));
        let offer = resp['parameters'][this.id]
        let selection = current_selection["items"][this.id]
        if (selection === undefined) {
            selection = {}
        }
        if (selection['part_name'] !== undefined) {
            part_name.val(selection['part_name'])
        } else {
            part_name.val('');
        }
        for (const type of offer['fiting_type'] || []) {
            type_select.append(new Option(type, type));
        }
        for (const carving of offer['carving'] || []) {
            carving_select.append(new Option(carving, carving));
        }
        for (const angle of offer['angle'] || []) {
            angle_select.append(new Option(angle, angle));
        }
        for (const fiting of resp['candidates'][this.id] || []) {
            fit_select.append(new Option(`${fiting['name']}: ${fiting['amount']}`, fiting['_id']));
        }
        if (selection['fiting_type'] !== undefined) {
            $(`#${this.id}_input-fit-type` + " option:last").attr("selected", "selected");
        }
        if (selection['carving'] !== undefined) {
            $(`#${this.id}_input-fit-carving` + " option:last").attr("selected", "selected");
        }
        if (selection[`angle`] !== undefined) {
            $(`#${this.id}_input-fit-angle` + " option:last").attr("selected", "selected");
        }
        if (selection['id'] !== undefined) {
            $(`#${this.id}_input-fit` + " option:last").attr("selected", "selected");
        }

        document.getElementById(`${this.id}_input-fit-type`).fstdropdown.rebind()
        document.getElementById(`${this.id}_input-fit-carving`).fstdropdown.rebind()
        document.getElementById(`${this.id}_input-fit-angle`).fstdropdown.rebind()
        document.getElementById(`${this.id}_input-fit`).fstdropdown.rebind()
    }

    get HTML() {
        return `<form id="${this.id}">\n` +
            `  <input type="hidden" name="type" value="${this.type}">\n` +
            `  <div class="d-inline-flex  mb-2"><h6 class="heading-small w-100">Выбор фитинга</h6>\n` +
            `    <input name="part_name" id="${this.id}_input-part-name" class="form-control form-control-sm ml-1" type="text"\n` +
            `           placeholder="Фитинг N"></div>\n` +
            `  <div class="d-flex">\n` +
            `    <div class="d-flex form-group col">\n` +
            `      <label class="form-control-label p-2" for="${this.id}_input-fit-type">Тип</label>\n` +
            `      <select name="fiting_type" class="form-control form-control-sm fstdropdown-select" id="${this.id}_input-fit-type">\n` +
            `        <option value="">Выберите стандарт фитинга</option>\n` +
            `        <option value="1">DK</option>\n` +
            `        <option value="2">DKI</option>\n` +
            `      </select>\n` +
            `    </div>\n` +
            `    <div class="d-flex form-group col">\n` +
            `      <label class="form-control-label p-2" for="${this.id}_input-fit-carving">Резьба</label>\n` +
            `      <select name="carving" class="form-control form-control-sm fstdropdown-select" id="${this.id}_input-fit-carving">\n` +
            `        <option value="">Выберите резьбу</option>\n` +
            `        <option value="1">6</option>\n` +
            `        <option value="2">8</option>\n` +
            `      </select>\n` +
            `    </div>\n` +
            `  </div>\n` +
            '  <div class="d-flex">' +
            `    <div class="d-flex form-group col">\n` +
            `      <label class="form-control-label p-2" for="${this.id}_input-angle">Угол</label>\n` +
            `      <select name="angle" class="form-control form-control-sm fstdropdown-select" id="${this.id}_input-fit-angle">\n` +
            `        <option value="">Выберите угол</option>\n` +
            `        <option value="1">DK 2x03</option>\n` +
            `        <option value="2">DK 2x06</option>\n` +
            `      </select>\n` +
            `    </div>\n` +
            `  <div class="d-flex form-group col">\n` +
            `    <label class="form-control-label p-2" for="${this.id}_input-fit">Фитинг</label>\n` +
            `    <select name="id" class="form-control form-control-sm fstdropdown-select" id="${this.id}_input-fit">\n` +
            `      <option value="">Выберите фитинг</option>\n` +
            `      <option value="1">Муфта 2x03</option>\n` +
            `      <option value="2">Муфта 2x06</option>\n` +
            `    </select>\n` +
            `  </div>\n` +
            ' </div>' +
            `</form>\n` +
            `          <div class="d-flex text-left">\n` +
            `            <a href="#!" onclick="dropSection('${this.id}')" class="btn btn-sm btn-primary">Сбросить деталь</a>\n` +
            `            <a href="#!" onclick="deleteSection('${this.id}')" class="btn btn-sm btn-primary">Удалить запчасть</a>\n` +
            `          </div>` +
            `<hr/>`
    }
}

class ClutchSection extends BasicSection {
    type = 'clutch';
    readable_name = "Муфта"

    constructor(data, id, parentBlockId, num) {
        super(data, id, parentBlockId, num);
    }

    updateData() {
        let resp = this.data;
        const part_name = $(`#${this.id}_input-part-name`)
        const clutch_select = $(`#${this.id}_input-clutch`)
        clutch_select.empty().append(new Option("Выберите муфту", ""));
        let selection = current_selection["items"][this.id]
        if (selection === undefined) {
            selection = {}
        }
        if (selection['part_name'] !== undefined) {
            part_name.val(selection['part_name'])
        } else {
            part_name.val('');
        }
        for (const clutch of resp['candidates'][this.id] || []) {
            clutch_select.append(new Option(`${clutch['name']}: ${clutch['amount']}`, clutch['_id']));
        }
        if (selection[`id`] !== undefined) {
            $(`#${this.id}_input-clutch` + " option:last").attr("selected", "selected");
        }

        document.getElementById(`${this.id}_input-clutch`).fstdropdown.rebind()
    }

    get HTML() {
        return `<form id="${this.id}">\n` +
            `  <input type="hidden" name="type" value="${this.type}">\n` +
            `  <div class="d-inline-flex  mb-2"><h6 class="heading-small w-100">Выбор муфты</h6>\n` +
            `    <input name="part_name" id="${this.id}_input-part-name" class="form-control form-control-sm ml-1" type="text"\n` +
            `           placeholder="Муфта N"></div>\n` +
            `  <div class="d-flex form-group col">\n` +
            `    <label class="form-control-label text-nowrap p-2" for="${this.id}_input-clutch">Муфта</label>\n` +
            `    <select name="id" class="form-control form-control-sm fstdropdown-select" id="${this.id}_input-clutch">\n` +
            `      <option value="">Выберите муфту</option>\n` +
            `      <option value="1">Муфта 2x03</option>\n` +
            `      <option value="2">Муфта 2x06</option>\n` +
            `    </select>\n` +
            `  </div>\n` +
            `</form>\n` +
            `          <div class="d-flex text-left">\n` +
            `            <a href="#!" onclick="dropSection('${this.id}')" class="btn btn-sm btn-primary">Сбросить муфту</a>\n` +
            `            <a href="#!" onclick="deleteSection('${this.id}')" class="btn btn-sm btn-primary">Удалить запчасть</a>\n` +
            `          </div>` +
            `<hr/>`
    }
}


class ArmSection extends BasicSection {
    type = 'arm';
    readable_name = "Рукав"

    constructor(data, id, parentBlockId, num) {
        super(data, id, parentBlockId, num);
    }


    updateData() {
        let resp = this.data;
        let selection = resp['selection']["items"][this.id]
        const diameter_select = $(`#${this.id}_input-arm-diameter`)
        const type_select = $(`#${this.id}_input-arm-type`)
        const length_select = $(`#${this.id}_input-arm-length`)
        const arm_select = $(`#${this.id}_input-arm`)
        const part_name = $(`#${this.id}_input-part-name`)
        diameter_select.empty().append(new Option("Выберите диаметр", ""));
        type_select.empty().append(new Option("Выберите тип рукава", ""));
        arm_select.empty().append(new Option("Выберите рукав", ""));
        let offer = resp['parameters'][this.id]
        if (selection === undefined) {
            selection = {}
        }
        if (selection['amount'] !== undefined) {
            length_select.val(selection['amount'])
        } else {
            length_select.val(0);
        }
        if (selection['part_name'] !== undefined) {
            part_name.val(selection['part_name'])
        } else {
            part_name.val('');
        }
        for (const type of offer['arm_type'] || []) {
            type_select.append(new Option(type, type));
        }
        for (const diameter of offer['diameter'] || []) {
            diameter_select.append(new Option(diameter + ' мм', diameter));
        }
        for (const arm of resp['candidates'][this.id] || []) {
            arm_select.append(new Option(`${arm['name']}: ${arm['amount']}`, arm['_id']));
        }
        if (selection['diameter'] !== undefined) {
            $(`#${this.id}_input-arm-diameter option:last`).attr("selected", "selected");
        }
        if (selection['braid'] !== undefined) {
            $(`#${this.id}_input-arm-braid option:last`).attr("selected", "selected");
        }
        if (selection['arm_type'] !== undefined) {
            $(`#${this.id}_input-arm-type option:last`).attr("selected", "selected");
        }
        if (selection['id'] !== undefined) {
            $(`#${this.id}_input-arm option:last`).attr("selected", "selected");
        }
        // console.log('rebinding')
        document.getElementById(`${this.id}_input-arm-diameter`).fstdropdown.rebind()
        document.getElementById(`${this.id}_input-arm-type`).fstdropdown.rebind()
        document.getElementById(`${this.id}_input-arm`).fstdropdown.rebind()
    }


    get HTML() {
        return `<form id="${this.id}">\n` +
            `<input type="hidden" name="type" value="${this.type}">` +
            `<div class="d-inline-flex mb-2"><h6 class="heading-small w-100">Выбор рукава</h6><input name="part_name" id="${this.id}_input-part-name" class="form-control form-control-sm ml-1" type="text" placeholder="Рукав N"></div>\n` +
            '<div class="pl-lg-4">\n' +
            `  <div class="row">\n` +
            `    <div class="col-lg-6">\n` +
            `      <div class="d-flex form-group">\n` +
            `        <label class="form-control-label text-nowrap p-2" for="${this.id}_input-arm-diameter">Диаметр</label>\n` +
            `        <select name="diameter" class="form-control form-control-sm fstdropdown-select" id="${this.id}_input-arm-diameter">\n` +
            `          <option value="">Выберите диаметр</option>\n` +
            `        </select>\n` +
            `      </div>\n` +
            `    </div>\n` +
            `    <div class="col-lg-6">\n` +
            `      <div class="d-flex form-group">\n` +
            `        <label class="form-control-label text-nowrap p-2" for="${this.id}_input-arm-type">Тип рукава</label>\n` +
            `        <select name="arm_type" class="form-control form-control-sm fstdropdown-select" id="${this.id}_input-arm-type">\n` +
            `          <option value="">Выберите тип рукава</option>\n` +
            `        </select>\n` +
            `      </div>\n` +
            `    </div>\n` +
            `  </div>\n` +
            `  <div class="row">\n` +
            `    <div class="col-lg-6">\n` +
            `      <div class="d-flex form-group">\n` +
            `        <label class="form-control-label text-nowrap p-2" for="${this.id}_input-length">Длина рукава (м)</label>\n` +
            `        <input name="amount" id="${this.id}_input-arm-length" class="form-control form-control-sm" type="number" placeholder="1">\n` +
            `      </div>\n` +
            `    </div>\n` +
            `    <div class="col-lg-6">\n` +
            `  <div class="d-flex form-group">\n` +
            `    <label class="form-control-label text-nowrap p-2" for="${this.id}_input-arm">Рукав</label>\n` +
            `    <select name="id" class="fstdropdown-select form-control form-control-sm" id="${this.id}_input-arm">\n` +
            `      <option value="">Выберите рукав</option>\n` +
            `    </select>\n` +
            `  </div>\n` +
            `</div>` +
            `  </div>\n` +
            `</form>` +
            `          <div class="d-flex text-left">\n` +
            `            <a href="#!" onclick="dropSection('${this.id}')" class="btn btn-sm btn-primary">Сбросить рукав</a>\n` +
            `            <a href="#!" onclick="deleteSection('${this.id}')" class="btn btn-sm btn-primary">Удалить запчасть</a>\n` +
            `          </div>` +
            `<hr/>`
    }
}

