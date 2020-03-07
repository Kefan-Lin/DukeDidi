from django.urls import path

from . import views

app_name = 'DukeDidi'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('driverRegister/',views.driverRegister,name='driverRegister'),
    path('editDriver/', views.editDriver, name='editDriver'),
    path('requestRide/', views.requestRide, name='requestRide'),
    path('searchSharableRides', views.searchSharableRides, name='searchSharableRides'),
    path('sharableRidesResults', views.sharableRidesResults, name='sharableRidesResults'),
    path('viewNonCompletedRides', views.viewNonCompletedRides, name='viewNonCompletedRides'),
    path('viewOpenRides', views.viewOpenRides, name='viewOpenRides'),
    path('editOpenRide', views.editOpenRide, name='editOpenRide'),
    path('driverDashboard', views.driverDashboard, name='driverDashboard'),
    path('driverOpenRides', views.driverOpenRides, name='driverOpenRides'),
    path('driverSelectRides', views.driverSelectRides, name='driverSelectRides'),
    path('viewConfirmedRides', views.viewConfirmedRides, name='viewConfirmedRides'),
    path('driverViewConfirmedRides', views.driverViewConfirmedRides, name='driverViewConfirmedRides')
]
