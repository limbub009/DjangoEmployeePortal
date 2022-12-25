from django.urls import path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from hobbies.views import login_view, sign_up_view, signed_in_view, logout_view, similar_users_view, friend_request_view, search_users_view

from .api import user_api, hobbies_api, create_hobby, update_user_api, update_profile_pic, users_api, get_friend_api, accept_friend_api, decline_friend_api, send_friend_api, users_list_api

from .api import user_api, hobbies_api, create_hobby, update_user_api, update_profile_pic, users_api



urlpatterns = [
    path('signup/', sign_up_view, name='signup'),
    path('signedin/',signed_in_view, name ='signed_in'),
    path('', login_view, name='login_page'),
    path('logout/', logout_view, name='logout'),
    path('similarusers/', similar_users_view, name='similar_users'),
    path('requests/', friend_request_view, name='requests'),
    path('search/', search_users_view, name='search'),

    path('api/user', user_api, name='user api'),
    path('api/users', users_api, name='users api'),
    path('api/hobbies', hobbies_api, name = 'hobbies'),
    path('signedin/create_hobby', create_hobby, name = 'create_hobby'),
    path("api/update_user_api/<int:id>",update_user_api, name = 'update_user_api' ),
    path('api/updateimage', update_profile_pic, name='update_profile_pic'),
    path("api/get_friends", get_friend_api, name = 'get_friends_api' ),
    path("api/send/<int:id>", send_friend_api, name = 'send_friend_api' ),
    path("api/accept/<int:id>",accept_friend_api, name = 'accept_friend_api' ),
    path("api/decline/<int:id>",decline_friend_api, name = 'decline_friend_api' ),
    path("api/users_list/", users_list_api, name = 'users list api' )
]
urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
