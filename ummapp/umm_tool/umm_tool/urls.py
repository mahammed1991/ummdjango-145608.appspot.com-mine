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
    url(r'^apollo/$', "umm_app.views.apollo_home", name="apollo_home"),
    url(r'^umm/manage-admin/','umm_app.views.manage_admin', name='manage_admin'),
    url(r'^umm/create-process/','umm_app.views.create_process', name='create_process'),
    url(r'^umm/view-process/','umm_app.views.view_process', name='view_process'),
    url(r'^umm/update-process/(?P<pk>[0-9]+)$','umm_app.views.update_process', name='update_process'),
    url(r'^umm/create-program-type/','umm_app.views.create_program_type', name='create_program_type'),
    url(r'^umm/view-program-type/','umm_app.views.view_program_type', name='view_program_type'),
    url(r'^umm/update-program-type/(?P<pk>[0-9]+)$','umm_app.views.update_program_type', name='update_program_type'),
    url(r'^umm/create-program-task/','umm_app.views.create_program_task', name='create_program_task'),
    url(r'^umm/view-program-task/','umm_app.views.view_program_task', name='view_program_task'),
    url(r'^umm/update-program-task/(?P<pk>[0-9]+)$','umm_app.views.update_program_task', name='update_program_task'),
    #url(r'^umm/create-task-data/','umm_app.views.create_task_data', name='create_task_data'),

    url(r'^create/','umm_app.views.create', name='create'),
    url(r'^get-process/','umm_app.views.get_process', name='get_process'),
    url(r'^process/(?P<process_id>[0-9]+)/(?P<sub_process>[A-Za-z0-9-]+)/','umm_app.views.create_task_data',name='create_task_data'),
    url(r'^get-program-tasks/(?P<program_type_id>[0-9]+)/','umm_app.views.get_program_tasks',name='get_program_tasks'),
    url(r'^get-column-name/','umm_app.views.get_column_name',name='get_column_name'),
    url(r'^add-task-data/','umm_app.views.add_task_data',name='add_task_data'),
    url(r'^get-task-data/(?P<task_id>[0-9]+)','umm_app.views.get_task_data',name='get_task_data'),
]