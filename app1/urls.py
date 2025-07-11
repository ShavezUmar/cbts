from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('admin/',admin.site.urls),
    path('test',views.test,name='test'),
    path('login1/',views.login1,name='login1'),
    path('mainc/',views.mainc,name='mainc'),
    path('explore/',views.explore,name='explore'),
    path('buyrefundticks/',views.buyrefundticks,name='buyrefundticks'),
    path('payment/',views.payment,name='payment')
]