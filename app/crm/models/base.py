class SiteObj:

    def __init__(self):
        self.id = ''
        self.name = ''
        self.measure = ''
        self.category_id = ''
        self.type = 'base'

    def convert_to_dict(self):
        data = {'_id': self.id,
                'category_id': self.category_id,
                'name': self.name,
                'measure': self.measure,
                'type': self.type}
        return data

    def convert_for_update(self):
        return {"$set": self.convert_to_dict()}

    @staticmethod
    def create_from_cml(obj):
        res = SiteObj()
        res.id = obj[0].text
        res.name = obj[2].text
        res.measure = obj[3].attrib['НаименованиеПолное']
        return res
