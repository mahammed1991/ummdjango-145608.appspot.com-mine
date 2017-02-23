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
    url(r'^knowledgebase/admin/','umm_app.views.manage_admin', name='manage_admin'),
    
    url(r'^get-program-tasks/(?P<program_type_id>[0-9]+)/','umm_app.views.get_program_tasks',name='get_program_tasks'),
    url(r'^get-column-name/','umm_app.views.get_column_name',name='get_column_name'),
    url(r'^add-task-data/','umm_app.views.add_task_data',name='add_task_data'),
    url(r'^get-task-data/(?P<task_id>[0-9]+)','umm_app.views.get_task_data',name='get_task_data'),
    url(r'^get-carousel-column-name/','umm_app.views.get_carousel_column_name',name='get_carousel_column_name'),
    url(r'^add-carousel-data/','umm_app.views.add_carousel_data',name='add_carousel_data'),
    url(r'^get-carousel-data/(?P<sub_process_id>[0-9]+)','umm_app.views.get_carousel_data',name='get_carousel_data'),
    url(r'^get-addldata-column-name/','umm_app.views.get_addldata_column_name',name='get_addldata_column_name'),
    url(r'^add-addldata/','umm_app.views.add_addldata',name='add_addldata'),
    url(r'^get-addldata/(?P<task_id>[0-9]+)','umm_app.views.get_addldata',name='get_addldata'),
    url(r'^get-subprocess-programdata/(?P<sub_process_id>[0-9]+)','umm_app.views.get_subprocess_programdata',name='get_subprocess_programdata'),
    url(r'^add-subprocess-programdata/(?P<sub_process_id>[0-9]+)','umm_app.views.add_subprocess_programdata',name='add_subprocess_programdata'),
    url(r'^edit-subprocess/(?P<sub_process_id>[0-9]+)','umm_app.views.edit_subprocess',name='edit_subprocess'),
    url(r'^delete-carouseldata/(?P<carousel_data_id>[0-9]+)','umm_app.views.delete_carouseldata',name='delete_carouseldata'),
    url(r'^delete-addldata/(?P<additional_data_id>[0-9]+)','umm_app.views.delete_addldata',name='delete_addldata'),
    url(r'^delete-taskdata/(?P<task_data_id>[0-9]+)','umm_app.views.delete_taskdata',name='delete_taskdata'),
    # API

    # Get all processes
    url(r'^get-process/$','umm_app.views.get_process', name='get_process'),
    # Get All Subprocesses
    url(r'^process/(?P<reference_id>[0-9]+)/subprocesses$', 'umm_app.views.subprocess_handler'),
    # Clone Sub Process
    url(r'^process/(?P<process_id>[0-9]+)/sp/(?P<sprocess_name>[A-Za-z0-9-]+)/clone', 'umm_app.views.clone_subprocess'),

    # Delete Process/Subproccess/Program types/ tasks/ task data/ additional data
    url(r'^process/(?P<process_id>[0-9]+)/delete$', 'umm_app.views.delete_process_handler'),
    url(r'^process/(?P<process_id>[0-9]+)/sp/(?P<sub_process_id>[0-9]+)/delete', 'umm_app.views.delete_subprocess_handler'),
    url(r'^programtype/delete', 'umm_app.views.delete_programs_handler'),
    url(r'^programtask/delete', 'umm_app.views.delete_tasks_handler'),
    url(r'^taskdata/(?P<task_data_id>[0-9]+)/delete', 'umm_app.views.delete_taskdata_handler'),
    url(r'^taskadditionaldata/(?P<additional_data_id>[0-9]+)/delete', 'umm_app.views.delete_additionaldata_handler'),
    url(r'^quaterupdate/(?P<data_id>[0-9]+)/delete', 'umm_app.views.delete_subprocess_level_data'),

    # Views
    url(r'^process/(?P<reference_id>[0-9]+)/show$', 'umm_app.views.subprocess_handler', name='subprocess_handler'),
    url(r'^process/(?P<process_id>[0-9]+)/sp/(?P<sprocess_name>[A-Za-z0-9-]+)/edit','umm_app.views.create_task_data',name=''),
    url(r'^process/create/$','umm_app.views.process_handler', name='process_handler'),
    url(r'^process/(?P<process_id>[0-9]+)/sp/(?P<sprocess_name>[A-Za-z0-9-]+)/view$','umm_app.views.show_process_data', name='show_process_data'),

    url(r'^faq/create/$','umm_app.views.faq_handler', name='faq_handler'),
    url(r'^faq/faq_creater/$','umm_app.views.faq_creater', name='faq_creater'),
    url(r'^faq/all/','umm_app.views.faq_all', name='faq_all'),
    url(r'^faq/edit/', 'umm_app.views.faq_edit', name='faq_edit'), 
    url(r'^faq/faq_update/', 'umm_app.views.faq_update', name='faq_update'),
    url(r'^faq/faq_delete/', 'umm_app.views.faq_delete', name='faq_delete'),
    url(r'^faq/home_view/', 'umm_app.views.faq_home_view', name='faq_home_view'),
    url(r'^faq/get_faq/', 'umm_app.views.get_faq', name='get_faq'),
    url(r'^faq/faq_creater/user_question/', 'umm_app.views.user_question', name='user_question'),
    
    #Quality Framework
    url(r'^qf/home/', 'umm_app.views.qf_home', name='qf_home'),
    url(r'^qualityframework/create/$','umm_app.views.qualityframework_handler', name='qualityframework_handler'),
    url(r'^get-qualityframework-name/$','umm_app.views.get_qualityframework_name', name='get_qualityframework_name'),
    url(r'^qualityframework/all/$','umm_app.views.get_qualityframework', name='get_qualityframework'),
    url(r'^qf/qf_delete/(?P<qf_id>[0-9]+)$', 'umm_app.views.delete_qualityframework'),
    url(r'^get-qf-data/(?P<qf_id>[0-9]+)','umm_app.views.get_qf_data',name='get_qf_data'),
    url(r'^qualityframework/update/','umm_app.views.qf_update',name='qf_update'),
    
]