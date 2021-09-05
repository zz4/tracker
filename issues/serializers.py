from rest_framework import serializers
from .models import Issue


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('name', 'creator', 'responsible_person', 'description', 'state', 'category', 'created_at',
                  'finished_at',)
