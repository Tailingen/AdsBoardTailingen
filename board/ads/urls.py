
from django.urls import path
from .views import (AdsList, AdsDetail, AdsCreate, AdsUpdate, AdsDelete, ReplyCreate, CategoryListView, subscribe)


urlpatterns = [
   path('', AdsList.as_view(), name='post_list'),
   path('<int:pk>', AdsDetail.as_view(), name='ads_detail'),
   path('create/', AdsCreate.as_view(), name='ads_create'),
   path('<int:pk>/update/', AdsUpdate.as_view(), name='ads_update'),
   path('<int:pk>/delete/', AdsDelete.as_view(), name='ads_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('<int:pk>/reply/', ReplyCreate.as_view(), name='reply_create'),

]