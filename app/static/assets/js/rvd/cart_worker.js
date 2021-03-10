async function get_cart() {
    let endpoint = '/api/get_cart'
    return await send(endpoint)
}

function update_cart() {
    get_cart().then(cart => {
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
    })

}

function update_clients() {
    const cd = $('#client_div')
    cd.empty()
    cd.append(get_card(-1, 'Добавить', '0000', 'fas fa-plus', 'bg-dark', ''))
    cd.append(get_client_card(1, 'test', 1111, true))
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
        .attr('class', 'nav-link').attr('onClick', 'update_cart()').attr('href', "#!")
        .append($('<i>').attr('class', 'fa fa-trash-alt text-red mr-2')))
    res.append(t_name)
    res.append(t_amount)
    res.append(t_price)
    res.append(t_fullprice)
    res.append(t_remove)


    return res
}


function get_client_card(id, name, inn, isorg) {
    let icon = 'ni-briefcase-24'
    let icon_color = 'bg-orange'
    let orgtext = 'Организация'
    if (!isorg) {
        orgtext = 'Клиент'
        icon = 'ni-single-02'
        icon_color = 'bg-blue'
    }
    return get_card(id, name, inn, icon, icon_color, orgtext)
}

function get_card(id, name, inn, icon, icon_color, orgtext) {
    const res = $('<div>')
    const fin = $('<a>').attr('href', '#!').append(res).attr('onClick', 'console.log("a")').attr('class', 'client_card')
    let c_org = $('<h5>').attr('class', 'card-title text-uppercase text-muted mb-0').text(orgtext)
    let c_orgname = $('<span>').attr('class', 'h3 font-weight-bold mb-0').text(name)
    const c_inn = $('<p>').attr('class', 'mt-3 mb-0 text-sm').append($('<span>').attr('class', 'text-nowrap')
<<<<<<< HEAD
        .text('ИНН: ' + inn))
=======
        .text(inn))
>>>>>>> master
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