import app.db.base as db
import app.db.variables as dbvars
from app.core.models.RVDItem import RVDItem
from app.core.models.selection import RVDSelection
from app.core.models.session import Session
from app.core.sessions import update_session


class RVDOffer:
    not_zero_amount = {'amount': {'$not': {'$eq': '0'}}}

    def __init__(self, session=None):
        self.arms = {}
        self.clutches = {}
        self.fitings = {}
        self.selection = {}
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
        result = {'name': '', 'amount': 1, 'price': 0, 'total_price': 0}
        params = {'arm_type': '',
                  'braid': '',
                  'diameter': '',
                  'fit1': '',
                  'fit2': ''
                  }
        components_price = 0

        if self.selection is not None:
            subt = self.selection.get('subtotal')
            if subt is not None:
                self.select_subtotal = subt
                result = subt
            arm = self.selection.get('arm')
            fitings = self.selection.get('fitings')
            clutches = self.selection.get('clutches')

            if arm is not None and len(arm.keys()) != 0:
                params["arm_type"] = arm.get('arm_type')
                params["braid"] = arm.get('braid')
                params["diameter"] = arm.get('diameter')
                arm_len = int(arm.get('length', 1))
                if arm.get('length') is not None:
                    arm.__delitem__('length')
                arm_price = self.get_component_price(dbvars.arm_collection, arm)
                arm["length"] = str(arm_len)
                components_price += arm_price * arm_len

            if fitings is not None:
                fiting = fitings.get('1')
                if fiting is not None and len(fiting.keys()) != 0:
                    params["fit1"] = fiting.get('fiting_type')
                    components_price += self.get_component_price(dbvars.fiting_collection, fiting)

                fiting = fitings.get('2')
                if fiting is not None and len(fiting.keys()) != 0:
                    params["fit2"] = fiting.get('fiting_type')
                    components_price += self.get_component_price(dbvars.fiting_collection, fiting)

            if clutches is not None:
                clutch = clutches.get('1')
                if clutch is not None and len(clutch.keys()) != 0:
                    components_price += self.get_component_price(dbvars.clutch_collection, clutch)

                clutch = clutches.get('2')
                if clutch is not None and len(clutch.keys()) != 0:
                    components_price += self.get_component_price(dbvars.clutch_collection, clutch)

            for i in params:
                if params[i] is None:
                    params[i] = ''
        result["name"] = f'Рукав {params["arm_type"]}x{params["diameter"]} ' \
                         f'{params["braid"]} {params["fit1"]}+{params["fit2"]}'
        result["price"] = components_price
        result["total_price"] = components_price * self.select_subtotal["amount"]
        self.select_subtotal = result
        return result

    def to_dict(self):
        res = {'arms': self.arms,
               'clutches': self.clutches,
               'fitings': self.fitings,
               'selection': self.selection,
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
        clutch_params = {}
        selection = RVDSelection(session)
        self.selection = selection
        self.selection["subtotal"] = self.make_subtotal()
        session.add_data({'selection': self.selection.__get__()})
        update_session(session)
        fiting1 = selection.fiting1
        fiting2 = selection.fiting2
        arm = selection.arm
        if arm['diameter'] is not None:
            clutch_params = {'diameter': arm['diameter']}
        self.selection = selection
        self.arms = db.join_queries_and_find(dbvars.arm_collection, arm.get_filter_params(), self.not_zero_amount)
        self.clutches = db.join_queries_and_find(dbvars.clutch_collection, clutch_params, self.not_zero_amount)
        self.fitings['1'] = db.join_queries_and_find(dbvars.fiting_collection, fiting1.get_filter_params(),
                                                     self.not_zero_amount)
        self.fitings['2'] = db.join_queries_and_find(dbvars.fiting_collection, fiting2.get_filter_params(),
                                                     self.not_zero_amount)

    def get_component_price(self, collection, component):
        res = self.get_component(collection, component)
        if res is None:
            return 0
        component_price = int(res["price"])
        return component_price

    @staticmethod
    def get_component(collection, component: dict):
        if component.get('length') is not None:
            component.__delitem__('length')
        res = db.join_queries_and_find(collection, component)
        if len(res) == 0:
            return None
        return res[0]
