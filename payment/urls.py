from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title='Payment API')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('paymentMethod.urls')),
    
    path('docs/', schema_view),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)