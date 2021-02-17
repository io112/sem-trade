import app.db.base as db
import app.db.variables as dbvars
from app.core.models.RVDItem import RVDItem
from app.core.models.items.arm import Arm
from app.core.models.items.base import BaseItem
from app.core.models.selection import RVDSelection
from app.core.models.session import Session
from app.core.sessions import update_session


class RVDOffer:
    not_zero_amount = {'amount': {'$not': {'$eq': '0'}}}

    def __init__(self, session=None):
        self.arms = {}
        self.clutches = {}
        self.fitings = {}
        self.selection = RVDSelection(session)
        self.select_subtotal = {'name': '', 'amount': 1, 'price': 0, 'total_price': 0}
        if session is None:
            self.make_offer()
        else:
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
        print(self.selection.get_subtotal())
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

    def create_cart_item(self, session, is_repair=False):
        selection = session.data.get('selection')
        arm = selection.get('arm')
        fitings = selection.get('fitings')
        clutches = selection.get('clutches')
        if arm is None or fitings is None or clutches is None:
            return 'some of components is undefined'
        if arm['diameter'] is None or arm['arm_type'] is None or arm['braid'] \
                is None or arm['length'] is None:
            return 'some of arm params is undefined'
        if fitings['1'] is None or fitings['2'] is None or fitings['1']['name'] \
                is None or fitings['2']['name'] is None:
            return 'one of fitings is undefined'
        if clutches['1'] is None or clutches['2'] is None or clutches['1']['name'] \
                is None or clutches['2']['name'] is None:
            return 'one of clutches is undefined'
        cart = session.data.get('cart')
        if cart is None:
            cart = []
        arm = self.get_component(dbvars.arm_collection, arm)
        clutch1 = self.get_component(dbvars.clutch_collection, clutches['1'])
        clutch2 = self.get_component(dbvars.clutch_collection, clutches['2'])
        fiting1 = self.get_component(dbvars.fiting_collection, fitings['1'])
        fiting2 = self.get_component(dbvars.fiting_collection, fitings['2'])
        item = RVDItem(arm, fiting1, fiting2, clutch1, clutch2)
        print(item)
        db.insert(dbvars.rvd_items_collection, item.to_dict())
        # TODO: clear selection and decrement amounts
        return 'success'

    def filter_by_session(self, session: Session):
        selection = self.selection
        self.selection.set_subtotal(self.make_subtotal())
        session.add_data({'selection': self.selection.__get__()})
        update_session(session)
        fiting1 = selection["fiting1"]
        fiting2 = selection["fiting2"]
        arm = selection["arm"]
        clutch_params = {}
        if arm.get_param_name() == Arm.get_param_name():
            clutch_params = arm.get_clutch_params()
        self.selection = selection
        self.arms = db.join_queries_and_find(dbvars.arm_collection, arm.get_filter_params(), self.not_zero_amount)
        self.clutches = db.join_queries_and_find(dbvars.clutch_collection, clutch_params,
                                                 self.not_zero_amount)
        self.fitings['1'] = db.join_queries_and_find(dbvars.fiting_collection, fiting1.get_filter_params(),
                                                     self.not_zero_amount)
        self.fitings['2'] = db.join_queries_and_find(dbvars.fiting_collection, fiting2.get_filter_params(),
                                                     self.not_zero_amount)
