
from django.urls import path, include

from . import admin
from .views import (AdsList, AdsDetail, AdsCreate, AdsUpdate, AdsDelete, ReplyCreate, CategoryListView, ReplyDetail, ReplyDelete, ReplyList, notifi_reply, subscribe)

#admin.site.site_header = 'GeeksForGeeks'
#admin.site.site_title = 'GeeksForGeeks'
#admin.site.index_title = 'GeeksForGeeks Administration'

urlpatterns = [
   path('', AdsList.as_view(), name='post_list'),
   path('<int:pk>', AdsDetail.as_view(), name='ads_detail'),
   path('create/', AdsCreate.as_view(), name='ads_create'),
   path('<int:pk>/update/', AdsUpdate.as_view(), name='ads_update'),
   path('<int:pk>/delete/', AdsDelete.as_view(), name='ads_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('<int:pk>/reply/', ReplyCreate.as_view(), name='reply_create'),
   path('replys/<int:pk>', ReplyDetail.as_view(), name='replys'),
   path('replys/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
   path('<int:pk>/allreplys', ReplyList.as_view(), name='all_replys'),
   path('replys/<int:pk>/notifi', notifi_reply, name='notifi'),
   path('editor/', include('django_summernote.urls')),

]