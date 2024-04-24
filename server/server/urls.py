from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from services.urls import router as servicesRouter
from users.urls import router as usersRouter
from patches import routers

router = routers.DefaultRouter()
router.extend(servicesRouter)
router.extend(usersRouter)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # path("api/", include('services.urls')),
]
