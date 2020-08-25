from django.conf.urls import url

from apps.powtoons.api.views import PowtoonListCreate, PowtoonDetails

urlpatterns = [

    url(r'^$',
        PowtoonListCreate.as_view(), name='api_powtoon_list_create'),
    url(r'^(?P<powtoon_id>\d+)/$',
        PowtoonDetails.as_view(), name='api_powtoon_details'),



]
