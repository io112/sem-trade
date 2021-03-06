let is_org_slider = ""

// ENDPOINTS
const get_carts_endpoint = 'api/make_order/get_carts'
const get_cart_endpoint = '/api/make_order/get_cart'
const find_contragents_endpoint = 'api/contragent/find_contragents'
const remove_contragent_endpoint = 'api/make_order/remove_contragent'
const set_contragent_endpoint = 'api/make_order/set_contragent'
const get_contragent_endpoint = 'api/make_order/get_contragent'
const cancel_order_endpoint = 'api/make_order/cancel'
const del_cart_item_endpoint = 'api/make_order/del_cart_item'
const create_contragent_endpoint = 'api/contragent/create_contragent'
const set_comment_endpoint = 'api/make_order/set_comment'
const get_comment_endpoint = 'api/make_order/get_comment'
const checkout_endpoint = 'api/make_order/checkout'

let current_part = undefined

function init_cw() {
    is_org_slider = $('#contragent_is_org');
    $('#comment_text').on('blur', set_comment);
    $('#checkout_btn').on('click', checkout);
    is_org_slider.on('change', change_contragent_type);
    get_contragent();
    render_comment();
}

var saveData = (function () {
    var a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    return function (fileName, blob) {
        var url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
    };
}());


function find_part() {
    let form_data = $('#part_form').serializeArray()
    request('/api/make_order/find_part', form_data).then(resp => render_parts(resp))

}

function submit_part() {
    update_part()
    send('/api/make_order/submit_part').then((resp) => {
        if (resp === 'success') {
            current_part = undefined
            render_parts(current_part)
            $('#addPartModal').modal('hide');
            update_cart();
        }
    })

}

function render_parts(list) {
    const parts_list = $('#parts_list')
    if (list === undefined) {
        parts_list.empty()
        $('#part_price').html(0)
        $('#part_total').html(0)
        $('#part-input-amount').val(0)
        $('#part_search').show()
        return;
    }
    console.log(list)
    parts_list.empty();
    if (list['current_part']) {
        $('#part_search').hide()
        let part = list['current_part']
        let item = part['item']
        console.log(part)
        parts_list.append(get_part(item['name'], item['amount'], item['_id'], true, item['type']))
        $('#part_price').html(part['price'])
        $('#part_total').html(part['total_price'])
        $('#part-input-amount').val(part['amount'])
        return
    }
    if (list['items'] === undefined)
        return
    list['items'].forEach(part => {
        parts_list.append(get_part(part['name'], part['amount'], part['_id'], false, part['type']))
    })
}

function get_part(name, amount, id, is_selected, type) {
    name = `${name} : ${amount}`
    return `<a href="#!" onclick="set_part('${id}', '${type}')" class="list-group-item list-group-item-action ${is_selected ? 'active' : ''}" aria-current="true">
              ${name}
            </a>`
}

function clear_part() {
    current_part = undefined
    send('/api/make_order/clear_part').then(res => {
        console.log(res)
        if (res === 'success') {
            render_parts(current_part)
        }
    })
}

function update_part() {
    if (current_part !== undefined)
        set_part(current_part['item']['_id'], current_part['item']['type'])
}

function set_part(id, collection) {
    let req = {
        'collection': collection, 'part_id': id,
        'amount': tryParseFloat($('#part-input-amount').val())
    }
    send('/api/make_order/set_part', req).then(resp => {
        console.log(resp)
        current_part = resp['current_part']
        render_parts(resp)
    })
}

function checkout() {
    set_comment();
    // fetch(checkout_endpoint, {
    //     method: 'POST',
    //     body: JSON.stringify({'sid': sid})
    // })
    //     .then(resp => resp.blob()).then(blob => {
    //     saveData('orders.xml', blob)
    // })

    send(checkout_endpoint).then(resp => {
        console.log(resp.status)
        if (!resp.status || resp.status === 200) {
            window.location.href = '/'
        }
    })

}

function set_comment() {
    send(set_comment_endpoint, $('#comment_text').val()).then()
}

function render_comment() {
    send(get_comment_endpoint).then(comment => {
        console.log(comment)
        $('#comment_text').val(comment)
    })
}

function init_sessions() {
    get_sessions()
}

function get_sessions() {
    request(get_carts_endpoint, {'sorting': '+last_modified'}).then(carts => {
        render_changer(carts)
    })
}

function render_changer(data) {
    data = data['data']
    const nav = $('#nav-pager')
    nav.empty()
    const list = $('<ul>').attr('class', 'pagination pagination-lg')
    let i = 1
    data.forEach(btn => {
        let btn_sid = btn['_id']
        let is_active = btn_sid === sid;
        list.append(get_btn(btn_sid, i, is_active))
        i += 1
    })
    list.append(get_btn('', '+', false))
    nav.append(list)
}

function get_btn(link, text, is_active) {
    let classes = 'page-item'
    if (is_active)
        classes += ' active'
    return `<li class="${classes}">` +
        `<a class="page-link" href="/?sid=${link}">${text}</a>` +
        '</li>'

}

function change_contragent_type() {
    if ($('#contragent_is_org').is(':checked')) {
        $('#contragent_surname_block').hide()
        $('#contragent_surname').val('')
        $('#contragent_kpp_block').show()
        $('#contragent_inn_block').show()
    } else {
        $('#contragent_surname_block').show()
        $('#contragent_inn_block').hide()
        $('#contragent_inn').val('')
        $('#contragent_kpp_block').hide()
        $('#contragent_kpp').val('')
    }
}

async function get_cart() {
    return await send(get_cart_endpoint)
}

function update_cart() {
    get_cart().then(render_cart)
}

function render_cart(cart) {
    const cart_table = $('#items_list tbody')
    console.log(cart)
    cart_table.empty()
    let items = cart['items']
    let subtotal = cart['subtotal']

    let i = 0
    items.forEach(item => {
        // item = item[Object.keys(item)[0]]
        cart_table.append(get_items_table_row(i, item['name'], item['amount'],
            item['price'], item['total_price']));
        i++;
    })
    $('#cart_total').text(subtotal)

}

let clients_fixture = [{
    'id': '1',
    'name': 'test1',
    'surname': 'test4',
    'phone': '+71234567890',
    'is_org': false
}, {
    'id': '2',
    'name': 'test2',
    'phone': '+71234561234',
    'is_org': true
},
]

function update_clients() {
    send(find_contragents_endpoint, $('#input-clientname').val()).then(
        res => {
            render_clients(res)
        }
    )
}

function remove_contragent() {
    send(remove_contragent_endpoint).then(resp => {
        render_contragent(resp)
    })
}

function set_contragent(id) {
    send(set_contragent_endpoint, id).then(resp => {
        render_contragent(resp)
    })
}

function get_contragent() {
    send(get_contragent_endpoint).then(resp => {
        render_contragent(resp)
    })
}

function render_contragent(resp) {
    const inp = $('#input-clientname')
    const checkout_field = $('#client_name')
    if (Object.keys(resp).length !== 0) {
        let name = resp['name']
        if (!resp['is_org'])
            name += ' ' + resp['surname']
        inp.val(name)
        inp.prop('disabled', true)
        checkout_field.html(name)
    } else {
        inp.val('')
        inp.prop('disabled', false)
        checkout_field.html('')
    }
    clear_finder()
}

function clear_finder() {
    const cd = $('#client_div')
    cd.empty()
}

function render_clients(data) {
    const cd = $('#client_div')
    cd.empty()
    cd.append(get_add_card())
    data.forEach(i => {
        let name = i['name']
        if (!i['is_org'])
            name += ' ' + i['surname']
        cd.append(get_client_card(i['_id'], name, i['phone'], i['is_org']))
    })
}

function del_order() {
    send(cancel_order_endpoint).then(new_sid => {
        console.log(new_sid)
        if (new_sid !== '')
            window.location.href = `/?sid=${new_sid}`;
        else
            create_order()
    })
}

function create_order() {
    window.location.href = '/';
}

function del_item(id) {
    send(del_cart_item_endpoint, {'id': id}).then(render_cart)
}

function get_items_table_row(id, name, amount, price, fullprice) {
    const res = $('<tr>').attr('id', id)
    const t_name = $('<td>').append($('<span>').text(name)
        .attr('class', 'item-table-name mb-0 text-sm'))
    const t_amount = $('<td>').append($('<span>').text(amount)
        .attr('class', 'mb-0 text-sm')).attr('class', 'text-center').attr('width', '10%')
    const t_price = $('<td>').append($('<span>').text(price + '₽')
        .attr('class', 'align-center mb-0 text-sm')).attr('class', 'text-center').attr('width', '10%')
    const t_fullprice = $('<td>').append($('<span>').text(fullprice + '₽')
        .attr('class', 'mb-0 text-sm')).attr('class', 'text-center').attr('width', '10%')
    const t_remove = $('<td>').append($('<a>')
        .attr('class', 'nav-link').attr('onClick', `del_item(${id})`
        ).attr('href', "#!")
        .append($('<i>').attr('class', 'fa fa-trash-alt text-red mr-2')))
    res.append(t_name)
    res.append(t_amount)
    res.append(t_price)
    res.append(t_fullprice)
    res.append(t_remove)


    return res
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

function create_contragent() {
    let mas = $('#contragent_form').serializeArray()
    send(create_contragent_endpoint, clean_form(mas)).then(resp => {
        if (resp === 'success') {
            const modal = $('#addContragentModal')
            modal.modal('hide');
        }
    })
}


function get_client_card(id, name, tel, isorg) {
    let icon = 'ni-briefcase-24'
    let icon_color = 'bg-orange'
    let orgtext = 'Организация'
    if (!isorg) {
        orgtext = 'Клиент'
        icon = 'ni-single-02'
        icon_color = 'bg-blue'
    }
    return get_card(id, name, tel, icon, icon_color, orgtext)
}

function get_card(id, name, tel, icon, icon_color, orgtext) {
    const res = $('<div>')
    const fin = $('<a>').attr('href', '#!').append(res).attr('onClick',
        `set_contragent('${id}')`
    ).attr('class', 'client_card')
    let c_org = $('<h5>').attr('class', 'card-title text-uppercase text-muted mb-0').text(orgtext)
    let c_orgname = $('<span>').attr('class', 'h3 font-weight-bold mb-0').text(name)
    const c_inn = $('<p>').attr('class', 'mt-3 mb-0 text-sm').append($('<span>').attr('class', 'text-nowrap')
        .text('Тел: ' + tel))

    const icon_div = $('<div>').attr('class', 'icon icon-shape ' + icon_color + ' text-white rounded-circle shadow')
        .append($('<i>').attr('class', 'ni ' + icon))
    const c_body = $('<div>').attr('class', 'card card-stats')
        .append($('<div>').attr('class', 'card-body')
            .append($('<div>').attr('class', 'row')
                .append($('<div>').attr('class', 'col')
                    .append(c_org)
                    .append(c_orgname))
                .append($('<div>').attr('class', 'col-auto').append(icon_div)))
            .append(c_inn))
    res.append(c_body)
    return fin

}

function get_add_card() {
    let id = -1
    let name = "Добавить"
    let inn = ""
    let icon = 'fas fa-plus'
    let icon_color = 'bg-dark'
    let orgtext = ""
    const res = $('<div>')
    const fin = $('<a>').attr('data-toggle', 'modal').attr('data-target', '#addContragentModal').attr('href', '#!').append(res).attr('class', 'client_card')
    let c_org = $('<h5>').attr('class', 'card-title text-uppercase text-muted mb-0').text(orgtext)
    let c_orgname = $('<span>').attr('class', 'h3 font-weight-bold mb-0').text(name)
    const c_inn = $('<p>').attr('class', 'mt-3 mb-0 text-sm').append($('<span>').attr('class', 'text-nowrap')
        .text('Тел: ' + inn))

    const icon_div = $('<div>').attr('class', 'icon icon-shape ' + icon_color + ' text-white rounded-circle shadow')
        .append($('<i>').attr('class', 'ni ' + icon))
    const c_body = $('<div>').attr('class', 'card card-stats')
        .append($('<div>').attr('class', 'card-body')
            .append($('<div>').attr('class', 'row')
                .append($('<div>').attr('class', 'col')
                    .append(c_org)
                    .append(c_orgname))
                .append($('<div>').attr('class', 'col-auto').append(icon_div)))
            .append(c_inn))
    res.append(c_body)
    return fin
}