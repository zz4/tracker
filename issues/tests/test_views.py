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
