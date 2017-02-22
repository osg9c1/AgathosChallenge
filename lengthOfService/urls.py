from django.conf.urls.defaults import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from adminviews import UploadCSVView, DownloadSeedFileView
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/upload_seed', UploadCSVView.as_view(), name='uploadSeed'),
    url(r'^admin/download_seed', DownloadSeedFileView.as_view(), name='downloadSeed'),
    url(r'^admin/', include(admin.site.urls)),


)

urlpatterns += staticfiles_urlpatterns()