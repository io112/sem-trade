from app.crm.models.base import SiteObj


class Fiting(SiteObj):
    def __init__(self, o_id, name, measure, diameter,
                 clutch_type, fiting_type, fiting_kind,
                 size, angle):
        super().__init__(o_id, name, measure)
        self.type = 'fiting'

        self.diameter = diameter
        self.clutch_type = clutch_type
        self.fiting_type = fiting_type
        self.fiting_kind = fiting_kind
        self.size = size
        self.angle = angle

    def convert_to_dict(self):
        data = super().convert_to_dict()
        data['clutch_type'] = self.clutch_type
        data['diameter'] = self.diameter
        data['fiting_type'] = self.fiting_type
        data['fiting_kind'] = self.fiting_kind
        data['size'] = self.size
        data['angle'] = self.angle
        return data
