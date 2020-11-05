class Offer:

    def __init__(self):
        self.id = ''
        self.amount = 0
        self.type = 'offer'

    def convert_to_dict(self):
        data = {'_id': self.id,
                'amount': self.amount}
        return data

    @staticmethod
    def create_from_cml(obj):
        res = Offer()
        res.id = obj[1].text
        res.amount = obj.find("{urn:1C.ru:commerceml_2}Количество")

        return res
