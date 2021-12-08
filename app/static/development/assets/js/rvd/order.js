window.addEventListener("load", init);

let order_id = ''
let order = {}


function init() {
    let path = window.location.pathname.split('/');
    order_id = path[path.length - 1];
    console.log(order_id)
    get_orders_list()

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
    get(API_ORDER_UPD_GET, {order_id: order_id}).then(data => {
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
    get(API_ORDER_BILL_GET, {order_id: order_id}).then(data => {
        w = window.open(window.location.href, "_blank", windowFeatures);
        //w.document.open();
        w.document.write(data);
        //w.document.close();
        w.addEventListener("load", () => {
            w.window.print();
            w.window.close();

        });
    })
}

async function get_orders_list() {
    let resp = await get(API_ORDER_GET, {order_id: order_id})
    render_page(resp);
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
                let name = i['name']
                if (i['local_name'])
                    name += ' [' + i['local_name'] + ']'
                tb.append(get_included_item_row(num, name, i['amount']))
                num += 1;
            })
        }
    })

}

function save_upd_num() {
    let upd_num = $('#upd_num').val();
    put(API_ORDER_UPD_SET, {order_id: order_id, upd_num: upd_num}).then(data => {
        console.log('УПД сохранен');
        render_page(data);
    })
}

async function close_order() {
    let resp = await request(API_ORDER_MAKE_OP, {order_id: order_id, operation: 'close'})
    if (typeof resp === "string") {
        alert(resp)
    } else {
        render_page(resp);
    }
}

async function checkout_order() {
    let resp = await request(API_ORDER_MAKE_OP, {order_id: order_id, operation: 'checkout'})
    if (typeof resp === "string") {
        alert(resp)
    } else {
        render_page(resp);
    }
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
