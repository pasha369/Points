# -*- coding: utf-8 -*-
from django.conf.urls import url

app_path = 'appls.points.views.'

urlpatterns = [
    # place
    url(r'^add/$', app_path+'place.add_place', name='add'),    
    url(r'^remove/$', 
        app_path+'place.remove_place', name='remove'),    
    url(r'^place-list/$', 
        app_path+'place.place_list', name='place_list'),        
    url(r'^place-detail/$', 
        app_path+'place.get_place_detail', name='place_detail'),        
    url(r'^saveplacephoto/$', 
        app_path+'place.save_place_photo', name='place_photo'),        
    url(r'^get-by-user/$', 
        app_path+'place.get_by_user', name='user_place'),        
    url(r'^get_place_page/$', 
        app_path+'place.get_place_page', name='get_place_page'),        
    url(r'^search/$', 
        app_path+'place.search', name='search'),   
    # place like
    url(r'^place_like/$', 
        app_path+'place.place_like', name='place_like'),   
    url(r'^get_place_likes/$', 
        app_path+'place.get_place_likes', name='get_place_likes'),  
    url(r'^get-favorite/$', 
        app_path+'place.get_favorite_place', name='get_favorite_place'), 
    url(r'^remove-favorite/$', 
        app_path+'place.remove_favorite', name='remove_favorite'), 
    # category
    url(r'^category-list/$', 
        app_path+'category.categort_list', name='get_all'),        
    url(r'^category-places/$', 
        app_path+'category.get_category_places', name='get_category_places'), 

    url(r'^country-list/$', 
        app_path+'country.country_list', name='country_list'), 
    #route
    url(r'^route-detail/$', 
        app_path+'route.get_route_detail', name='get_route_detail'),
    url(r'^route-list/$', 
        app_path+'route.get_route_list', name='get_route_list'),   
    url(r'^remove-route/$', 
        app_path+'route.remove_route', name='remove_route'),   
    url(r'^save-route/$', 
        app_path+'route.save_route', name='save_route'),        
    # trip
    url(r'^add-trip/$', 
        app_path+'trip.create_trip', name='add_trip'), 
    url(r'^get-all/$', 
        app_path+'trip.get_all', name='get_all'),       
    url(r'^subscribe-trip/$', 
        app_path+'trip.subscribe_trip', name='subscribe_trip'),
    url(r'^discard-trip/$', 
        app_path+'trip.discard_trip', name='discard_trip'),
    url(r'^trip-by-user/$', 
        app_path+'trip.get_trip_by_user', name='get_trip_by_user'),    
    url(r'^trip-date/$', 
        app_path+'trip.get_trip_date', name='get_trip_date') 
]
