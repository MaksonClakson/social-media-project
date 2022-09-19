from api import views
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'customers', views.CustomerAllViewSet)
router.register(r'customer', views.CustomerViewSet)
urlpatterns = router.urls