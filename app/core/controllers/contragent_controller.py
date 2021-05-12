import app.core.utilities.contragent_utility as utility


def get_contragent(cid: str) -> dict:
    contragent = utility.get_contragent(cid)
    return contragent.get_safe()


def find_contragents(query: str):
    return utility.find_contragents(query)


def create_contragent_from_form(form_data):
    res = {}
    for i in form_data:
        i: dict
        key = i['name']
        val = i['value']
        if key == 'is_org':
            res['is_org'] = True
        else:
            res[key] = val
    utility.create_contragent(res)
