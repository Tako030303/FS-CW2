from django.urls import path
from . import views

app_name = "accounts"


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("manage-users/", views.users_list, name="users_list"),
    path("user/create/", views.user_create, name="user_create"),
    path("user/<int:pk>/edit/", views.user_edit, name="user_edit"),
    path("user/<int:pk>/delete/", views.user_delete, name="user_delete"),
    # path("manage-groups/", views.groups_list, name="groups_list"),
    # path("group/create/", views.group_create, name="group_create"),
    # path("group/<int:pk>/edit/", views.group_edit, name="group_edit"),
    # path("group/<int:pk>/delete/", views.group_delete, name="group_delete"),
]
