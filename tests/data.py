from dataclasses import dataclass

# Public demo credentials displayed on the SauceDemo login page; not private secrets.
STANDARD_USER = "standard_user"
DEMO_PASSWORD = "secret_sauce"


@dataclass(frozen=True)
class Product:
    name: str
    price: str


BACKPACK = Product("Sauce Labs Backpack", "$29.99")
BIKE_LIGHT = Product("Sauce Labs Bike Light", "$9.99")
