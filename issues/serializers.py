from datetime import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from .exceptions import IssueException
from .models import Issue, Category, State


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_superuser', 'is_staff', 'is_active',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'name',)


class IssueSerializer(serializers.ModelSerializer):
    creator_id = serializers.IntegerField()
    responsible_person_id = serializers.IntegerField()
    state_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    class Meta:
        model = Issue
        fields = ('id', 'name', 'creator_id', 'responsible_person_id', 'description', 'state_id', 'category_id',
                  'created_at', 'finished_at',)

    # Check if model's instance with given pk exists
    @staticmethod
    def validate_instance_of_model_exists(model, pk):
        model_instance = model.objects.filter(pk=pk)
        if model_instance:
            return model_instance[0]
        else:
            raise IssueException(400, [('chyba', f'{model}: pk {pk} nenalezen')])

    # Check superuser role for creator of issue (staff in not allowed modify issues)
    @staticmethod
    def validate_creator_is_superuser(user):
        if user.is_superuser:
            return user
        else:
            raise IssueException(400, [('chyba', 'Pouze superuser může zadávat issue.')])

    @staticmethod
    def validate_finished_datetime(finished_datetime, create_datetime, state_instance):
        if finished_datetime:
            if finished_datetime < create_datetime:
                # Issue finished time can not be earlier than created time
                raise IssueException(400, [('chyba', 'Hodnota <finished_at> musí být později než <created_at>')])
            elif not state_instance.mark_issue_as_finished:
                # Given issue's state is not for finishing but finished time is not empty
                _long_message = f'<finished_at> není prázdné, ale stav <{state_instance.name}> není pro dokončení issue'
                raise IssueException(400, [('chyba', _long_message)])
        else:
            if state_instance.mark_issue_as_finished:
                # Given issue's state is for finishing but finished time is empty =>
                # => fill finished time as current time
                finished_datetime = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        return finished_datetime

    def create(self, validated_data):
        creator_instance = self.validate_instance_of_model_exists(User, validated_data.pop('creator_id'))
        response_person = self.validate_instance_of_model_exists(User, validated_data.pop('responsible_person_id'))
        state_instance = self.validate_instance_of_model_exists(State, validated_data.pop('state_id'))
        category_instance = self.validate_instance_of_model_exists(Category, validated_data.pop('category_id'))
        finished_datetime = self.validate_finished_datetime(validated_data.pop('finished_at'),
                                                            validated_data.get('created_at'), state_instance)
        new_issue = Issue.objects.create(creator=self.validate_creator_is_superuser(creator_instance),
                                         responsible_person=response_person, state=state_instance,
                                         category=category_instance, finished_at=finished_datetime, **validated_data)
        return new_issue

    def update(self, instance, validated_data):
        creator_instance = self.validate_instance_of_model_exists(User, validated_data.pop('creator_id'))
        response_person = self.validate_instance_of_model_exists(User, validated_data.pop('responsible_person_id'))
        state_instance = self.validate_instance_of_model_exists(State, validated_data.pop('state_id'))
        instance.creator = self.validate_creator_is_superuser(creator_instance)
        instance.responsible_person = response_person
        instance.state = state_instance
        instance.category = self.validate_instance_of_model_exists(Category, validated_data.pop('category_id'))
        instance.finished_at = self.validate_finished_datetime(validated_data.pop('finished_at'),
                                                               validated_data.get('created_at'), state_instance)
        instance.name = validated_data.get('name')
        instance.description = validated_data.get('description')
        instance.created_at = validated_data.get('created_at')
        instance.save()
        return instance
