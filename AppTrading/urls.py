from django.urls import path
from AppTrading import views

urlpatterns = [
    path('', views.home, name='home'),
    path('titre/<str:titre>/', views.home_titre, name='home_titre'),
    path('liste_titre/', views.titre, name='titre'),
    path('home_titre/add_action/<str:titre>',
         views.add_action, name='add_action'),
    path('delete/<str:id>', views.sell_action, name='delete')
]
