from django.urls import path

from .views import *


urlpatterns = [
    path('', Main.as_view(), name='home_page_url'),
    path('create-user/', CreateAnUser.as_view(), name='create_user_url'),
    path('create-employee/', CreateAnEmployee.as_view(), name='create_employee_url'),
    path('login/', Login.as_view(), name='login_url'),
    path('personal-area/', PersonalArea.as_view(), name='personal_area_url'),
    path('logout/', logout_view, name='logout_url'),
]
