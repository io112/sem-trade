import app.db.base as db
import app.db.variables as dbvars
from app.core.models.cart import Cart
from app.core.models.items.arm import Arm
from app.core.models.items.base import BaseItem
from app.core.models.items.composite_item import CompositeItem
from app.core.models.selection import RVDSelection
from app.core.models.session import Session
from app.core.sessions import update_session


class RVDOffer:
    not_zero_amount = {'amount': {'$not': {'$eq': '0'}}}

    def __init__(self, session=None):
        self.arms = {}
        self.clutches = {}
        self.fitings = {}
        self.selection: RVDSelection = RVDSelection(session)
        self.select_subtotal = {'name': '', 'amount': 1, 'price': 0, 'total_price': 0}
        if session is None:
            self.make_offer()
        else:
            self.session = session
            self.filter_by_session(session)

    def make_offer(self):
        self.arms = db.find(dbvars.arm_collection, self.not_zero_amount)
        self.clutches = db.find(dbvars.clutch_collection, self.not_zero_amount)
        self.fitings = db.find(dbvars.fiting_collection, self.not_zero_amount)

    def make_subtotal(self):
        self.selection: RVDSelection
        result = {'name': '', 'amount': 1, 'price': 0, 'total_price': 0}
        params = {'arm_type': '',
                  'braid': '',
                  'diameter': '',
                  'fit1': '',
                  'fit2': ''
                  }
        arm = self.selection['arm']
        fiting1 = self.selection['fiting1']
        fiting2 = self.selection['fiting2']

        components_price = self.selection.calc_subtotal()
        amount = self.selection.get_subtotal()['subtotal'].get("amount")
        if amount is None:
            amount = 1

        result["name"] = f'Рукав {arm["arm_type"]}x{arm["diameter"]} ' \
                         f'{arm["braid"]} {fiting1["name"]}+{fiting2["name"]}'
        result["price"] = components_price
        result["total_price"] = components_price * amount
        result["amount"] = amount
        self.select_subtotal = result
        return result

    def to_dict(self):
        self.selection: RVDSelection
        res = {'arms': self.arms,
               'clutches': self.clutches,
               'fitings': self.fitings,
               'selection': self.selection.__get__(),
               }
        return res

    def create_cart_item(self, is_repair=False) -> list:
        self.selection: RVDSelection
        errors = self.selection.check_presence()
        if errors:
            response = '\r\n'.join(errors)
            print(errors)
            raise Exception('selection has problems: ' + response)
        else:
            ans = self.selection.finish_selection()
            cart = Cart.create_from_session(self.session)
            err = cart.add(ans)
            if err != 'success':
                print('err: ' + err)
            else:
                del self.selection
            self.session.add_data(cart.dict)
            self.session.remove_data('selection')
            update_session(self.session)
            return []

    def get_errors(self):
        self.selection: RVDSelection
        return self.selection.check_presence()

    def filter_by_session(self, session: Session):
        selection = self.selection
        self.selection.set_subtotal(self.make_subtotal())
        session.add_data({'selection': self.selection.__get__()})
        update_session(session)
        fiting1 = selection["fiting1"]
        fiting2 = selection["fiting2"]
        arm = selection["arm"]
        clutch_params = self.not_zero_amount
        if arm.get_param_name() == Arm.get_param_name():
            clutch_params = arm.get_clutch_params()
        self.selection = selection
        self.arms = db.join_queries_and_find(dbvars.arm_collection, arm.get_filter_params())
        self.clutches = db.join_queries_and_find(dbvars.clutch_collection, clutch_params)
        self.fitings['1'] = db.join_queries_and_find(dbvars.fiting_collection, fiting1.get_filter_params())
        self.fitings['2'] = db.join_queries_and_find(dbvars.fiting_collection, fiting2.get_filter_params())
