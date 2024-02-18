"""
Протестируйте классы из модуля homework/models.py
"""
import random
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture()
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(random.randint(1, 1000)) is True
        assert product.check_quantity(random.randint(1001, 1500)) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        to_buy = random.randint(1, 1000)
        remainder = product.quantity - to_buy
        product.buy(to_buy)
        assert product.quantity == remainder

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        quantity_to_buy = random.randint(1001, 1500)
        with pytest.raises(ValueError) as exception_info:
            product.buy(quantity_to_buy)
        assert "Not enough 'book' product in stock" in str(exception_info)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_cart_add_product_empty(self, product, cart):
        to_buy = random.randint(1, 1000)
        cart.add_product(product, to_buy)
        assert product in cart.products
        assert cart.products[product] == to_buy

    def test_cart_add_product_non_empty(self, product, cart):
        to_buy = random.randint(1, 1000)
        cart.add_product(product, to_buy)
        cart.add_product(product, to_buy)
        assert product in cart.products
        assert cart.products[product] == to_buy * 2

    def test_cart_remove_product(self, product, cart):
        to_remove = random.randint(1, 999)
        cart.add_product(product, 1000)
        cart.remove_product(product, to_remove)
        assert product in cart.products
        assert cart.products[product] == 1000 - to_remove

    def test_cart_remove_product_position(self, product, cart):
        cart.add_product(product, 1000)
        cart.remove_product(product)
        assert product not in cart.products

    def test_cart_remove_product_position_by_count(self, product, cart):
        to_remove = random.randint(1000, 1500)
        cart.add_product(product, 1000)
        cart.remove_product(product, to_remove)
        assert product not in cart.products

    def test_cart_clear(self, product, cart):
        cart.add_product(product, 1000)
        cart.clear()
        assert len(cart.products) == 0

    def test_cart_get_total_price(self, product, cart):
        to_buy = random.randint(1, 1000)
        cart.add_product(product, to_buy)
        assert cart.get_total_price() == product.price * to_buy

    def test_cart_buy_success(self, product, cart):
        to_buy = random.randint(1, 1000)
        original_quantity = product.quantity
        cart.add_product(product, to_buy)
        cart.buy()
        assert product.quantity == original_quantity - to_buy
        assert len(cart.products) == 0

    def test_cart_buy_not_in_stock(self, product, cart):
        to_buy = random.randint(1000, 1500)
        cart.add_product(product, to_buy)
        with pytest.raises(ValueError) as exception_info:
            cart.buy()
        assert "Not enough book in stock" in str(exception_info)
        assert len(cart.products) == 1
