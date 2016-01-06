"""umm_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^umm/admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('^auth/', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'umm_app.views.home'),
    url(r'^task/', "umm_app.views.tasks", name="tasks"),
    url(r'^auth/error/', "umm_app.views.auth_error", name="error"),
    url(r'^login/', "umm_app.views.home", name=""),
    url(r'^umm/$', "umm_app.views.home1", name="home1"),
    url(r'^task_list/(?P<cat_id>\d+)/', 'umm_app.views.task_list', name='task_list'),
    url(r'^left_column_list/(?P<task_id>\d+)/', 'umm_app.views.left_column_list', name='left_column_list'),
    url(r'^elevator_pitch_data/(?P<task_id>\d+)/', 'umm_app.views.elevator_pitch_data', name='elevator_pitch_data'),
    url(r'^right_column_list/(?P<task_id>\d+)/', 'umm_app.views.right_column_list', name='right_column_list'),
    url(r'^combodata/$', 'umm_app.views.combo_data', name='combo_data'),
    url(r'^budget_band/$', 'umm_app.views.budget_band', name='budget_band'),
    url(r'^_ah/', include('djangae.urls')),
]
