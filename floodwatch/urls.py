from django.contrib import admin
from django.urls import path
from monitor import views
urlpatterns=[path('admin/',admin.site.urls),path('',views.dashboard,name='dashboard'),path('api/readings/',views.readings,name='readings'),path('api/ingest/',views.ingest,name='ingest'),path('api/alerts/',views.alerts,name='alerts')]
