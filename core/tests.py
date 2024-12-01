from django.test import TestCase
from core.models import Property, ViewingRequest, RentalAgreement
from django.contrib.auth import get_user_model

class PropertyTestCase(TestCase):
    def setUp(self):
        # Создаем пользователя-риелтора
        self.realtor = get_user_model().objects.create_user(
            username='realtor',
            password='password',
            role='realtor',
            email='realtor@example.com'
        )

    def test_create_property(self):
        # Создаем объект недвижимости
        property = Property.objects.create(
            title="Квартира в центре",
            description="Большая светлая квартира.",
            area=50.5,
            location="Москва",
            price=50000,
            status="available",
            realtor=self.realtor
        )

        # Проверка, что объект создан и данные корректны
        self.assertEqual(property.title, "Квартира в центре")
        self.assertEqual(property.status, "available")
        self.assertEqual(property.realtor, self.realtor)
        self.assertEqual(property.price, 50000)
        self.assertEqual(property.location, "Москва")

    def test_property_str_method(self):
        property = Property.objects.create(
            title="Квартира в центре",
            description="Большая светлая квартира.",
            area=50.5,
            location="Москва",
            price=50000,
            status="available",
            realtor=self.realtor
        )

        # Проверка работы метода __str__
        self.assertEqual(str(property), "Квартира в центре")


class ViewingRequestModelTest(TestCase):
    def setUp(self):
        # Создаем пользователей
        self.realtor = get_user_model().objects.create_user(
            username='realtor',
            password='password',
            role='realtor',
            email='realtor@example.com'
        )
        self.client = get_user_model().objects.create_user(
            username='client',
            password='password',
            role='client',
            email='client@example.com'
        )
        self.property = Property.objects.create(
            title="Квартира в центре",
            description="Большая светлая квартира.",
            area=50.5,
            location="Москва",
            price=50000,
            status="available",
            realtor=self.realtor
        )

    def test_create_viewing_request(self):
        # Создаем запрос на просмотр
        viewing_request = ViewingRequest.objects.create(
            property=self.property,
            user=self.client,
            realtor=self.realtor,
            viewing_time="2024-12-01"
        )

        # Проверка, что запрос на просмотр был создан
        self.assertEqual(viewing_request.property, self.property)
        self.assertEqual(viewing_request.user, self.client)
        self.assertEqual(viewing_request.status, 'pending')
        self.assertEqual(str(viewing_request), f'Запрос на просмотр {self.property.title} от {self.client.username}')

    def test_viewing_request_status_change(self):
        # Создаем запрос на просмотр и меняем его статус
        viewing_request = ViewingRequest.objects.create(
            property=self.property,
            user=self.client,
            realtor=self.realtor,
            viewing_time="2024-12-01"
        )
        viewing_request.status = 'confirmed'
        viewing_request.save()

        # Проверка изменения статуса
        self.assertEqual(viewing_request.status, 'confirmed')


class RentalAgreementModelTest(TestCase):
    def setUp(self):
        # Создаем пользователей
        self.realtor = get_user_model().objects.create_user(
            username='realtor',
            password='password',
            role='realtor',
            email='realtor@example.com'
        )
        self.client = get_user_model().objects.create_user(
            username='client',
            password='password',
            role='client',
            email='client@example.com'
        )
        self.property = Property.objects.create(
            title="Квартира в центре",
            description="Большая светлая квартира.",
            area=50.5,
            location="Москва",
            price=50000,
            status="available",
            realtor=self.realtor
        )
        self.viewing_request = ViewingRequest.objects.create(
            property=self.property,
            user=self.client,
            realtor=self.realtor,
            viewing_time="2024-12-01"
        )

    def test_create_rental_agreement(self):
        # Создаем договор аренды
        rental_agreement = RentalAgreement.objects.create(
            viewing_request=self.viewing_request,
            tenant=self.client,
            realtor=self.realtor,
            start_date="2024-12-10",
            end_date="2025-12-10",
            rent_price=50000
        )

        # Проверка, что договор аренды был создан
        self.assertEqual(rental_agreement.viewing_request, self.viewing_request)
        self.assertEqual(rental_agreement.tenant, self.client)
        self.assertEqual(rental_agreement.realtor, self.realtor)
        self.assertEqual(rental_agreement.rent_price, 50000)
        self.assertEqual(str(rental_agreement), f"Договор аренды: {self.viewing_request.property.title} - {self.client.username}")