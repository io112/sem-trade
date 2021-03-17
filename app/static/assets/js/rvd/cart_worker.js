let is_org_slider = ""

function init_cw() {
    is_org_slider = $('#contragent_is_org');
    is_org_slider.on('change', change_contragent_type);
    get_contragent()
}

function change_contragent_type() {
    if ($('#contragent_is_org').is(':checked')) {
        $('#contragent_surname_block').hide()
        $('#contragent_surname').val('')
    } else {
        $('#contragent_surname_block').show()
    }
}

async function get_cart() {
    let endpoint = '/api/get_cart'
    return await send(endpoint)
}

function update_cart() {
    get_cart().then(render_cart)
}

function render_cart(cart) {
    console.log(cart)
    cart = cart['cart']
    const cart_table = $('#items_list tbody')

    cart_table.empty()
    let items = cart['items']
    let subtotal = cart['subtotal']

    let i = 0
    items.forEach(item => {
        item = item[Object.keys(item)[0]]
        cart_table.append(get_items_table_row(i, item['name'], item['amount'],
            item['price'], item['final_price']));
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
    send('api/find_contragents', $('#input-clientname').val()).then(
        res => {
            console.log(res)
            render_clients(res)
        }
    )
}

function remove_contragent() {
    send('api/remove_contragent').then(resp => {
        render_contragent(resp)
    })
}

function set_contragent(id) {
    send('api/set_contragent', id).then(resp => {
        render_contragent(resp)
    })
}

function get_contragent() {
    send('api/get_contragent').then(resp => {
        render_contragent(resp)
    })
}

function render_contragent(resp) {
    const inp = $('#input-clientname')
    if (Object.keys(resp).length !== 0) {
        let name = resp['name']
        if (!resp['is_org'])
            name += ' ' + resp['surname']
        inp.val(name)
        inp.prop('disabled', true)
    } else {
        inp.val('')
        inp.prop('disabled', false)
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

function del_item(id) {
    send('api/del_cart_item', {'id': id}).then(render_cart)
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
        .attr('class', 'nav-link').attr('onClick', `del_item(${id})`).attr('href', "#!")
        .append($('<i>').attr('class', 'fa fa-trash-alt text-red mr-2')))
    res.append(t_name)
    res.append(t_amount)
    res.append(t_price)
    res.append(t_fullprice)
    res.append(t_remove)


    return res
}


function create_contragent() {
    let mas = $('#contragent_form').serializeArray()
    send('api/create_contragent', mas).then(resp => {
        $('#addContragentModal').modal('hide');
    })
    console.log(mas)
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
    const fin = $('<a>').attr('href', '#!').append(res).attr('onClick', `set_contragent('${id}')`).attr('class', 'client_card')
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
    const fin = $('<a>').attr('data-toggle', 'modal').attr('data-target', '#addContragentModal').attr('href', '#!').append(res).attr('onClick', 'console.log("a")').attr('class', 'client_card')
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