import json

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
        User.objects.create(username='not_allowed_1', password='CanDoNothing1')
        User.objects.create(username='not_allowed_2', password='CanDoNothing2')

    def test_get_all_users_200(self):
        user = User.objects.get(username='first_superuser')
        client.force_login(user)
        response = client.get(reverse('get_all_users'), )

        # URL and user are valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response.data length must be equal records count from DB
        users = User.objects.all()
        self.assertEqual(len(users), len(response.data))

        # response field are relevant to serializer's fields
        if len(response.data) > 0:
            self.assertEqual([x for x in response.data[0].keys()],
                             ['id', 'username', 'is_superuser', 'is_staff', 'is_active'])

    def test_get_all_users_403(self):
        user = User.objects.get(username='not_allowed_1')
        client.force_login(user)
        response = client.get(reverse('get_all_users'), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetAllStatesTest(TestCase):
    """ GET all states using API """

    def setUp(self):
        User.objects.create(username='first_stuff', password='ReadOnly001', is_staff=True)
        User.objects.create(username='not_allowed_1', password='CanDoNothing1')

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

        # response.data length must be equal records count from DB
        states = State.objects.all()
        self.assertEqual(len(states), len(response.data))

        # response field are relevant to serializer's fields
        if len(response.data) > 0:
            self.assertEqual([x for x in response.data[0].keys()], ['id', 'name'])

    def test_get_all_states_403(self):
        user = User.objects.get(username='not_allowed_1')
        client.force_login(user)
        response = client.get(reverse('get_all_states'), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetAllCategoriesTest(TestCase):
    """ GET all categories using API """

    def setUp(self):
        User.objects.create(username='first_stuff', password='ReadOnly001', is_staff=True)
        User.objects.create(username='not_allowed_1', password='CanDoNothing1')

        Category.objects.create(name='Bug')
        Category.objects.create(name='Docs')
        Category.objects.create(name='Fix')

    def test_get_all_categories_200(self):
        user = User.objects.get(username='first_stuff')
        client.force_login(user)
        response = client.get(reverse('get_all_categories'), )

        # URL and user are valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response.data length must be equal records count from DB
        categories = Category.objects.all()
        self.assertEqual(len(categories), len(response.data))

        # response field are relevant to serializer's fields
        if len(response.data) > 0:
            self.assertEqual([x for x in response.data[0].keys()], ['id', 'name'])

    def test_get_all_categories_403(self):
        user = User.objects.get(username='not_allowed_1')
        client.force_login(user)
        response = client.get(reverse('get_all_categories'), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class IssuesAPITest(TestCase):
    """ Tests for Issue model using API """

    def setUp(self):
        State.objects.create(name='New', mark_issue_as_finished=False)
        State.objects.create(name='In progress', mark_issue_as_finished=False)
        State.objects.create(name='Delayed', mark_issue_as_finished=False)
        State.objects.create(name='Finished', mark_issue_as_finished=True)

        Category.objects.create(name='Bug')
        Category.objects.create(name='Docs')
        Category.objects.create(name='Fix')

        User.objects.create(username='first_superuser', password='Super001', is_superuser=True, is_staff=True)
        User.objects.create(username='second_superuser', password='Super002', is_superuser=True, is_staff=True)
        User.objects.create(username='first_staff', password='ReadOnly001', is_staff=True)
        User.objects.create(username='second_staff', password='ReadOnly002', is_staff=True)
        User.objects.create(username='not_allowed_1', password='CanDoNothing1')
        User.objects.create(username='not_allowed_2', password='CanDoNothing2')

        Issue.objects.create(name='Test bug', description='Bug...', category=Category.objects.get(name='Bug'),
                             state=State.objects.get(name='New'), creator=User.objects.get(username='first_superuser'),
                             responsible_person=User.objects.get(username='first_superuser'))
        Issue.objects.create(name='Misspellings', description='Article 123', category=Category.objects.get(name='Docs'),
                             state=State.objects.get(name='New'), creator=User.objects.get(username='first_superuser'),
                             responsible_person=User.objects.get(username='first_superuser'))
        Issue.objects.create(name='Bug 42', description='Bug from Movie 42', category=Category.objects.get(name='Bug'),
                             state=State.objects.get(name='New'), creator=User.objects.get(username='first_superuser'),
                             responsible_person=User.objects.get(username='first_superuser'))

    def test_get_all_issues_200(self):
        user = User.objects.get(username='first_staff')
        client.force_login(user)
        response = client.get(reverse('get_post_issues'), )

        # URL and user are valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response.data length must be equal records count from DB
        self.assertEqual(len(Issue.objects.all()), len(response.data))

        # response field are relevant to serializer's fields
        if len(response.data) > 0:
            self.assertEqual([x for x in response.data[0].keys()],
                             ['id', 'name', 'creator_id', 'responsible_person_id', 'description', 'state_id',
                              'category_id', 'created_at', 'finished_at'])

    def test_get_all_issues_403(self):
        user = User.objects.get(username='not_allowed_1')
        client.force_login(user)
        response = client.get(reverse('get_post_issues'), )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_issue_201_and_403(self):
        valid_payload = {'name': 'Add a new function', 'description': 'Add a new function for counting mushrooms',
                         'creator_id': User.objects.get(username='second_superuser').id,
                         'responsible_person_id': User.objects.get(username='second_superuser').id,
                         'state_id': State.objects.get(name='New').id, 'created_at': '2021-09-04T22:38:48',
                         'category_id': Category.objects.get(name='Docs').id, 'finished_at': None}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.post(reverse('get_post_issues'), data=json.dumps(valid_payload),
                               content_type='application/json')
        # OK
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # User 'not_allowed_1' is not allowed to create
        user = User.objects.get(username='not_allowed_1')
        client.force_login(user)
        response = client.post(reverse('get_post_issues'), data=json.dumps(valid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_issue_empty_name(self):
        invalid_payload = {'description': 'Add a new function for counting mushrooms',
                           'creator_id': User.objects.get(username='second_superuser').id,
                           'responsible_person_id': User.objects.get(username='second_superuser').id,
                           'state_id': State.objects.get(name='New').id, 'created_at': '2021-09-04T22:38:48',
                           'category_id': Category.objects.get(name='Docs').id, 'finished_at': None}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.post(reverse('get_post_issues'), data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_issue_empty_description(self):
        invalid_payload = {'name': 'Add a new function',
                           'creator_id': User.objects.get(username='second_superuser').id,
                           'responsible_person_id': User.objects.get(username='second_superuser').id,
                           'state_id': State.objects.get(name='New').id, 'created_at': '2021-09-04T22:38:48',
                           'category_id': Category.objects.get(name='Docs').id, 'finished_at': None}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.post(reverse('get_post_issues'), data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_issue_wrong_creator_id(self):
        invalid_payload = {'name': 'Add a new function', 'description': 'Add a new function for counting mushrooms',
                           'creator_id': -1,
                           'responsible_person_id': User.objects.get(username='second_superuser').id,
                           'state_id': State.objects.get(name='New').id, 'created_at': '2021-09-04T22:38:48',
                           'category_id': Category.objects.get(name='Docs').id, 'finished_at': None}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.post(reverse('get_post_issues'), data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_issue_wrong_responsible_person_id(self):
        invalid_payload = {'name': 'Add a new function', 'description': 'Add a new function for counting mushrooms',
                           'creator_id': User.objects.get(username='second_superuser').id,
                           'responsible_person_id': -1,
                           'state_id': State.objects.get(name='New').id, 'created_at': '2021-09-04T22:38:48',
                           'category_id': Category.objects.get(name='Docs').id, 'finished_at': None}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.post(reverse('get_post_issues'), data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # finished_at can not be earlier than created_at
    def test_create_issue_finished_before_was_created(self):
        invalid_payload = {'name': 'Add a new function', 'description': 'Add a new function for counting mushrooms',
                           'creator_id': User.objects.get(username='second_superuser').id,
                           'responsible_person_id': User.objects.get(username='second_superuser').id,
                           'state_id': State.objects.get(name='New').id, 'created_at': '2021-09-04T22:38:48',
                           'category_id': Category.objects.get(name='Docs').id, 'finished_at': '2021-08-04T22:38:48'}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.post(reverse('get_post_issues'), data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # finished_at can not be set with non-relevant state (state.mark_issue_as_finished == False)
    def test_create_issue_finished_at_with_non_relevant_state(self):
        invalid_payload = {'name': 'Add a new function', 'description': 'Add a new function for counting mushrooms',
                           'creator_id': User.objects.get(username='second_superuser').id,
                           'responsible_person_id': User.objects.get(username='second_superuser').id,
                           'state_id': State.objects.get(name='New').id, 'created_at': '2021-09-04T22:38:48',
                           'category_id': Category.objects.get(name='Docs').id, 'finished_at': '2021-09-05T22:38:48'}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.post(reverse('get_post_issues'), data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Only superuser can be a creator
    def test_create_issue_creator_is_superuser(self):
        invalid_payload = {'name': 'Add a new function', 'description': 'Add a new function for counting mushrooms',
                           'creator_id': User.objects.get(username='first_staff').id,
                           'responsible_person_id': User.objects.get(username='second_superuser').id,
                           'state_id': State.objects.get(name='New').id, 'created_at': '2021-09-04T22:38:48',
                           'category_id': Category.objects.get(name='Docs').id, 'finished_at': None}
        user = User.objects.get(username='first_superuser')
        client.force_login(user)
        response = client.post(reverse('get_post_issues'), data=json.dumps(invalid_payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_valid_single_issue(self):
        user = User.objects.get(username='first_superuser')
        client.force_login(user)
        response = client.get(reverse('get_delete_update_issue', kwargs={'pk': Issue.objects.get(name='Test bug').id}))

        # URL and user are valid
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response field are relevant to serializer's fields
        self.assertEqual([x for x in response.data.keys()],
                         ['id', 'name', 'creator_id', 'responsible_person_id', 'description', 'state_id','category_id',
                          'created_at', 'finished_at'])

    def test_get_single_issue_404(self):
        user = User.objects.get(username='first_superuser')
        client.force_login(user)
        response = client.get(reverse('get_delete_update_issue', kwargs={'pk': 999999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_single_issue_403(self):
        user = User.objects.get(username='not_allowed_1')
        client.force_login(user)
        response = client.get(reverse('get_delete_update_issue', kwargs={'pk': Issue.objects.get(name='Test bug').id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_issue_valid(self):
        user = User.objects.get(username='first_superuser')
        client.force_login(user)
        response = client.delete(reverse('get_delete_update_issue',
                                         kwargs={'pk': Issue.objects.get(name='Test bug').id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_issue_404(self):
        user = User.objects.get(username='first_superuser')
        client.force_login(user)
        response = client.delete(reverse('get_delete_update_issue', kwargs={'pk': 999999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_issue_403(self):
        user = User.objects.get(username='not_allowed_1')
        client.force_login(user)
        response = client.delete(reverse('get_delete_update_issue',
                                         kwargs={'pk': Issue.objects.get(name='Misspellings').id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_issue_201_and_403(self):
        valid_payload = {'name': 'Add more small functions', 'description': 'Divide and conquer',
                         'creator_id': User.objects.get(username='second_superuser').id,
                         'responsible_person_id': User.objects.get(username='second_superuser').id,
                         'state_id': State.objects.get(name='New').id, 'created_at': '2021-09-04T22:38:48',
                         'category_id': Category.objects.get(name='Docs').id, 'finished_at': None}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.put(reverse('get_delete_update_issue',
                                      kwargs={'pk': Issue.objects.get(name='Misspellings').id}),
                              data=json.dumps(valid_payload), content_type='application/json')
        # OK
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # response field are relevant to serializer's fields
        self.assertEqual([x for x in response.data.keys()],
                         ['id', 'name', 'creator_id', 'responsible_person_id', 'description', 'state_id', 'category_id',
                          'created_at', 'finished_at'])

        # User 'not_allowed_1' is not allowed to create
        user = User.objects.get(username='not_allowed_1')
        client.force_login(user)
        response = client.put(reverse('get_delete_update_issue', kwargs={'pk': Issue.objects.get(name='Bug 42').id}),
                              data=json.dumps(valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_issue_name_only(self):
        valid_payload = {'name': 'Bug-42'}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.put(reverse('get_delete_update_issue', kwargs={'pk': Issue.objects.get(name='Bug 42').id}),
                              data=json.dumps(valid_payload), content_type='application/json')
        # OK
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # response field are relevant to serializer's fields
        self.assertEqual([x for x in response.data.keys()],
                         ['id', 'name', 'creator_id', 'responsible_person_id', 'description', 'state_id', 'category_id',
                          'created_at', 'finished_at'])

    def test_update_issue_description_only(self):
        valid_payload = {'description': 'Description for bug-42'}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.put(reverse('get_delete_update_issue', kwargs={'pk': Issue.objects.get(name='Bug 42').id}),
                              data=json.dumps(valid_payload), content_type='application/json')
        # OK
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # response field are relevant to serializer's fields
        self.assertEqual([x for x in response.data.keys()],
                         ['id', 'name', 'creator_id', 'responsible_person_id', 'description', 'state_id', 'category_id',
                          'created_at', 'finished_at'])

        # Check if missed fields were not overwritten with default values
        issue = Issue.objects.get(name='Bug 42')
        is_ok = all(
                    (issue.name == response.data['name'], issue.creator.id == response.data['creator_id'],
                     issue.responsible_person.id == response.data['responsible_person_id'],
                     issue.state.id == response.data['state_id'], issue.category.id == response.data['category_id'],
                     str(issue.created_at) == response.data['created_at'].replace('T', ' '),
                     issue.finished_at == response.data['finished_at'])
                    )
        self.assertEqual(is_ok, True)

    # finished_at can not be earlier than created_at
    def test_update_issue_invalid_finished_at(self):
        valid_payload = {'finished_at': '2020-09-04T22:38:48', 'state_id': State.objects.get(name='Finished').id}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.put(reverse('get_delete_update_issue', kwargs={'pk': Issue.objects.get(name='Bug 42').id}),
                              data=json.dumps(valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # finished_at can not be set with non-relevant state (state.mark_issue_as_finished == False)
    def test_update_issue_invalid_finished_at_with_non_relevant_state(self):
        valid_payload = {'finished_at': '2021-09-06T16:30:48', 'state_id': State.objects.get(name='New').id}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.put(reverse('get_delete_update_issue', kwargs={'pk': Issue.objects.get(name='Bug 42').id}),
                              data=json.dumps(valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Only superuser can be a creator
    def test_update_issue_invalid_creator(self):
        valid_payload = {'creator_id': User.objects.get(username='second_staff').id}
        user = User.objects.get(username='second_superuser')
        client.force_login(user)
        response = client.put(reverse('get_delete_update_issue', kwargs={'pk': Issue.objects.get(name='Bug 42').id}),
                              data=json.dumps(valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
