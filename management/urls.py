from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
  path('', views.landing,name = 'landing'),
  path('about', views.about,name = 'about'),
  path('home/<user>', views.home,name = 'home'),
  path('new_batch', views.new_batch,name = 'new_batch'),
  path('new_customer/<id>', views.new_customer,name = 'new_customer'),
  path('new_expense/<id>', views.new_expense,name = 'new_expense'),
  path('new_expense_group/<id>', views.new_expense_group,name = 'new_expense_group'),
  path('new_revenue/<id>', views.new_revenue,name = 'new_revenue'),
  path('new_death/<id>', views.new_death,name = 'new_death'),
  path('business/<id>', views.batch,name = 'batch'),
  path('profile/<editor>', views.profile,name = 'profile'),
  path('profile/new/', views.new_profile,name = 'new_profile'),
]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
