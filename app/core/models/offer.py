import app.db.base as db
import app.db.variables as dbvars


class RVDOffer:
    not_zero_amount = {'amount': {'$not': {'$eq': '0'}}}

    def __init__(self, session=None):
        self.arms = {}
        self.cluthes = {}
        self.fitings = {}
        self.selection = {}
        if session is None:
            self.make_offer()
        else:
            self.filter_by_session(session)

    def make_offer(self):
        self.arms = db.find(dbvars.arm_collection, self.not_zero_amount)
        self.cluthes = db.find(dbvars.clutch_collection, self.not_zero_amount)
        self.fitings = db.find(dbvars.fiting_collection, self.not_zero_amount)

    def to_dict(self):
        res = {'arms': self.arms,
               'cluthes': self.cluthes,
               'fitings': self.fitings,
               'selection': self.selection
               }
        return res

    def filter_by_session(self, session):
        selection = session.data.get('selection')
        if selection is None:
            selection = {}
        fitings = selection.get('fitings')
        arm = selection.get('arm')
        if fitings is None:
            fitings = {}
        if arm is None:
            arm = {}
        self.selection = selection
        self.arms = db.join_queries_and_find(dbvars.arm_collection, arm, self.not_zero_amount)
        self.cluthes = db.join_queries_and_find(dbvars.clutch_collection, selection.get('clutch'), arm.get('braid'), self.not_zero_amount)
        self.fitings['1'] = db.join_queries_and_find(dbvars.fiting_collection, fitings.get('1'), self.not_zero_amount)
        self.fitings['2'] = db.join_queries_and_find(dbvars.fiting_collection, fitings.get('2'), self.not_zero_amount)
