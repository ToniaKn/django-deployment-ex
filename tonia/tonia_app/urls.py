from tonia_app import views
from django.conf.urls import url,include


app_name="tonia_app"


urlpatterns = [

    url(r"^register/",views.register,name="register"),
    url(r"^user_login/$",views.user_login,name="user_login"),

]
