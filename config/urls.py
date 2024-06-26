from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps import payment

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('admin/', admin.site.urls),
    path('user/', include('apps.user.urls')),

    path('stores/', include('apps.store.urls')),
    path('products/', include('apps.product.urls')),
    path('payment/', include('apps.payment.urls')),
    path('purchase/', include('apps.purchase.urls')),
    path('warehouse/', include('apps.warehouse.urls')),
    path('refund/', include('apps.refund.urls')),
    path('cashs/', include('apps.cash.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler400 = lambda request, exception=None: JsonResponse({'error': 'Bad Request (400)'}, status=400)
handler404 = lambda request, exception=None: JsonResponse({'error': 'Not Found (404)'}, status=404)
handler500 = lambda request, exception=None: JsonResponse({'error': 'Server Error (500)'}, status=500)
