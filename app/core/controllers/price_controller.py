from app.core.models.items.cart_item import CartItem
from app.core.models.price import Price
from app.core.utilities.items_utility import get_item, get_generic_item


class RVDPrice:
    @staticmethod
    def calc_part_price(part, rvd_type) -> Price:
        item = get_item(part['type'], part['id'])
        amount = part['amount']
        price = RVDPrice.round_price(RVDPrice.calc_extra(item.price))
        full_price = RVDPrice.round_price(RVDPrice.calc_extra(item.price * amount))
        return Price(price=price, full_price=full_price, amount=amount, measure=part['measure'])

    @staticmethod
    def calc_cart_item_price(item: CartItem, rvd_type) -> Price:
        if item.item is None:
            return Price(price=item.price, full_price=item.price, amount=item.amount, measure="")
        amount = item.amount
        base_price = item.item.price
        price = RVDPrice.round_price(RVDPrice.calc_extra(base_price))
        full_price = RVDPrice.round_price(RVDPrice.calc_extra(base_price * amount))
        return Price(price=price, full_price=full_price, amount=amount, measure=item.item.measure)

    @staticmethod
    def calc_extra(price) -> float:
        if price <= 100:
            return price + price * 3
        if price <= 500:
            return price + price * 1.3
        if price <= 3000:
            return price + price * 1.2
        return price + price * 0.5

    @staticmethod
    def round_price(price) -> float:
        return round(price, 2)


class PartPrice:
    @staticmethod
    def calc_part_price(part, amount) -> Price:
        item = get_generic_item(part['_id'])
        price = PartPrice.round_price(PartPrice.calc_extra(item.price))
        full_price = PartPrice.round_price(PartPrice.calc_extra(item.price * amount))
        return Price(price=price, full_price=full_price, amount=amount, measure=item.measure)

    @staticmethod
    def calc_cart_item_price(item: CartItem) -> Price:
        if item.item is None:
            return Price(price=item.price, full_price=item.price, amount=item.amount, measure="")
        amount = item.amount
        base_price = item.item.price
        price = PartPrice.round_price(PartPrice.calc_extra(base_price))
        full_price = PartPrice.round_price(PartPrice.calc_extra(base_price * amount))
        return Price(price=price, full_price=full_price, amount=amount, measure=item.item.measure)

    @staticmethod
    def calc_extra(price) -> float:
        return price

    @staticmethod
    def round_price(price) -> float:
        return round(price, 2)
