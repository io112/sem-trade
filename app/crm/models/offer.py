class Offer:

    def __init__(self):
        self.id = ''
        self.amount = 0
        self.collection = ''
        self.price = 0
        self.type = 'offer'

    def convert_to_dict(self):
        data = {'_id': self.id,
                'amount': float(self.amount),
                'price': float(self.price)}
        return data

    def convert_for_update(self):
        return {"$set": self.convert_to_dict()}

    @staticmethod
    def create_from_cml(obj):
        res = Offer()
        res.id = obj[0].text
        res.price = obj.find("{urn:1C.ru:commerceml_2}Цены")[0][2].text
        res.amount = obj.find("{urn:1C.ru:commerceml_2}Количество").text

        return res
