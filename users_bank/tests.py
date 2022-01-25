from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Customer


class TestCustomer(APITestCase):
    """ Test class for the "users" endpoint
    """

    def setUp(self):
        """ Prepares the data required for the tests (url, sensor, standardScaler, ...)
        """
        self.user1 = User.objects.create_user('user1', '', 'password1')
        self.user2 = User.objects.create_user('user2', '', 'password2')
        self.user1.save()
        self.user2.save()
        self.customer1 = {
            "first_name": "Clark",
            "last_name": "Kent",
            "iban": "ATRE123SFDQFFBDB123132132323",
        }
        self.customer2 = {
            "first_name": "Bruce",
            "last_name": "Wayne",
            "iban": "ATRE123SFDQFFBDB123132132323"
        }

        self.list_create_url = reverse("user-list")
        self.client = APIClient()

    def test_list(self):
        """ Tests the create and get request
        Test if the request works, handles authentication and if the parameter's validation is valid
        """
        # Test with user not authenticated
        rsp = self.client.post(self.list_create_url, self.customer1, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticates user
        self.client.force_authenticate(user=self.user1)

        # Correct test. We've used the valid requirements.
        # NB: problem here
        rsp = self.client.post(self.list_create_url, self.customer1, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_201_CREATED)

        # Test with wrong request. We've used the valid requirements.
        rsp = self.client.put(self.list_create_url, self.customer1, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test error : IBAN not matching the correct format
        rsp = self.client.post(self.list_create_url,
                               {"first_name": "Dwayne",
                                "last_name": "Johnson",
                                "iban": "'(-è_çà)'"
                                },
                               format="json")
        self.assertEqual(rsp.status_code, status.HTTP_400_BAD_REQUEST)

        # Test error : Empty argument
        rsp = self.client.post(self.list_create_url, {}, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_400_BAD_REQUEST)

        # Test list
        rsp = self.client.get(self.list_create_url, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)

        # Disconnect the test user
        self.client.force_authenticate(user=None)

    def test_detail(self):
        """ Tests the retrieve, delete and update actions on a specific customer.
        Also ensures that the modification actions are reserved to the Customer's creator
        """
        # Authenticates user
        self.client.force_authenticate(user=self.user1)

        # Creates two customers and test if they were created
        Customer.objects.create(first_name='Dwayne', last_name='Johnson', iban='GREATIBAN', creator=self.user1)
        Customer.objects.create(first_name='Clark', last_name='Kent', iban='superiban', creator=self.user2)

        rsp = self.client.get(reverse("user-detail", args=[1]), {}, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        rsp = self.client.get(reverse("user-detail", args=[2]), {}, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
        # 404 if the customer is not found
        rsp = self.client.get(reverse("user-detail", args=[1231]), {}, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_404_NOT_FOUND)

        # update - unauthorized
        rsp = self.client.put(reverse("user-detail", args=[2]),
                              {"first_name": "Bruce", "iban": "EVENBETTERIBAN123"},
                              format="json")
        self.assertEqual(rsp.status_code, status.HTTP_403_FORBIDDEN)
        # update - owner so ok
        rsp = self.client.put(reverse("user-detail", args=[1]),
                              {"first_name": "Bruce", "last_name": "Wayne", "iban": "EVENBETTERIBAN123"},
                              format="json")
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)

        # deletion - unauthorized
        rsp = self.client.delete(reverse("user-detail", args=[2]), {}, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_403_FORBIDDEN)
        # deletion - owner so ok
        rsp = self.client.delete(reverse("user-detail", args=[1]), {}, format="json")
        self.assertEqual(rsp.status_code, status.HTTP_204_NO_CONTENT)
        # Deleted so can not be found anymore
        rsp = self.client.get(reverse("user-detail", args=[1]), format="json")
        self.assertEqual(rsp.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(user=None)
