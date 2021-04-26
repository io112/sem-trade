document.addEventListener("DOMContentLoaded", init);

let order_id = ''
let order = {}

function init() {
    let path = window.location.pathname.split('/');
    order_id = path[path.length - 1];
    console.log(order_id)
    get_orders_list()

}


async function send(endpoint, data = {}) {
    if (data === undefined)
        data = []
    var request = {"data": JSON.stringify(data)}
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


function get_orders_list() {
    send('/api/orders/get_order', order_id).then(data => {
        $('#order_num').html(data['order_num']);
        render_item_list(data)
    })
}

function render_item_list(list) {
    const tb = $('#items_list')
    tb.empty()
    list['cart']['items'].forEach(item => {
        console.log(Object.keys(item)[0])
        item = item[Object.keys(item)[0]];
        tb.append(get_item_row(item['name'], item['amount'], item['price'], item['final_price']))
    })

}


function get_item_row(name, num, price, fullprice) {
    return '<tr id="0">\n' +
        `        <td><span class="item-table-name mb-0 text-sm">${name}</span>\n` +
        '        </td>\n' +
        `        <td class="text-center" width="10%"><span class="mb-0 text-sm">${num}</span></td>\n` +
        `        <td class="text-center" width="10%"><span class="align-center mb-0 text-sm">${price} ₽</span></td>\n` +
        `        <td class="text-center" width="10%"><span class="mb-0 text-sm">${fullprice} ₽</span></td>\n` +
        '      </tr>'
}

function view_order(order_id) {
}
