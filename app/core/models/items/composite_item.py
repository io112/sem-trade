from app.core.models.items.base import BaseItem
from app.core.models.utils import create_simple_item


# noinspection SpellCheckingInspection
class CompositeItem(BaseItem):

    def __init__(self, out_name: str):
        super().__init__(out_name)
        self.name = ""
        self.amount = 0
        self.type = self.get_param_name()
        self.items = []

    @staticmethod
    def get_param_name() -> str:
        return 'composite_item'

    def get_filter_params(self) -> dict:
        dictvals = ["name"]
        return self.get_props(dictvals)

    def get_price(self) -> float:
        res = 0
        for i in self.items:
            i: BaseItem
            res += i.get_price()
        return res * self.amount

    def create_from_dict(self, data: dict):
        for i in data:
            if i == 'items':
                self.process_items(data[i])
            elif self.__dict__.get(i) is not None:
                self.__dict__[i] = data[i]

    def process_items(self, items: dict):
        for item in items:
            item_type = items[item]['type']
            res = create_simple_item(item_type, item)
            res.create_from_dict(items[item])
            self.items.append(res)

    def __get__(self, instance=None, owner=None) -> dict:
        res = {'name': self.name, 'type': self.type, 'outer_name': self.outer_name,
               'amount': self.amount, 'final_price': self.final_price, 'price': self.get_price_for_amount(1)}
        items = {}
        for i in self.items:
            i: BaseItem
            items.update(i.__get__())
        res['items'] = items
        return {self.outer_name: res}

    def get_price_for_amount(self, amount) -> float:
        price = 0
        for i in self.items:
            i: BaseItem
            price += i.final_price
        return price

    def reserve_item(self) -> str:
        errors = "success"
        completed_items = []
        for i in self.items:
            i: BaseItem
            err = i._reserve_item_amount(self.amount * i.amount)
            if err != 'success':
                errors += err
            else:
                completed_items.append(i)
        if errors != "success":
            for i in completed_items:
                i.unreserve_item()
        return errors

    def finish_item(self) -> str:
        self.final_price = 0
        for i in self.items:
            i: BaseItem
            err = i.finish_item()
            if err != 'success':
                return err
            self.final_price += i.final_price
        self.final_price *= self.amount
        return 'success'

    def unreserve_item(self):
        for i in self.items:
            i: BaseItem
            i._unreserve_item_amount(self.amount * i.amount)

    def cancel_item(self):
        for i in self.items:
            i: BaseItem
            i._cancel_item_amount(self.amount * i.amount)

    def checkout_item(self):
        for i in self.items:
            i: BaseItem
            i._checkout_item_amount(self.amount * i.amount)

    def find_candidate(self):
        for i in self.items:
            i: BaseItem
            i.find_candidate()
        return 'success'

    def check_validity(self) -> bool:
        res = True
        for i in self.items:
            i: BaseItem
            res = res and i.check_validity()
        return res

    def get_item_params(self) -> list:
        pass
