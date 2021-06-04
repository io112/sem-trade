window.addEventListener("load", init);

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
        error: function (e) {
            alert(e.responseText)
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

function print_bill() {
    let windowFeatures = "menubar=yes,location=yes,resizable=yes,scrollbars=yes,status=yes";
    send(`/api/orders/${order_id}/download_bill`).then(data => {
        w = window.open(window.location.href, "_blank", windowFeatures);
        //w.document.open();
        w.document.write(data);
        //w.document.close();
        w.addEventListener("load", () => {
            alert('a')
            w.window.print();
            w.window.close();

        });
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
        tb.append(get_item_row(item['name'], item['amount'], item['price'], item['total_price']))
        if (item['items']) {
            let num = 1;
            item['items'].forEach(i => {
                let name = i['item']['name']
                if (i['local_name'])
                    name += ' [' + i['local_name']+']'
                tb.append(get_included_item_row(num, name, i['amount']))
                num += 1;
            })
        }
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
        if (data.responseText === undefined) {
            render_page(data);
        }
    })
}

function checkout_order() {
    let upd_num = $('#upd_num').val();
    send(`/api/orders/${order_id}/checkout`).then(data => {
        if (data.responseText === undefined) {
            render_page(data)
        }
    })
}


function get_item_row(name, num, price, fullprice) {
    return '<tr  id="0">\n' +
        `        <td><span class="item-table-name mb-0 text-sm">${name}</span>\n` +
        '        </td>\n' +
        `        <td class="text-center" width="10%"><span class="mb-0 text-sm">${num}</span></td>\n` +
        `        <td class="text-center" width="10%"><span class="align-center mb-0 text-sm">${price} ₽</span></td>\n` +
        `        <td class="text-center" width="10%"><span class="mb-0 text-sm">${fullprice} ₽</span></td>\n` +
        '      </tr>'
}

function get_included_item_row(num, name, amount) {
    return '<tr style="background-color: #cfd8dc" id="0">\n' +
        `        <td><span class="item-table-name mb-0 text-sm">${num}. ${name}</span>\n` +
        '        </td>\n' +
        `        <td class="text-center" width="10%"><span class="mb-0 text-sm">${amount}</span></td>\n` +
        '      </tr>'
}

function view_order(order_id) {
}
