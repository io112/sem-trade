document.addEventListener("DOMContentLoaded", init);


function init() {
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
    send('api/orders/get_orders').then(data => {
        render_order_list(data)
    })
}

function render_order_list(list) {
    const tb = $('#orders_table')
    tb.empty()
    list.forEach(order => {
        console.log(order)
        tb.append(get_order_row(order['_id'], order['order_num'], order['user']['username'], order['time_created'], order['status']))
    })

}


function get_order_row(order_id, order_num, user, time, status) {
    time = moment(time).tz('Europe/Moscow').format('YYYY-MM-DD HH:mm z')
    return '<tr>\n' +
        '                  <th scope="row">\n' +
        `                    <span class="name mb-0 text-sm">${order_num}</span>\n` +
        '                  </th>\n' +
        `                  <td>${time}</td>\n` +
        `                  <td>${user}</td>\n` +
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

function view_order(order_id) {
    window.location.href = '/orders/' + order_id
}
