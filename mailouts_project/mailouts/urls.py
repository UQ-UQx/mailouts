from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^importdata$', views.import_csv, name='importdata'),
    url(r'^unsubscribe$', views.unsubscribe, name='unsubscribe'),
    url(r'^newsletter$', views.newsletter, name='newsletter'),
    url(r'^newsletterpreview$', views.newsletterpreview, name='newsletterpreview'),
    url(r'^unsubscribe/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<validation_hash>[a-fA-F\d]{32})/$', views.updateoptout_db, name='unsubscribedb'),
]
