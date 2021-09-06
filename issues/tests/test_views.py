from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Issue, State, Category


client = Client()


class GetAllUsersTest(TestCase):
    """ GET all users using API """

    def setUp(self):
        User.objects.create(username='first_superuser', password='Super001', is_superuser=True, is_staff=True)
        User.objects.create(username='second_superuser', password='Super002', is_superuser=True, is_staff=True)
        User.objects.create(username='first_stuff', password='ReadOnly001', is_staff=True)
        User.objects.create(username='second_stuff', password='ReadOnly002', is_staff=True)
        User.objects.create(username='no_allowed_1', password='CanDoNothing1')
        User.objects.create(username='no_allowed_2', password='CanDoNothing2')

    def test_get_all_users_200(self):
        user = User.objects.get(username='first_superuser')
        client.force_login(user)
        response = client.get(reverse('get_all_users'), )

        # URL and user are valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response.data length must be equal User's records count from DB
        users = User.objects.all()
        self.assertEqual(len(users), len(response.data))

        # response field are relevant to serializer's fields
        if len(response.data) > 0:
            self.assertEqual([x for x in response.data[0].keys()],
                             ['id', 'username', 'is_superuser', 'is_staff', 'is_active'])

    def test_get_all_users_403(self):
        user = User.objects.get(username='no_allowed_1')
        client.force_login(user)
        response = client.get(reverse('get_all_users'), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetAllStatesTest(TestCase):
    """ GET all states using API """

    def setUp(self):
        User.objects.create(username='first_stuff', password='ReadOnly001', is_staff=True)
        User.objects.create(username='no_allowed_1', password='CanDoNothing1')

        State.objects.create(name='New', mark_issue_as_finished=False)
        State.objects.create(name='In progress', mark_issue_as_finished=False)
        State.objects.create(name='Delayed', mark_issue_as_finished=False)
        State.objects.create(name='Finished', mark_issue_as_finished=True)

    def test_get_all_states_200(self):
        user = User.objects.get(username='first_stuff')
        client.force_login(user)
        response = client.get(reverse('get_all_states'), )

        # URL and user are valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response.data length must be equal User's records count from DB
        states = State.objects.all()
        self.assertEqual(len(states), len(response.data))

        # response field are relevant to serializer's fields
        if len(response.data) > 0:
            self.assertEqual([x for x in response.data[0].keys()], ['id', 'name'])

    def test_get_all_states_403(self):
        user = User.objects.get(username='no_allowed_1')
        client.force_login(user)
        response = client.get(reverse('get_all_states'), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetAllCategoriesTest(TestCase):
    """ GET all categories using API """

    def setUp(self):
        User.objects.create(username='first_stuff', password='ReadOnly001', is_staff=True)
        User.objects.create(username='no_allowed_1', password='CanDoNothing1')

        Category.objects.create(name='Bug')
        Category.objects.create(name='Docs')
        Category.objects.create(name='Fix')

    def test_get_all_categories_200(self):
        user = User.objects.get(username='first_stuff')
        client.force_login(user)
        response = client.get(reverse('get_all_categories'), )

        # URL and user are valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response.data length must be equal User's records count from DB
        categories = Category.objects.all()
        self.assertEqual(len(categories), len(response.data))

        # response field are relevant to serializer's fields
        if len(response.data) > 0:
            self.assertEqual([x for x in response.data[0].keys()], ['id', 'name'])

    def test_get_all_categories_403(self):
        user = User.objects.get(username='no_allowed_1')
        client.force_login(user)
        response = client.get(reverse('get_all_categories'), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
