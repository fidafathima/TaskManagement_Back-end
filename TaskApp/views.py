from django.http import Http404

# Create your views here.
from rest_framework import status, views, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from TaskApp.models import Tasks, UserDetails
from TaskApp.serializer import TaskSerializer, RegisterSerializer


class LoginView(views.APIView):
    def post(self, request):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                return Response({
                    'user': {
                        'id': user.id,
                        'username': user.username
                    },
                    'access': access_token,
                    'refresh': refresh_token
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Account is disabled'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class Task(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer=TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Registration(APIView):
    def get(self,request):
        data=UserDetails.objects.all()
        serializer=RegisterSerializer(data,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            user.is_user = True
            user.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditTask(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,id):
        try:
            return Tasks.objects.get(id=id)
        except Tasks.DoesNotExist:
            raise Http404

    def get(self, request, id):
        task = self.get_object(id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, id):
        task = self.get_object(id)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        task = self.get_object(id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,id):
        try:
            return Tasks.objects.get(id=id)
        except Tasks.DoesNotExist:
            raise Http404

    def post(self,request,id):
        task = self.get_object(id)
        serializer = TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            task1=serializer.save()
            task1.status = True
            task1.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeStatus2(APIView):
    permission_classes = [IsAuthenticated]
    def get_object(self,id):
        try:
            return Tasks.objects.get(id=id)
        except Tasks.DoesNotExist:
            raise Http404

    def post(self,request,id):
        task = self.get_object(id)
        serializer = TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            task1=serializer.save()
            task1.status = False
            task1.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Pending(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        data=Tasks.objects.filter(status=False)
        serializer=TaskSerializer(data,many=True)
        return Response(serializer.data)

class Completed(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        data=Tasks.objects.filter(status=True)
        serializer=TaskSerializer(data,many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]