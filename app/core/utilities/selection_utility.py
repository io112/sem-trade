from app.core.models.items.arm import Arm
from app.core.models.selection import RVDSelection
import app.db.variables as dbvars
import app.db.base as db

not_zero_amount = {'amount': {'$not': {'$eq': 0}}}


def get_candidates_by_params(selection: RVDSelection):
    fiting1 = selection.items["fiting1"]
    fiting2 = selection.items["fiting2"]
    arm = selection.items.get("arm", EmptyItem())
    fitings = {}
    clutch_params = not_zero_amount
    if arm != {}:
        arm: Arm
        clutch_params = arm.get_clutch_params()
    arms = db.join_queries_and_find(dbvars.arm_collection, arm.get_filter_params())
    clutches = db.join_queries_and_find(dbvars.clutch_collection, clutch_params)
    fitings['1'] = db.join_queries_and_find(dbvars.fiting_collection, fiting1.get_filter_params())
    fitings['2'] = db.join_queries_and_find(dbvars.fiting_collection, fiting2.get_filter_params())
    res = {'arms': arms, 'clutches': clutches, 'fitings': fitings}
    return res


def get_available_parameters(candidates: dict):
    res = {}
    for i in candidates:
        res[i] = {}

