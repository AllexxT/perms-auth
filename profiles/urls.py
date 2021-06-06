from django.urls import path, include

from profiles import views


urlpatterns = [
    # path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("details/", views.ProfileDetailsView.as_view(), name="details"),
    path("verify/", views.VerificationView.as_view(), name="verify")

]
