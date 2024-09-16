

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from TaskApp import views


router = DefaultRouter()
router.register('task', views.TaskViewSet)

urlpatterns = [
    path('LoginView',views.LoginView.as_view(),name='LoginView'),
    path('Task',views.Task.as_view(),name='Task'),
    path('Registration',views.Registration.as_view(),name='Registration'),
    path('EditTask/<uuid:id>/',views.EditTask.as_view(),name='EditTask'),
    path('ChangeStatus/<uuid:id>/',views.ChangeStatus.as_view(),name='ChangeStatus'),
    path('ChangeStatus2/<uuid:id>/',views.ChangeStatus2.as_view(),name='ChangeStatus2'),
    path('Pending',views.Pending.as_view(),name='Pending'),
    path('Completed',views.Completed.as_view(),name='Completed'),
    path('', include(router.urls)),

]