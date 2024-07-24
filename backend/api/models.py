from django.db import models

# Create your models here.

class scraped_data(models.Model):
    title = models.CharField(max_length=250,default="")
    uploaddate = models.CharField(max_length=250,default="")
    channelid = models.CharField(max_length=250,default="")
    description = models.TextField( blank=False) 
    video_id = models.CharField(max_length=250,default="")
    video_tags = models.TextField( blank=False) 
    view_count = models.CharField(max_length=250,default="")
    like_count = models.CharField(max_length=250,default="")
    comment_count = models.CharField(max_length=250,default="")
    latitude = models.CharField(max_length=250,default="null")
    longitude = models.CharField(max_length=250,default="null")
    locationDescription = models.CharField(max_length=250,default="null")
    thumbnail = models.CharField(max_length=500,default="null")
    profile = models.CharField(max_length=500,default="null")
    simmilar_video = models.TextField(default="null")
    email_scraping_dis = models.TextField(default="null")
    channel_profile_link = models.CharField(max_length=50,default="null")
    channel_Location = models.CharField(max_length=5,default="null")
    channel_custom_url = models.CharField(max_length=60,default="null")
    channel_Default_language = models.CharField(max_length=10,default="null")
    channel_name = models.CharField(max_length=50,default="null")


class Test(models.Model):
    pass

class prof(models.Model):
    audio_prof = models.TextField(blank=False,default="null")

    Command_prof = models.TextField( blank=False) 
    Command_no_of_prof = models.CharField(max_length=500,default="null")
    Command_who_used_prof_user = models.CharField(max_length=500,default="null")
    Command_who_used_prof_channelid = models.CharField(max_length=500,default="null")
    Command_prof_published_at = models.CharField(max_length=1000,default='null')


class Files(models.Model):
    video = models.FileField()

    
class User(models.Model):
    username = models.CharField(max_length=255, blank=False, default='')
    email = models.CharField(max_length=255, blank=False, default='')
    password = models.CharField(max_length=65, blank=False, default='')