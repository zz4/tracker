from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Issue
from .serializers import IssueSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_issue(request, pk):
    try:
        issue = Issue.objects.get(pk=pk)
    except Issue.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single issue
    if request.method == 'GET':
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    # update details of a single issue
    if request.method == 'PUT':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = IssueSerializer(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete a single issue
    if request.method == 'DELETE':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def get_post_issues(request):

    # get all issues
    if request.method == 'GET':
        issues = Issue.objects.all()
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    # insert a new record for a issue
    if request.method == 'POST':
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        data = {
            'name': request.data.get('name'),
            'creator': request.data.get('creator'),
            'responsible_person': request.data.get('responsible_person'),
            'description': request.data.get('description'),
            'state': request.data.get('state'),
            'category': request.data.get('category'),
            'created_at': request.data.get('created_at'),
            'finished_at': request.data.get('finished_at')
        }
        serializer = IssueSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
