from django.urls import path
from .views import SetupView

app_name = "Pimoduleapp"

urlpatterns =[
    path('setup/<str:pk>',SetupView.as_view(),name='setup') #endpoint to setup the device attributes
]