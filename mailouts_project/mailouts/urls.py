from django.conf.urls import url
import views

urlpatterns = [
    url(r'^import_csv$', views.import_csv, name='import_csv'),
    url(r'^setuprecipients/$', views.setuprecipients, name='setuprecipients'),
    url(r'^sendnewsletters/$', views.sendnewsletters, name='sendnewsletters'),
    url(r'^newsletter$', views.newsletter, name='newsletter'),
    url(r'^unsubscribe$', views.unsubscribe, name='unsubscribe'),
    url(r'^unsubscribe/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<validation_hash>[a-fA-F\d]{32})/$', views.updateoptout_db, name='unsubscribedb'),
]
