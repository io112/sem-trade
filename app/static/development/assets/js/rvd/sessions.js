window.addEventListener("load", init);
var current_page = 1
var limit = 15

function init() {
    get_session_list(current_page, limit)
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


function get_session_list(page, limit) {
    request('api/sessions/get_sessions', {'limit': limit, 'offset': (page - 1) * limit}).then(data => {
        render_session_list(data, limit)
    })
}

function render_session_list(data) {
    current_page = Math.floor((data['from'] - 1) / limit) + 1
    let precision = 2
    const nav = $('#nav-pager')
    const l = $('<ul>').attr('class', 'pagination pagination-lg')
    nav.empty()
    for (let j = current_page - precision; j <= current_page + precision; j++) {
        console.log(data['count'])
        if (j > 0 && data['count'] - (j - 1) * limit > 0) {
            let is_active = j === current_page;
            l.append(get_btn(j, j, is_active))
        }
    }
    nav.append(l)
    let list = data['data']
    const tb = $('#sessions_table')
    tb.empty()
    list.forEach(session => {
        console.log(session)
        let cart = session['cart'] ? session['cart']['subtotal'] : 0
        let contragent = session['contragent'] ? session['contragent']['name'] : ''
        tb.append(get_session_row(session['_id'], session['last_modified'], session['user'], cart,
            contragent))
    })

}


function get_session_row(session_id, time, user, total_price, contragent) {
    time = moment(time).tz('Europe/Moscow').format('YYYY-MM-DD HH:mm z')
    return '<tr>\n' +
        '                  <th scope="row">\n' +
        `                    <span class="name mb-0 text-sm">${session_id}</span>\n` +
        '                  </th>\n' +
        `                  <td>${time}</td>\n` +
        `                  <td>${contragent}</td>\n` +
        `                  <td>${user}</td>\n` +
        `                  <td>${total_price} ₽</td>\n` +
        '                  <td class="text-right">\n' +
        '                    <div class="row">\n' +
        `                      <a class="nav-link" href="#!" onclick="del_session('${session_id}')">\n` +
        '                        <i class="fa fa-trash-alt text-red"></i>\n' +
        '                      </a>\n' +
        `                      <a class="nav-link" href="#!" onclick="open_session('${session_id}')">\n` +
        '                        <i class="fa fa-edit text-blue"></i>\n' +
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
        `<a class="page-link" onclick="get_session_list(${page_num}, ${limit})" ">${text}</a>` +
        '</li>'
}

function open_session(new_sid) {
    window.location.href = '/?sid=' + new_sid
}

function del_session(del_id) {
    console.log(del_id)
    send('api/sessions/remove_session', del_id).then(list => {
        render_session_list(list)
    })
}
