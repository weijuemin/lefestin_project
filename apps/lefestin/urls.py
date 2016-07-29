from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login$', views.login, name='login'),
	url(r'^register$', views.register, name='register'),
	url(r'^registration$', views.registration, name='registration'),
	url(r'^home/(?P<id>\d+)$', views.home, name = 'home'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^addgroup$', views.addgroup, name='addgroup'),
	url(r'^process_addgroup$', views.process_addgroup, name='process_addgroup'),
	# url(r'^showgroup/(?P<id>\d+)$', views.showgroup, name='showgroup'),
	url(r'^search/group/$', views.searchGroup, name="search_group"),
	url(r'^showgroups/$', views.showgroups, name='showgroups'),
	url(r'^deletegroup/(?P<id>\d+)$', views.deletegroup, name='deletegroup'),
	url(r'^user/create/recipe$', views.create_recipe, name='create_recipe'),
	url(r'^user/create/recipe/process$', views.create_recipe_process, name='create_recipe_process'),
	url(r'^show/recipe/(?P<recipe_id>\d+)$', views.show_recipe, name='show_recipe'),
	url(r'^show/recipe/all$', views.showrecipes, name='showrecipes'),
	url(r'^delete/all/recipe$', views.delete_recipe, name='delete_recipe'),
	url(r'^delete/all/groups$',views.delete_all_group),
	url(r'^get/all/groups$',views.getAllGroups)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
