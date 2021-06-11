from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from djangoPfm.quickstart import views
from graphene_django.views import GraphQLView
router = routers.DefaultRouter()
router.register(r'news', views.NewsViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("graphql", GraphQLView.as_view(graphiql=True)),
]