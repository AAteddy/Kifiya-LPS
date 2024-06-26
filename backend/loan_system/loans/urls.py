from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import LoanApplicationViewSet

router = DefaultRouter()
router.register(r"loans", LoanApplicationViewSet, basename="loan")

urlpatterns = router.urls
