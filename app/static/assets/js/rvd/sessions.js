function init_sessions() {
    get_sessions()
}

function get_sessions() {
    send('api/get_carts').then(carts => {
        render_changer(carts)
    })
}

function render_changer(data) {
    const nav = $('#nav-pager')
    nav.empty()
    const list = $('<ul>').attr('class', 'pagination pagination-lg')
    let i = 1
    data.forEach(btn => {
        let btn_sid = btn['_id']
        console.log(`${sid} ${btn_sid}`)
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
    const btn = $('<li>').attr('class', classes)
    btn.append($('<a>').attr('class', 'page-link').attr('href', `/?sid=${link}`).text(text))
    return btn
}