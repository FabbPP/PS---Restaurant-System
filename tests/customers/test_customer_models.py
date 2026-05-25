from customers.models import DeliveryCustomer


def test_customer_model_normalizes() -> None:
    customer = DeliveryCustomer(id=1, name=" Ana ", phone="987654321")
    assert customer.name == "Ana"
