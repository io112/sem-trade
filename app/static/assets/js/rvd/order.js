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

//
// function download_upd() {
//     send(`/api/orders/${order_id}/download_upd`).then(data => {
//         w = window.open(window.location.href, "_blank");
//         //w.document.open();
//         w.document.write(data);
//         //w.document.close();
//         w.window.print();
//         w.window.close();
//     })
// }

function print_upd() {
    send(`/api/orders/${order_id}/download_upd`).then(data => {
        w = window.open(window.location.href, "_blank");
        //w.document.open();
        w.document.write(data);
        //w.document.close();
        w.window.print();
        w.window.close();
    })
}

function get_orders_list() {
    send('/api/orders/get_order', order_id).then(data => {
        render_page(data);
    })
}

function render_page(data) {
    $('#order_num').html(data['order_num']);
    $('#status').html(data['status']);
    if (data['upd_num'])
        $('#upd_num').val(data['upd_num']);
    let contragent = data['contragent']['name'];
    if (!data['contragent']['is_org'])
        contragent += ' ' + data['contragent']['surname']
    $('#clientname').val(contragent);
    $('#comment').val(data['comment']);
    render_item_list(data);
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

function save_upd_num() {
    let upd_num = $('#upd_num').val();
    send(`/api/orders/${order_id}/set_upd`, upd_num).then(data => {
        console.log('УПД сохранен');
        render_page(data);
    })
}

function close_order() {
    let upd_num = $('#upd_num').val();
    send(`/api/orders/${order_id}/close`, upd_num).then(data => {
        render_page(data);
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
