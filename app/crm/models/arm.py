from app.crm.models.base import SiteObj


class Arm(SiteObj):
    def __init__(self, o_id, name, measure, diameter):
        super().__init__(o_id, name, measure)
        self.diameter = diameter
        self.type = 'arm'

    def convert_to_dict(self):
        data = super().convert_to_dict()
        data['diameter'] = self.diameter
        return data
