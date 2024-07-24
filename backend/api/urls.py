from django.urls import path
# from .views import Piechart,csvconverter,title_list,YouTubeMetadataView,get_all_meta_data,LoginAPI,LogoutAPI,RegisterAPI,Similar_video,download_video,Profanity
from knox import views as knox_views
from .views import *

urlpatterns = [
    #path('download/', download_video, name='download_video'),
    path('list/',title_list),#### To remove 


    path('download/', download_video, name='download_video'),
    path('display/', Profanity.as_view(), name='display data'),#To remove
    path('download/', get_all_meta_data, name='display data'),#To remove
    

    
    
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('register/', RegisterAPI.as_view(), name='register'),
    path('register/', RegisterAPI.as_view(), name='register'),


    path('csv/<str:video_id>/', csvconverter.as_view(), name='Put id in get'),###Test if need 
    


    path('metadata/', YouTubeMetadataView.as_view(), name='need video_id'),
    path('similarvideo/', SimilarVideo.as_view(), name='need video_id'),
    path('chat/', ChatProfanity.as_view(), name='need video_id'),
    path('video/',  VideoProfanity.as_view(), name='need url'),
    path('test/',  VideoDownload.as_view(), name='need url'),
]