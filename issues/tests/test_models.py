from datetime import datetime

from django.test import TestCase
from django.db import utils
from django.contrib.auth.models import User
from ..models import State, Category, Issue


class StateTest(TestCase):
    """ Test module for State model """

    def setUp(self):
        State.objects.create(name='New', mark_issue_as_finished=False)
        State.objects.create(name='In progress', mark_issue_as_finished=False)
        State.objects.create(name='Delayed', mark_issue_as_finished=False)
        State.objects.create(name='Finished', mark_issue_as_finished=True)
        State.objects.create(name='Canceled', mark_issue_as_finished=True)

    def test_update_name(self):
        new_name = 'Nové'
        state = State.objects.get(name='New')
        state.name = new_name
        state.save()
        self.assertEqual(State.objects.get(name=new_name).name, new_name)

    def test_update_mark_issue_as_finished(self):
        state = State.objects.get(name='Finished')
        state.mark_issue_as_finished = False
        state.save()
        self.assertEqual(State.objects.get(name='Finished').mark_issue_as_finished, False)

    def test_delete(self):
        State.objects.get(name='Canceled').delete()
        self.assertEqual(len(State.objects.filter(name='Canceled')), 0)

    def test_insert_incorrect_name(self):
        state = State.objects.get(name='In progress')
        state.name = 'Finished'
        _integrity_error = False
        try:
            state.save()
        except utils.IntegrityError:
            _integrity_error = True
        self.assertEqual(_integrity_error, True)


class CategoryTest(TestCase):
    """ Test module for Category model """

    def setUp(self):
        Category.objects.create(name='Bug')
        Category.objects.create(name='Docs')
        Category.objects.create(name='Fix')

    def test_update_name(self):
        new_name = 'Changelog'
        state = Category.objects.get(name='Bug')
        state.name = new_name
        state.save()
        self.assertEqual(Category.objects.get(name=new_name).name, new_name)

    def test_delete(self):
        Category.objects.get(name='Docs').delete()
        self.assertEqual(len(Category.objects.filter(name='Docs')), 0)

    def test_insert_incorrect_name(self):
        category = Category.objects.get(name='Bug')
        category.name = 'Fix'
        _integrity_error = False
        try:
            category.save()
        except utils.IntegrityError:
            _integrity_error = True
        self.assertEqual(_integrity_error, True)


class IssueTest(TestCase):
    """ Test module for Issue model """

    def setUp(self):
        State.objects.create(name='New', mark_issue_as_finished=False)
        State.objects.create(name='In progress', mark_issue_as_finished=False)
        State.objects.create(name='Delayed', mark_issue_as_finished=False)
        State.objects.create(name='Finished', mark_issue_as_finished=True)

        Category.objects.create(name='Bug')
        Category.objects.create(name='Docs')
        Category.objects.create(name='Fix')

        User.objects.create(username='first_superuser', password='Super001', is_superuser=True)
        User.objects.create(username='second_superuser', password='Super002', is_superuser=True)
        User.objects.create(username='first_stuff', password='ReadOnly001', is_staff=True)
        User.objects.create(username='second_stuff', password='ReadOnly002', is_staff=True)
        User.objects.create(username='no_allowed_1', password='CanDoNothing1')
        User.objects.create(username='no_allowed_2', password='CanDoNothing2')

    @staticmethod
    def test_create_correct_not_finished_issue():
        user = User.objects.get(username='first_superuser')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Bug')
        Issue.objects.create(name='Bug name', description='Bug description', creator=user, responsible_person=user,
                             state=state, category=category, created_at=datetime(2021, 9, 1, 12, 12, 12))

    @staticmethod
    def test_create_correct_finished_issue():
        user = User.objects.get(username='first_superuser')
        state = State.objects.get(name='Finished')
        category = Category.objects.get(name='Bug')
        Issue.objects.create(name='Bug name', description='Bug description', creator=user, responsible_person=user,
                             state=state, category=category, created_at=datetime(2021, 9, 1, 12, 12, 12),
                             finished_at=datetime(2021, 9, 5, 15, 15, 15))

    def test_create_invalid_empty_name(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        _integrity_error = False
        try:
            Issue.objects.create(name=None, description='Bug...', creator=user, state=state, category=category,
                                 responsible_person=user, created_at=datetime(2021, 9, 1, 12, 12, 12))
        except utils.IntegrityError:
            _integrity_error = True
        self.assertEqual(_integrity_error, True)

    def test_create_invalid_empty_description(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        _integrity_error = False
        try:
            Issue.objects.create(name='Bug name', description=None, creator=user, state=state, category=category,
                                 responsible_person=user, created_at=datetime(2021, 9, 1, 12, 12, 12))
        except utils.IntegrityError:
            _integrity_error = True
        self.assertEqual(_integrity_error, True)

    def test_create_invalid_empty_creator(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        _integrity_error = False
        try:
            Issue.objects.create(name='Bug name', description='Description', state=state, category=category,
                                 responsible_person=user, created_at=datetime(2021, 9, 1, 12, 12, 12))
        except utils.IntegrityError:
            _integrity_error = True
        self.assertEqual(_integrity_error, True)

    def test_create_invalid_empty_responsible_person(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        _integrity_error = False
        try:
            Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state, category=category,
                                 created_at=datetime(2021, 9, 1, 12, 12, 12))
        except utils.IntegrityError:
            _integrity_error = True
        self.assertEqual(_integrity_error, True)

    def test_create_invalid_empty_state(self):
        user = User.objects.get(username='first_stuff')
        category = Category.objects.get(name='Docs')
        _integrity_error = False
        try:
            Issue.objects.create(name='Test bug', description='Bug...', creator=user, category=category,
                                 responsible_person=user, created_at=datetime(2021, 9, 1, 12, 12, 12))
        except utils.IntegrityError:
            _integrity_error = True
        self.assertEqual(_integrity_error, True)

    def test_create_invalid_empty_category(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        _integrity_error = False
        try:
            Issue.objects.create(name='Bug name', description='Description', state=state, creator=user,
                                 responsible_person=user, created_at=datetime(2021, 9, 1, 12, 12, 12))
        except utils.IntegrityError:
            _integrity_error = True
        self.assertEqual(_integrity_error, True)

    def test_create_valid_empty_created_at(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        issue = Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state,
                                     category=category, responsible_person=user)
        self.assertEqual(type(issue.created_at), datetime)

    def test_create_valid_empty_finished_at(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        issue = Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state,
                                     category=category, responsible_person=user)
        self.assertEqual(issue.finished_at is None, True)

    def test_update_name_correct(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        issue = Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state,
                                     category=category, responsible_person=user)
        issue.name = 'Modified name'
        issue.save()
        self.assertEqual(Issue.objects.get(pk=issue.id).name, 'Modified name')

    def test_update_description_correct(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        issue = Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state,
                                     category=category, responsible_person=user)
        issue.description = 'Modified description'
        issue.save()
        self.assertEqual(Issue.objects.get(pk=issue.id).description, 'Modified description')

    def test_update_creator_correct(self):
        user = User.objects.get(username='first_stuff')
        new_user = User.objects.get(username='second_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        issue = Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state,
                                     category=category, responsible_person=user)
        issue.creator = new_user
        issue.save()
        self.assertEqual(Issue.objects.get(pk=issue.id).creator.id, new_user.id)

    def test_update_responsible_person_correct(self):
        user = User.objects.get(username='first_stuff')
        new_user = User.objects.get(username='second_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        issue = Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state,
                                     category=category, responsible_person=user)
        issue.responsible_person = new_user
        issue.save()
        self.assertEqual(Issue.objects.get(pk=issue.id).responsible_person.id, new_user.id)

    def test_update_state_correct(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        new_state = State.objects.get(name='Delayed')
        category = Category.objects.get(name='Docs')
        issue = Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state,
                                     category=category, responsible_person=user)
        issue.state = new_state
        issue.save()
        self.assertEqual(Issue.objects.get(pk=issue.id).state.id, new_state.id)

    def test_update_category_correct(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        new_category = Category.objects.get(name='Bug')
        issue = Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state,
                                     category=category, responsible_person=user)
        issue.category = new_category
        issue.save()
        self.assertEqual(Issue.objects.get(pk=issue.id).category.id, new_category.id)

    def test_delete_correct(self):
        user = User.objects.get(username='first_stuff')
        state = State.objects.get(name='New')
        category = Category.objects.get(name='Docs')
        issue = Issue.objects.create(name='Test bug', description='Bug...', creator=user, state=state,
                                     category=category, responsible_person=user)
        issue.delete()
        self.assertEqual(len(Issue.objects.filter(pk=issue.id)), 0)
