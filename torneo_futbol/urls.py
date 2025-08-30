from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('torneos.urls')),  # Aquí cargamos las APIs de torneos
]
