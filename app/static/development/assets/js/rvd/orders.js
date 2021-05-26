document.addEventListener("DOMContentLoaded", init);
var current_page = 1
var limit = 15

function init() {
    current_page = 1
    limit = 15
    get_orders_list(current_page, limit)
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


function get_orders_list(page, limit) {
    request('api/orders/get_orders', {'limit': limit, 'offset': (page - 1) * limit})
        .then(data => {
            render_order_list(data, limit)
        })
}

function render_order_list(data, limit) {
    current_page = Math.floor((data['from'] - 1) / limit) + 1
    precision = 2
    const nav = $('#nav-pager')
    const l = $('<ul>').attr('class', 'pagination pagination-lg')
    nav.empty()
    for (let j = current_page - 2; j <= current_page + 2; j++) {
        console.log(data['count'])
        if (j > 0 && data['count'] - (j - 1) * limit > 0) {
            let is_active = j === current_page;
            l.append(get_btn(j, j, is_active))
        }
    }
    nav.append(l)
    let list = data['data']
    const tb = $('#orders_table')
    tb.empty()
    list.forEach(order => {
        console.log(order)
        tb.append(get_order_row(order['_id'], order['order_num'],
            order['contragent']['name'], order['user']['username'],
            order['time_created'], order['status'], order['_price']))
    })

}


function get_order_row(order_id, order_num, contragent, user, time, status, total_price) {
    time = moment(time).tz('Europe/Moscow').format('YYYY-MM-DD HH:mm z')
    return '<tr style="color:black;">\n' +
        '                  <th scope="row">\n' +
        `                    <span class="name mb-0 text-sm">${order_num}</span>\n` +
        '                  </th>\n' +
        `                  <td>${time}</td>\n` +
        `                  <td>${contragent}</td>\n` +
        `                  <td>${user}</td>\n` +
        `                  <td>${total_price} ₽</td>\n` +
        `                  <td>${status}</td>\n` +
        '                  <td class="text-right">\n' +
        '                    <div class="row">\n' +
        `                      <a class="nav-link" href="#!" onclick="view_order('${order_id}')">\n` +
        '                        <i class="far fa-eye text-blue"></i>\n' +
        '                      </a>\n' +
        '                    </div>\n' +
        '                  </td>\n' +
        '                </tr>'
}

function get_btn(page_num, text, is_active) {
    let classes = 'page-item'
    if (is_active)
        classes += ' active'
    return `<li class="${classes}">` +
        `<a class="page-link" onclick="get_orders_list(${page_num}, ${limit})" ">${text}</a>` +
        '</li>'
}

function view_order(order_id) {
    window.location.href = '/orders/' + order_id
}
