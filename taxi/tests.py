from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from taxi.models import Car, Driver, Manufacturer


class PrivateDriverSearchTest(TestCase):
    url = reverse("taxi:driver-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

        cls.john_smith = Driver.objects.create_user(
            username="john_smith",
            password="TestPass123!",
            first_name="John",
            last_name="Smith",
            license_number="ABC12345",
        )

        cls.john_brown = Driver.objects.create_user(
            username="john_brown",
            password="TestPass123!",
            first_name="John",
            last_name="Brown",
            license_number="XYZ54321",
        )

        cls.michael_jones = Driver.objects.create_user(
            username="michael_jones",
            password="TestPass123!",
            first_name="Michael",
            last_name="Jones",
            license_number="QWE98765",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_search_returns_matching_drivers(self):
        res = self.client.get(self.url, {"username": "john"})
        self.assertCountEqual(
            [driver.username for driver in res.context["driver_list"]],
            ["john_smith", "john_brown"]
        )

    def test_search_is_case_insensitive(self):
        res = self.client.get(self.url, {"username": "JOHN_SMITH"})
        self.assertEqual(res.context["driver_list"][0].username, "john_smith")

    def test_search_returns_empty_queryset_when_no_matches_found(self):
        res = self.client.get(self.url, {"username": "bill"})
        self.assertQuerySetEqual(res.context["driver_list"], [])

    def test_search_returns_all_drivers_when_query_is_empty(self):
        res = self.client.get(self.url, {"username": ""})
        self.assertCountEqual(
            [driver.username for driver in res.context["driver_list"]],
            ["test_user", "john_smith", "john_brown", "michael_jones"]
        )


class PrivateCarSearchTest(TestCase):
    url = reverse("taxi:car-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

        cls.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        cls.renault = Manufacturer.objects.create(
            name="Renault",
            country="France",
        )

        cls.megane = Car.objects.create(
            model="Megane",
            manufacturer=cls.renault
        )

        cls.clio = Car.objects.create(
            model="Clio",
            manufacturer=cls.renault
        )

        cls.x5 = Car.objects.create(
            model="X5",
            manufacturer=cls.bmw
        )

        cls.x6 = Car.objects.create(
            model="X6",
            manufacturer=cls.bmw
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_search_returns_partial_model_match(self):
        res = self.client.get(self.url, {"model": "X"})
        self.assertCountEqual(
            [car.model for car in res.context["car_list"]],
            ["X5", "X6"]
        )

    def test_search_is_case_insensitive(self):
        res = self.client.get(self.url, {"model": "x"})
        self.assertCountEqual(
            [car.model for car in res.context["car_list"]],
            ["X5", "X6"]
        )

    def test_search_returns_empty_queryset_when_no_matches_found(self):
        res = self.client.get(self.url, {"model": "X7"})
        self.assertQuerySetEqual(
            res.context["car_list"], []
        )

    def test_search_returns_all_cars_when_query_is_empty(self):
        res = self.client.get(self.url, {"model": ""})
        self.assertCountEqual(
            [car.model for car in res.context["car_list"]],
            ["Megane", "Clio", "X5", "X6"]
        )


class PrivateManufacturerSearchTest(TestCase):
    url = reverse("taxi:manufacturer-list")

    @classmethod
    def setUpTestData(cls):
        cls.user = Driver.objects.create_user(
            username="test_user",
            password="test123",
            license_number="TST12345",
        )

        cls.bmw = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )

        cls.renault = Manufacturer.objects.create(
            name="Alpine",
            country="France",
        )

        cls.bmw = Manufacturer.objects.create(
            name="Toyota",
            country="Japan",
        )

        cls.renault = Manufacturer.objects.create(
            name="Tesla",
            country="USA",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_search_returns_partial_name_match(self):
        res = self.client.get(self.url, {"name": "T"})
        self.assertCountEqual(
            [manufacturer.name for
             manufacturer in res.context["manufacturer_list"]],
            ["Tesla", "Toyota"]
        )

    def test_search_is_case_insensitive(self):
        res = self.client.get(self.url, {"name": "t"})
        self.assertCountEqual(
            [manufacturer.name for
             manufacturer in res.context["manufacturer_list"]],
            ["Tesla", "Toyota"]
        )

    def test_search_returns_empty_queryset_when_no_matches_found(self):
        res = self.client.get(self.url, {"name": "Bugatti"})
        self.assertQuerySetEqual(
            res.context["manufacturer_list"], []
        )

    def test_search_returns_all_manufacturers_when_query_is_empty(self):
        res = self.client.get(self.url, {"name": ""})
        self.assertCountEqual(
            [manufacturer.name for
             manufacturer in res.context["manufacturer_list"]],
            ["Alpine", "Tesla", "Toyota", "BMW"]
        )
