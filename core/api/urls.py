from rest_framework import routers

from api import views

router = routers.SimpleRouter()
router.register(r'tags', views.TagAllViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'pages', views.PageAllViewSet)
router.register(r'pages', views.PageViewSet)
router.register(r'posts', views.PostAllViewSet)
router.register(r'posts', views.PostViewSet)
urlpatterns = router.urls
