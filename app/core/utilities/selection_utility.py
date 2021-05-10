from app.core.models.items.arm import Arm
from app.core.models.items.clutch import Clutch
from app.core.models.items.fiting import Fiting
from app.core.models.items.base import ItemsQuerySet
from app.core.models.selection import RVDSelection
import app.db.variables as dbvars
import app.db.base as db
from mongoengine import QuerySet

not_zero_amount = {'amount': {'$not': {'$eq': 0}}}


def queryset_to_list(qs: QuerySet):
    return [each.to_mongo().to_dict() for each in qs]


def get_candidates_by_params(selection: RVDSelection):
    fiting1 = selection.items["fiting1"]
    fiting2 = selection.items["fiting2"]
    clutch1 = selection.items["clutch1"]
    clutch2 = selection.items["clutch2"]
    arm = selection.items.get("arm", {})
    fitings = {}
    clutch_params = not_zero_amount
    arms = queryset_to_list(Arm.objects().filter_params(arm))
    clutches = queryset_to_list(Clutch.objects().filter_params(clutch1))
    fitings['1'] = queryset_to_list(Fiting.objects().filter_params(fiting1))
    fitings['2'] = queryset_to_list(Fiting.objects().filter_params(fiting2))
    res = {'arms': arms, 'clutches': clutches, 'fitings': fitings}
    return res


def get_available_parameters(candidates: dict):
    res = {}
    for i in candidates:
        res[i] = {}
