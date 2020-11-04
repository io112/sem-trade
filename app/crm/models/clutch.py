from app.crm.models.base import SiteObj


class Clutch(SiteObj):
    def __init__(self, o_id, name, measure, diameter,
                 clutch_type, arm_type):
        super().__init__(o_id, name, measure)
        self.type = 'clutch'

        self.diameter = diameter
        self.clutch_type = clutch_type
        self.arm_type = arm_type

    def convert_to_dict(self):
        data = super().convert_to_dict()
        data['clutch_type'] = self.clutch_type
        data['diameter'] = self.diameter
        data['arm_type'] = self.arm_type
        return data
