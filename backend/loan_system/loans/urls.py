from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanApplicationViewSet

# router = DefaultRouter()
# router.register(r"loans", LoanApplicationViewSet, basename="loan")

# urlpatterns = router.urls

router = DefaultRouter()
router.register(r"loanapplications", LoanApplicationViewSet, basename="loanapplication")

urlpatterns = [
    path("", include(router.urls)),
]
