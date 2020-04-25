from rest_framework import generics, mixins, permissions
from .serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

from tasks.models import Task

from accounts.api.permissions import IsOwner


class TaskListAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        qs = Task.objects.filter(user=self.request.user)
        is_completed = self.request.GET.get('isCompleted', None)
        if is_completed is not None:
            try:
                is_completed = int(is_completed)
            except :
                pass
            if is_completed==0:
                qs = qs.filter(is_completed=False)
            elif is_completed ==1:
                qs = qs.filter(is_completed=True)
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskCompletedAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def post(self, request, id, *args, **kwargs):

        try:
            task_obj = Task.objects.get(id=id)
            task_obj.is_completed = True
            task_obj.save()
            return Response({'detail': 'isCompleted is updated'}, status=200)
        except Task.DoesNotExist:
            return Response({'detail': 'error occured'}, status=400)
