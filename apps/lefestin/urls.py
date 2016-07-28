from django.conf.urls import url
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^login$', views.login, name='login'),
	url(r'^register$', views.register, name='register'),
	url(r'^registration$', views.registration, name='registration'),
	url(r'^home/(?P<id>\d+)$', views.home, name = 'home'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^addgroup$', views.addgroup, name='addgroup'),
	url(r'^process_addgroup$', views.process_addgroup, name='process_addgroup'),
	url(r'^deletegroup/(?P<id>\d+)$', views.deletegroup, name='deletegroup'),
	url(r'^user/create/recipe$', views.create_recipe, name='create_recipe'),
	url(r'^user/create/recipe/process$', views.create_recipe_process, name='create_recipe_process'),
	url(r'^delete/all/recipe$', views.delete_recipe, name='delete_recipe'),
]
