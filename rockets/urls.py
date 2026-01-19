from django.urls import path
from . import views

urlpatterns = [
    # Главная
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    
    # Ракеты
    path('rockets/', views.rocket_list, name='rocket_list'),
    path('rockets/<int:pk>/', views.rocket_detail, name='rocket_detail'),
    path('rockets/add/', views.rocket_create, name='rocket_create'),
    path('rockets/<int:pk>/edit/', views.rocket_edit, name='rocket_edit'),
    path('rockets/<int:pk>/delete/', views.rocket_delete, name='rocket_delete'),
    
    # Космодромы
    path('cosmodromes/', views.cosmodrome_list, name='cosmodrome_list'),
    path('cosmodromes/<int:pk>/', views.cosmodrome_detail, name='cosmodrome_detail'),
    path('cosmodromes/add/', views.cosmodrome_create, name='cosmodrome_create'),
    path('cosmodromes/<int:pk>/edit/', views.cosmodrome_edit, name='cosmodrome_edit'),
    path('cosmodromes/<int:pk>/delete/', views.cosmodrome_delete, name='cosmodrome_delete'),
    
    # Запуски
    path('launches/', views.launch_list, name='launch_list'),
    path('launches/<int:pk>/', views.launch_detail, name='launch_detail'),
    path('launches/add/', views.launch_create, name='launch_create'),
    path('launches/<int:pk>/edit/', views.launch_edit, name='launch_edit'),
    path('launches/<int:pk>/delete/', views.launch_delete, name='launch_delete'),
]
