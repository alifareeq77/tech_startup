from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from my_api import views

urlpatterns = [
                  path('index', views.get_view),
                  path('', views.get_it),
                  path('<id>', views.get_it_id),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
