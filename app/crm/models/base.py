class SiteObj:
    def __init__(self, o_id, name, measure):
        self.id = o_id
        self.name = name
        self.measure = measure
        self.type = 'base'

    def convert_to_dict(self):
        data = {'_id': self.id,
                'name': self.name,
                'measure': self.measure,
                'type': self.type}
        return data
