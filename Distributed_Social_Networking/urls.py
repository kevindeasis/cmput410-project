from django.conf.urls import patterns, include, url 
from django.contrib import admin
from SocialNetworkModels import views
from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, routers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)




urlpatterns = patterns('',
    url(r'^$', views.user_login, name = 'user_login'),
    url(r'^login/', views.user_login, name = 'user_login'),
    url(r'^home/', views.home,name='home'), # NEW MAPPING!
    url(r'^post/', views.author_post, name ='author_post'),
    url(r'^profile/', views.profile, name ='profile'),
    url(r'^register/', views.register, name ='register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', views.user_logout, name = 'user_logout'), # NEW MAPPING!
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest/', include(router.urls)),

)

