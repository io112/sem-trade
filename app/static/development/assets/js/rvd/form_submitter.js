'use strict'

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
    init_cw()
    defineSections();
    update_cart();
    init_sessions();
    if (current_part !== undefined) {
        render_parts({'current_part': current_part})
    }
}

function writeToSession(sid, data) {
    return send("/api/bp/update_selection_items", data)
}


async function getCurrentSelection() {
    let only_present = $('#rvd_only_present').is(':checked')
    let resp = await request('/api/bp/get_offer', {'only_present': only_present});
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


function changeSubtotal() {
    current_selection["subtotal"]["amount"] = parseInt($('#subtotal_amount').val());
    current_selection["subtotal"]["job_type"] = $('#input-job-type').val();
    writeToSession(sid, current_selection).then(() => {
        getCurrentSelection()
    })

}

function updateSelectionSubtotal() {
    let name = current_selection["subtotal"]["name"]
    let price = current_selection["subtotal"]["price"]
    let amount = current_selection["subtotal"]["amount"]
    let total_price = current_selection["subtotal"]["total_price"]
    // $('#input-job-type').val(current_selection["subtotal"]["job_type"])
    if (current_selection["subtotal"]["job_type"])
        $(`#input-job-type option[value=${current_selection["subtotal"]["job_type"]}]`).attr("selected", "selected");
    document.getElementById('input-job-type').fstdropdown.rebind()
    $('#select_subtotal tbody').empty().append('<tr>\n' +
        '<td>\n' +
        '<span class="name mb-0 text-sm">' + name + '</span>\n' +
        '</td>\n' +
        '<td class="number">\n' +
        '<input class="form-control form-control-sm" id="subtotal_amount" onchange="changeSubtotal()" type="number" placeholder="количество" value="' + amount + '">\n' +
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
    getCurrentSelection().then(defineSections)
}

function addToCart() {
    send("/api/bp/submit_selection", {'sid': sid}).then(
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
    return send("/api/bp/update_selection_items", current_selection).then(updateAllSections)
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
            case 'pipe':
                section_type = PipeSection
                break
            case 'service':
                section_type = ServiceSection
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
    current_selection['items'][sectionId] = {
        'type': current_selection['items'][sectionId]['type'],
        'part_name': current_selection['items'][sectionId]['part_name']
    }
    send("/api/bp/update_selection_items", current_selection).then(updateAllSections)
}

function deleteSection(sectionId) {
    delete current_selection['items'][sectionId]
    send("/api/bp/update_selection_items", current_selection).then(defineSections)
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

        const part_name = $(`#${this.id}_input-part-name`)
        let selection = current_selection["items"][this.id] || {}
        let offer = resp['parameters'][this.id]
        const amount_select = $(`#${this.id}_input-fiting-amount`)
        amount_select.val(selection['amount'] || 1)
        part_name.val(selection['part_name'] || '')


        updateSelect(`${this.id}_input-fit-type`, "Выберите тип", offer['fiting_type'],
            offer['fiting_type'], "", selection['fiting_type'] !== undefined)

        updateSelect(`${this.id}_input-fit-carving`, "Выберите резьбу", offer['carving'],
            offer['carving'], "", selection['carving'] !== undefined)

        updateSelect(`${this.id}_input-fit-angle`, "Выберите угол", offer['angle'],
            offer['angle'], "", selection['angle'] !== undefined)

        updateIdSelect(`${this.id}_input-fit`, "Выберите фитинг", resp['candidates'][this.id], "",
            selection['id'] !== undefined)
    }

    get HTML() {
        return `<form id="${this.id}">\n` +
            `  <input type="hidden" name="type" value="${this.type}">\n` +
            `  <div class="d-inline-flex  mb-2"><h6 class="heading-small w-100">Выбор фитинга</h6>\n` +
            `    <input name="part_name" id="${this.id}_input-part-name" class="form-control form-control-sm ml-1" type="text"\n` +
            `           placeholder="Фитинг N">` +
            `        <label class="form-control-label text-nowrap p-2 ml-2" for="${this.id}_input-fiting-amount">количество</label>` +
            `        <input name="amount" id="${this.id}_input-fiting-amount" class="form-control form-control-sm" type="number" placeholder="1">` +
            `</div>\n` +
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
        let selection = current_selection["items"][this.id] || {}
        const part_name = $(`#${this.id}_input-part-name`)
        const amount_select = $(`#${this.id}_input-clutch-amount`)
        amount_select.val(selection['amount'] || 1)
        part_name.val(selection['part_name'] || '')

        updateIdSelect(`${this.id}_input-clutch`, "Выберите муфту", resp['candidates'][this.id], "",
            selection['id'] !== undefined)
    }

    get HTML() {
        return `<form id="${this.id}">\n` +
            `  <input type="hidden" name="type" value="${this.type}">\n` +
            `  <div class="d-inline-flex  mb-2"><h6 class="heading-small w-100">Выбор муфты</h6>\n` +
            `    <input name="part_name" id="${this.id}_input-part-name" class="form-control form-control-sm ml-1" type="text"\n` +
            `           placeholder="Муфта N">` +
            `        <label class="form-control-label text-nowrap p-2 ml-2" for="${this.id}_input-clutch-amount">Количество</label>` +
            `        <input name="amount" id="${this.id}_input-clutch-amount" class="form-control form-control-sm" type="number" placeholder="1">` +
            `</div>\n` +
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


class ServiceSection extends BasicSection {
    type = 'service';
    readable_name = "Услуга"

    constructor(data, id, parentBlockId, num) {
        super(data, id, parentBlockId, num);
    }

    updateData() {
        let resp = this.data;
        let selection = current_selection["items"][this.id] || {}

        const part_name = $(`#${this.id}_input-part-name`)
        const amount_select = $(`#${this.id}_input-service-amount`)
        amount_select.val(selection['amount'] || 0)
        part_name.val(selection['part_name'] || '')

    }

    get HTML() {
        return `<form id="${this.id}">\n` +
            `  <input type="hidden" name="type" value="${this.type}">\n` +
            `  <div class="d-inline-flex  mb-2"><h6 class="heading-small w-100">Выбор услуги</h6>\n` +
            `</div>\n` +
            `  <div class="d-flex">\n` +
            `        <label class="form-control-label text-nowrap p-2 ml-2" for="${this.id}_input-part-name">Название</label>` +
            `    <input name="part_name" id="${this.id}_input-part-name" class="form-control form-control-sm ml-1" type="text"\n` +
            `           placeholder="Трубка N">` +
            `        <label class="form-control-label text-nowrap p-2 ml-2" for="${this.id}_input-service-amount">Стоимость</label>` +
            `        <input name="amount" id="${this.id}_input-service-amount" class="form-control form-control-sm" type="number" placeholder="1">` +
            `  </div>\n` +
            `</form>\n` +
            `          <div class="d-flex text-left">\n` +
            `            <a href="#!" onclick="dropSection('${this.id}')" class="btn btn-sm btn-primary">Сбросить услугу</a>\n` +
            `            <a href="#!" onclick="deleteSection('${this.id}')" class="btn btn-sm btn-primary">Удалить услугу</a>\n` +
            `          </div>` +
            `<hr/>`
    }
}


class PipeSection extends BasicSection {
    type = 'pipe';
    readable_name = "Трубка"

    constructor(data, id, parentBlockId, num) {
        super(data, id, parentBlockId, num);
    }

    updateData() {
        let resp = this.data;
        let offer = resp['parameters'][this.id]
        let selection = current_selection["items"][this.id] || {}

        const part_name = $(`#${this.id}_input-part-name`)
        const amount_select = $(`#${this.id}_input-pipe-amount`)
        amount_select.val(selection['amount'] || 1)
        part_name.val(selection['part_name'] || '')


        updateSelect(`${this.id}_input-pipe-size`, "Выберите размер", offer['size'],
            offer['size'], "", selection['size'] !== undefined)

        updateIdSelect(`${this.id}_input-pipe`, "Выберите трубку", resp['candidates'][this.id], "",
            selection['id'] !== undefined)

    }

    get HTML() {
        return `<form id="${this.id}">\n` +
            `  <input type="hidden" name="type" value="${this.type}">\n` +
            `  <div class="d-inline-flex  mb-2"><h6 class="heading-small w-100">Выбор трубки</h6>\n` +
            `    <input name="part_name" id="${this.id}_input-part-name" class="form-control form-control-sm ml-1" type="text"\n` +
            `           placeholder="Трубка N">` +
            `        <label class="form-control-label text-nowrap p-2 ml-2" for="${this.id}_input-pipe-amount">Длина (м)</label>` +
            `        <input name="amount" id="${this.id}_input-pipe-amount" class="form-control form-control-sm" type="number" placeholder="1">` +
            `</div>\n` +
            `  <div class="d-flex">\n` +
            `  <div class="d-flex form-group col">\n` +
            `    <label class="form-control-label text-nowrap p-2" for="${this.id}_input-pipe-size">Трубка</label>\n` +
            `    <select name="size" class="form-control form-control-sm fstdropdown-select" id="${this.id}_input-pipe-size">\n` +
            `      <option value="">Выберите размер</option>\n` +
            `    </select>\n` +
            `  </div>\n` +
            `  <div class="d-flex form-group col">\n` +
            `    <label class="form-control-label text-nowrap p-2" for="${this.id}_input-pipe">Трубка</label>\n` +
            `    <select name="id" class="form-control form-control-sm fstdropdown-select" id="${this.id}_input-pipe">\n` +
            `      <option value="">Выберите трубку</option>\n` +
            `    </select>\n` +
            `  </div>\n` +
            '</div>' +
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
        let selection = current_selection["items"][this.id] || {}
        const length_select = $(`#${this.id}_input-arm-length`)
        const part_name = $(`#${this.id}_input-part-name`)
        let offer = resp['parameters'][this.id]
        length_select.val(selection['amount'] || 0)
        part_name.val(selection['part_name'] || '')

        updateSelect(`${this.id}_input-arm-type`, "Выберите тип", offer['arm_type'],
            offer['arm_type'], "", selection['arm_type'] !== undefined)
        updateSelect(`${this.id}_input-arm-diameter`, "Выберите диаметр", offer['diameter'],
            offer['diameter'], " мм", selection['diameter'] !== undefined)
        updateIdSelect(`${this.id}_input-arm`, "Выберите рукав", resp['candidates'][this.id], "",
            selection['id'] !== undefined)

    }


    get HTML() {
        return `<form id="${this.id}">\n` +
            `<input type="hidden" name="type" value="${this.type}">` +
            `<div class="d-inline-flex align-items-center mb-2"><h6 class="heading-small text-nowrap p-2">Выбор рукава</h6><input name="part_name" id="${this.id}_input-part-name" class="form-control form-control-sm ml-1" type="text" placeholder="Рукав N">` +
            `</div>\n` +
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

function updateSelect(id, optionName, visibleList, optionList, nameAppendix, isSelected) {
    visibleList = visibleList || []
    const select = $(`#${id}`)
    select.empty().append(new Option(optionName, ""));

    for (let i = 0; i < visibleList.length; i++) {
        select.append(new Option(`${visibleList[i]}${nameAppendix}`, optionList[i]));
    }

    if (isSelected) {
        $(`#${id} option:last`).attr("selected", "selected");
    }

    document.getElementById(id).fstdropdown.rebind()
}

function updateIdSelect(id, optionName, candidatesList, nameAppendix, isSelected) {
    let res = []
    let options = []
    for (const candidate of candidatesList) {
        res.push(`${candidate['name']}: ${candidate['amount']}`)
        options.push(candidate['_id'])
    }
    updateSelect(id, optionName, res, options, nameAppendix, isSelected)
}