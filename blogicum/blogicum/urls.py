from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, reverse_lazy

urlpatterns = [
    path('', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('blog:index'),
        ),
        name='registration',
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

handler403 = 'core.views.csrf_failure'
handler404 = 'core.views.page_not_found'
handler500 = 'core.views.internal_server'
