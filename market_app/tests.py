from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import User


class BaseTestCase(APITestCase):
    """
    Базовые настройки тест-кейса.
    Создание пользователей.
    Создание клиента для каждого пользователя.
    Аутентификация пользователей.
    """

    USERS_DATA = [
        {"email": "ivan@mail.ru", "password": "qwerty123!"},
        {"email": "max@mail.ru", "password": "qwerty123!"},
    ]

    URL = "/api/ads/"

    ADS_DATA = [
        {"title": "Продам ноутбук", "price": 50000, "description": "Хороший ноутбук"},
        {
            "title": "Продам машину",
            "price": 300000,
            "description": "Отличное состояние",
        },
    ]

    def setUp(self):
        self.user_1 = User.objects.create_user(
            email="ivan@mail.com",
            first_name="Ivan",
            last_name="Ivanov",
            patronymic="Ivanovich",
            password="Qwerty12345!",
            phone="+7(912)345-67-89",
        )
        self.user_2 = User.objects.create_user(
            email="max@mail.com",
            first_name="Max",
            last_name="Maxov",
            patronymic="Maxoovich",
            password="Qwerty12345!",
            phone="+7(912)345-67-89",
        )
        self.user_clients = []
        for user_data in self.USERS_DATA:
            client = self.create_authenticated_client(user_data)
            self.user_clients.append(client)


class ProductTestCase(BaseTestCase):
    """Создание продукта """

    def test_unauthorized_user_cannot_create_ad(self):
        """Неавторизованный пользователь не может создать продукт"""
        data = {
            "name": "ноутбук",
            "price": "50000",
            "created_at": "08.09.2023",
            "updated_at": "08.09.2023",
        }
        client = APIClient()
        response = client.post(self.URL, data)
        response_data = response.json()

        self.assertEqual(
            response_data.get("detail"), "Учетные данные не были предоставлены."
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_create_ad(self):
        """Успешное создание продуктов обычным пользователем"""
        for i, client in enumerate(self.user_clients):
            ad_data = self.ADS_DATA[i]
            response = client.post(self.URL, ad_data)
            response_data = response.json()

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(response_data.get("pk"))
            self.assertEqual(response_data.get("name"), ad_data.get("name"))
            self.assertEqual(response_data.get("price"), ad_data.get("price"))
            self.assertEqual(
                response_data.get("created_at"), ad_data.get("created_at")
            )
            self.assertEqual(
                response_data.get("updated_at"), ad_data.get("updated_at")
            )

        all_ads = APIClient().get(self.URL).json().get("results")
        self.assertEqual(len(all_ads), 2)


class ProductReadTestCase(BaseTestCase):
    """
    Чтение продукта
    """

    def setUp(self):
        super().setUp()

        self.ad_ids = []

        for i, client in enumerate(self.user_clients):
            ad_data = self.ADS_DATA[i]
            response = client.post(self.URL, ad_data)
            response_data = response.json()
            self.ad_ids.append(response_data.get("pk"))

    def test_admin_user_can_read_products(self):
        """
        Админ и обычный пользователь видят свои продукты и продукты друг друга по ID.
        """

        for client in self.user_clients:
            for ad_id in self.ad_ids:
                response = client.get(f"{self.URL}{ad_id}/")
                self.assertEqual(response.status_code, status.HTTP_200_OK)

                index = self.ad_ids.index(ad_id)
                original_ad_data = self.ADS_DATA[index]

                response_data = response.json()

                self.assertTrue(response_data.get("pk"))
                self.assertEqual(response_data.get("name"), original_ad_data.get("name"))
                self.assertEqual(response_data.get("price"), original_ad_data.get("price"))
                self.assertEqual(
                    response_data.get("created_at"), original_ad_data.get("created_at")
                )
                self.assertEqual(
                    response_data.get("updated_at"), original_ad_data.get("updated_at")
                )

    def test_unauthorized_user_can_not_read_products(self):
        """
        Неавторизованный пользователь не видит прдукты по ID.
        """

        client = APIClient()
        for ad_id in self.ad_ids:
            response = client.get(f"{self.URL}{ad_id}/")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_admin_can_read_list_of_products(self):
        """
        Админ и обычный пользователь видят список всех продуктов.
        """

        for client in self.user_clients:
            response = client.get(self.URL)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_data = response.json()
            results_from_response = response_data.get("results")

            ad_ids_from_response = [ad.get("pk") for ad in results_from_response]
            self.assertTrue(all(ad_id in ad_ids_from_response for ad_id in self.ad_ids))

            for ad in results_from_response:
                ad_id = ad.get("pk")

                index = self.ad_ids.index(ad_id)
                original_ad_data = self.ADS_DATA[index]

                self.assertTrue(response_data.get("pk"))
                self.assertEqual(response_data.get("name"), original_ad_data.get("name"))
                self.assertEqual(response_data.get("price"), original_ad_data.get("price"))
                self.assertEqual(
                    response_data.get("created_at"), original_ad_data.get("created_at")
                )
                self.assertEqual(
                    response_data.get("updated_at"), original_ad_data.get("updated_at")
                )

    def test_unauthorized_user_can_read_of_list_products(self):
        """
        Неавторизованный пользователь видит список продуктов.
        """

        client = APIClient()
        response = client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        results_from_response = response_data.get("results")

        ad_ids_from_response = [ad.get("pk") for ad in results_from_response]
        self.assertTrue(all(ad_id in ad_ids_from_response for ad_id in self.ad_ids))

        for ad in results_from_response:
            ad_id = ad.get("pk")

            index = self.ad_ids.index(ad_id)
            original_ad_data = self.ADS_DATA[index]

            self.assertTrue(response_data.get("pk"))
            self.assertEqual(response_data.get("name"), original_ad_data.get("name"))
            self.assertEqual(response_data.get("price"), original_ad_data.get("price"))
            self.assertEqual(
                response_data.get("created_at"), original_ad_data.get("created_at")
            )
            self.assertEqual(
                response_data.get("updated_at"), original_ad_data.get("updated_at")
            )

    def test_user_can_read_own_products(self):
        """
        Авторизованные пользователи могут видеть свои продукты
        """

        for i, client in enumerate(self.user_clients):
            response = client.get(self.URL + "me/")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_data = response.json()
            results_from_response = response_data.get("results")

            own_ads = [self.ad_ids[i]]

            ad_ids_from_response = [ad.get("pk") for ad in results_from_response]
            self.assertTrue(all(ad_id in own_ads for ad_id in ad_ids_from_response))

            for ad in results_from_response:
                ad_id = ad.get("pk")

                index = self.ad_ids.index(ad_id)
                original_ad_data = self.ADS_DATA[index]

                self.assertTrue(response_data.get("pk"))
                self.assertEqual(response_data.get("name"), original_ad_data.get("name"))
                self.assertEqual(response_data.get("price"), original_ad_data.get("price"))
                self.assertEqual(
                    response_data.get("created_at"), original_ad_data.get("created_at")
                )
                self.assertEqual(
                    response_data.get("updated_at"), original_ad_data.get("updated_at")
                )


class ProductPartialUpdateAPITestCase(BaseTestCase):
    """Частичное обновление продуктов"""

    def setUp(self):
        super().setUp()

        self.ad_ids = []

        for i, client in enumerate(self.user_clients):
            ad_data = self.ADS_DATA[i]
            response = client.post(self.URL, ad_data)
            response_data = response.json()
            self.ad_ids.append(response_data.get("pk"))

    def test_unauthorized_user_cannot_update_products(self):
        """Неавторизованный пользователь не может обновлять продукты"""

        client = APIClient()
        for ad_id in self.ad_ids:
            response = client.patch(f"{self.URL}{ad_id}/", {"name": "New title"})
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_update_own_products(self):
        """Обычный пользователь может обновлять только свои продукты"""

        for i, client in enumerate(self.user_clients):
            ad_id = self.ad_ids[i]
            response = client.patch(f"{self.URL}{ad_id}/", {"name": "New name"})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response_data = response.json()
            self.assertEqual(response_data.get("name"), "New name")

    def test_user_cannot_update_others_products(self):
        """Обычный пользователь не может обновлять чужие продукты"""

        client = self.user_clients[0]
        ad_id = self.ad_ids[1]

        response = client.patch(f"{self.URL}{ad_id}/", {"name": "New name"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdDeleteAPITestCase(BaseTestCase):
    """Удаление продуктов"""

    def setUp(self):
        super().setUp()

        self.ad_ids = []

        for i, client in enumerate(self.user_clients):
            ad_data = self.ADS_DATA[i]
            response = client.post(self.URL, ad_data)
            response_data = response.json()
            self.ad_ids.append(response_data.get("pk"))

    def test_unauthorized_user_cannot_delete_products(self):
        """Неавторизованный пользователь не может удалять продукты"""

        client = APIClient()
        for ad_id in self.ad_ids:
            response = client.delete(f"{self.URL}{ad_id}/")
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_delete_own_products(self):
        """Обычный пользователь может удалять только свои продукты"""

        for i, client in enumerate(self.user_clients):
            ad_id = self.ad_ids[i]
            response = client.delete(f"{self.URL}{ad_id}/")
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = APIClient().get(f"{self.URL}")
        self.assertEqual(len(response.json()["results"]), 0)

    def test_user_cannot_delete_others_products(self):
        """Обычный пользователь не может удалять чужие объявления"""

        client = self.user_clients[0]
        ad_id = self.ad_ids[1]

        response = client.delete(f"{self.URL}{ad_id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_all_products(self):
        """Админ может удалять все объявления"""

        admin_client = self.user_clients[1]

        for ad_id in self.ad_ids:
            response = admin_client.delete(f"{self.URL}{ad_id}/")
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            response = admin_client.get(f"{self.URL}")
            self.assertTrue(
                ad_id not in [ad["pk"] for ad in response.json()["results"]]
            )

        response = APIClient().get(f"{self.URL}")
        self.assertEqual(len(response.json()["results"]), 0)
