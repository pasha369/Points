from django.conf.urls import url


urlpatterns = [
    url(r'^sign_in$', 'appls.login.views.sign_in', name='login'),        
    url(r'^sign_up$', 'appls.login.views.register', name='register'),  
    url(r'^logout$', 'appls.login.views.user_logout', name='logout'),  
    url(r'^get-user$', 'appls.login.views.get_user', name='get_user'),      
    url(r'^follow$', 'appls.login.views.follow', name='follow'),    
]
