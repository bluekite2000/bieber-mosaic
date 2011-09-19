from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from notes.views import *



urlpatterns = patterns(
    '',
    (r'^$','notes.views.upload_page'),

	url(r'^ajax_upload/$','notes.views.ajax_upload',name='ajax_upload'),
    (r'^upload/$','notes.views.upload_page'),


)

