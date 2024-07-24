from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.views import LogoutView as KnoxLogoutView
from knox.models import AuthToken
from .models import scraped_data,User
from .serializers import scraped_data_Serializer,UserSerializer


import requests
from pytube import YouTube
import requests
import googleapiclient.discovery as discovery
from bs4 import BeautifulSoup
import io
import nltk 
import re
import nltk
import emoji
import statistics
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import googleapiclient.discovery as discovery
from datetime import datetime
import ffmpeg
import whisper
import os
import pandas as pd
import speech_recognition as sr
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech
from .test import new,similar_video_main
from googleapiclient.discovery import build
from textblob import TextBlob
import numpy as np
import googleapiclient.discovery as discovery
import csv
import time
from bs4 import BeautifulSoup


import io
# from apiclient.discovery import build
import nltk 
import nltk
import emoji
import statistics
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from textblob import TextBlob
import googleapiclient.discovery as discovery
import ffmpeg
import whisper
import os
import pandas as pd
import speech_recognition as sr
from .test import new
from googleapiclient.discovery import build



class Comments(APIView):
    def post(self,request):
        url = request.data.get('url')
        

@api_view(['GET','POST'])
def title_list(request):
    if request.method == 'GET':
        titles = scraped_data.objects.all()  #complex data
        serializer = scraped_data_Serializer(titles,many = True)
        return Response(serializer.data)
    
@api_view(['POST'])
def download_video(request):
    url = request.data.get('url')
    yt = YouTube(url)
    video = yt.streams.get_lowest_resolution()
    video_url = video.url
    response = requests.get(video_url)
    content_type = response.headers['content-type']
    content = response.content
    response = HttpResponse(content, content_type)
    response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'
    return response

#scrape youtube meta data
DEVELOPER_KEY = 'AIzaSyBLiy3AiPuc33fl3z2xhLL0Nubv8tKeKp8'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


class csvconverter(APIView):
    def get(self, request, video_id):
        youtube = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        video_response = youtube.videos().list(id=video_id, part='snippet,statistics,recordingDetails').execute()
        channelid = video_response["items"][0]['snippet']['channelId']
        url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet&id={} &key={}'.format(channelid,DEVELOPER_KEY)
        response = requests.get(url)

        if response.status_code == 200:
            channel_data = response.json()['items'][0]['snippet']

        try:
            title = video_response["items"][0]['snippet']['title']
        except:
            title = 'Nil'

        try:
            uploaddate = video_response["items"][0]['snippet']['publishedAt']
        except:
            uploaddate = 'Nil'
        
        try:
            channelid = video_response["items"][0]['snippet']['channelId']
        except:
            channelid = 'Nil'

        try:
            description =video_response['items'][0]['snippet']['description']
        except:
            description = 'Nil'
        try:
            video_id= video_response["items"][0]['etag']
        except:
            video_id = 'Nil'

        try:
            video_tags=video_response["items"][0]['snippet']['tags']
        except:
            video_tags = 'Nil'

        try:    
            view_count=video_response['items'][0]['statistics']['viewCount']
        except:
            view_count ='Nil'

        try:
            like_count=video_response['items'][0]['statistics']['likeCount']
        except:
            like_count='Nil'

        try:
            comment_count=video_response['items'][0]['statistics']['commentCount']
        except:
            comment_count= 'Nil'

        try:
            geoloaction=video_response['items'][0]['recordingDetails']
        except:
            geoloaction='Nil'
        
        try:
            thumbnail=video_response['items'][0]['snippet']['thumbnails']
        except:
            thumbnail='Nil'
            

        video_tags_connected = ""
        for i in video_tags:
            if(i != video_tags[0]):
                video_tags_connected += ","
            video_tags_connected += i
        # return Response(geoloaction)
        try:
            location_description = geoloaction["locationDescription"]

        except:
            location_description='none'
        
        try:
            latitude = geoloaction['location']['latitude']
            longitude = geoloaction['location']['longitude']
        except:
            latitude = 'Nil'
            longitude = 'Nil'
        
        try:
            thumbnail = thumbnail['maxres']['url']
        except:
            thumbnail = 'Nil'


        if response.status_code == 200:
            channel_data = response.json()['items'][0]['snippet']
        else:
            print('Error:', response.status_code)



        # try:
        #     # Call the videos.list method to retrieve the video resource
        #     video_response = youtube.videos().list(part='contentDetails',id=video_id).execute()

        #     # Extract the duration from the video resource
        #     duration = video_response['items'][0]['contentDetails']['duration']

        # except:
        #     duration = None

        
        # duration=str(duration)
        # list1 = []
        # list1[:0] = duration
        # duration2
        # for i in range(len(list1)):
        #     if list1[i] == 'H':
        #         list1[i]='Hours'
        #     if list1[i] == 'M':
        #         list1[i]='Minutes'
        #     if list1[i] == 'S':
        #         list1[i]="Seconds" 

        # for i in range(len(list1)):
        #     if list1[i]=='T':
        #         duration2="".join(list1[i+1:])



        #return Response()
        response_data = {
            'title': title,
            'uploaddate': uploaddate,
            'channelid': channelid,
            'description': description,
            'video_id': video_id,
            'video_tags': video_tags_connected,
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count,
            'locationDescription'  : location_description,
            'latitude' : latitude,
            'longitude' : longitude,
            'thumbnail' : thumbnail,
            'channel_data' : channel_data,
            'profile':channel_data["thumbnails"]["default"]["url"],
            #'duration' : duration2,
        }
        # serializer = scraped_data_Serializer(data = response_data)

        # if serializer.is_valid():
        #     serializer.save()
        # else:
        #     return Response(serializer.errors)
        




        print(channel_data["thumbnails"]["default"]["url"])
        return Response(response_data)
    
class Profanity(APIView):
    def post(self,request):
        video_id = request.data.get('video_id')
        a = profanity(video_id)
        return Response(a)


def profanity(video_id):
    url = 'https://www.youtube.com/watch?v='+video_id+'/'


    yt = YouTube(url)

    # Get the audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Download the audio stream
    output_path = "/content"
    filename = "audio.mp3"
    audio_stream.download(output_path=output_path, filename=filename)

    print(f"Audio downloaded to {output_path}/{filename}")
    model = whisper.load_model("large")
    result = model.transcribe("/content/sample.ogg", fp16=False)
    with open ('writeme.txt', 'w') as file:  
        file.write(str(result["text"]))  

    print(result["text"])


    import pandas as pd
    df=pd.read_csv("profanity/profanity_en.csv")


    with open('writeme.txt', 'r') as file:
        data1=file.read()
        words=data1.split()
        a=[]
        for i in range(len(words)):
            if words[i] in list(df['text']):
                a.append(words[i])
        frequency = {}
        for j in a:
            if j in frequency:
                frequency[j] +=1
            else:
                frequency[j] =1

        list1 = frequency.values() 
        list1_sum=sum(list1)

    print(list1_sum)
        
    with open('Names.csv', 'w') as f:
        for key in frequency.keys():
            f.write("%s, %s\n" % (key, frequency[key]))

    df=pd.read_csv("profanity/profanity_en.csv")

    def countOccurrence(a):
        frequency = {}
        for j in a:
            if j in frequency:
                frequency[j] +=1
            else:
                frequency[j] =1
        
        list1 = frequency.values() 
        list1_sum=sum(list1)
        print(list1_sum)
        print(frequency)


    with open('writeme.txt', 'r') as file:
        data1=file.read()
        words=data1.split()
        a=[]
        for i in range(len(words)):
            if words[i] in list(df['text']):
                a.append(words[i])

    countOccurrence(a)

    

    # field_name=["words",'count']
    # with open('Names.csv', 'w') as f:
    #     for key in frequency1.keys():
    #         f.write("%s, %s\n" % (key, frequency1[key]))

    return a
    




class YouTubeMetadataView(APIView):
    def get(self, request, video_id):
        youtube = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
        video_response = youtube.videos().list(id=video_id, part='snippet,statistics,recordingDetails').execute()
        channelid = video_response["items"][0]['snippet']['channelId']
        url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet&id={} &key={}'.format(channelid,DEVELOPER_KEY)
        response = requests.get(url)

        if response.status_code == 200:
            channel_data = response.json()['items'][0]['snippet']

        try:
            title = video_response["items"][0]['snippet']['title']
        except:
            title = 'Nil'

        try:
            uploaddate = video_response["items"][0]['snippet']['publishedAt']
        except:
            uploaddate = 'Nil'
        
        try:
            channelid = video_response["items"][0]['snippet']['channelId']
        except:
            channelid = 'Nil'

        try:
            description =video_response['items'][0]['snippet']['description']
        except:
            description = 'Nil'
        try:
            video_id= video_response["items"][0]['etag']
        except:
            video_id = 'Nil'

        try:
            video_tags=video_response["items"][0]['snippet']['tags']
        except:
            video_tags = 'Nil'

        try:    
            view_count=video_response['items'][0]['statistics']['viewCount']
        except:
            view_count ='Nil'

        try:
            like_count=video_response['items'][0]['statistics']['likeCount']
        except:
            like_count='Nil'

        try:
            comment_count=video_response['items'][0]['statistics']['commentCount']
        except:
            comment_count= 'Nil'

        try:
            geoloaction=video_response['items'][0]['recordingDetails']
        except:
            geoloaction='Nil'
        
        try:
            thumbnail=video_response['items'][0]['snippet']['thumbnails']
        except:
            thumbnail='Nil'
            

        video_tags_connected = ""
        for i in video_tags:
            if(i != video_tags[0]):
                video_tags_connected += ","
            video_tags_connected += i
        # return Response(geoloaction)
        try:
            location_description = geoloaction["locationDescription"]

        except:
            location_description='none'
        
        try:
            latitude = geoloaction['location']['latitude']
            longitude = geoloaction['location']['longitude']
        except:
            latitude = 'Nil'
            longitude = 'Nil'
        
        try:
            thumbnail = thumbnail['maxres']['url']
        except:
            thumbnail = 'Nil'

        other_important_details=""
        other_important_details = find_email(description)
        # other_important_details = other_important_details +  get_url_from_des(video_id)

        
        if response.status_code == 200:
            channel_data = response.json()['items'][0]['snippet']
        else:
            print('Error:', response.status_code)

        response_data = {
            'title': title,
            'uploaddate': uploaddate,
            'channelid': channelid,
            'description': description,
            'video_id': video_id,
            'video_tags': video_tags_connected,
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count,
            'locationDescription'  : location_description,
            'latitude' : latitude,
            'longitude' : longitude,
            'thumbnail' : thumbnail,
            'channel_data' : channel_data,
            'profile':channel_data["thumbnails"]["default"]["url"],
            'other_important_details' : other_important_details

        }


        print(channel_data["thumbnails"]["default"]["url"])
        return Response(response_data)
    
def find_email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text)
    return emails

def get_url_from_des(video_id):
    youtube = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    video_response = youtube.videos().list(id=video_id, part='snippet,statistics,recordingDetails,contentDetails').execute()
    description =video_response['items'][0]['snippet']['description']
    s = description
    
  

    lst = re.findall('\S+@\S+', s)     

    print(lst) 
    return lst



@api_view(['POST'])
def download_video(request):
    url = request.data.get('url')
    yt = YouTube(url)

    video = yt.streams.get_lowest_resolution()
    video_url = video.url

    response = requests.get(video_url)
    content_type = response.headers['content-type']
    content = response.content
    response = HttpResponse(content, content_type)
    response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'
    return response


class Similar_video(APIView):
    def post(self,request):
        video_id = request.data.get('video_id')
        t= similar_video_main(video_id)
        return Response(t)


def similar_video_main(video_id):

    DEVELOPER_KEY = 'AIzaSyBLiy3AiPuc33fl3z2xhLL0Nubv8tKeKp8'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    youtube = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    video_response = youtube.videos().list(id=video_id, part='snippet,statistics,recordingDetails,contentDetails').execute()
    video_tags=video_response["items"][0]['snippet']['tags']

    # scrapes the title 
    def get_title():
        d = soup.find_all('h1', 'branded-page-header-title')
        for i in d:
            title = i.text.strip().replace('\n',' ').replace(',','').encode('utf-8') 
            f.write(title+',')
            print('\t%s') % (title)

    # scrapes the subscriber count
    def get_subs():
        b = soup.find_all('span', 'about-stat')
        for i in b:
            try:			
                value = i.b.text.strip().replace(',','')					
                if len(b) == 3:
                    f.write(value+',')
                    print('\t%s') %(value)
                elif len(b) == 2:
                    f.write('null,'+ value + ',')
                    print('\tsubs = null\n\t%s') %(value)
                else:
                    f.write('null,null,')
                    print('\tsubs = null\nviews = null')
            except AttributeError:
                pass

    # scrapes the description
    def get_description():
        c = soup.find_all('div', 'about-description')
        if c:
            for i in c:
                description = i.text.strip().replace('\n',' ').replace(',','').encode('utf-8')		
                f.write(description+',')
                print('\t%s') % (description)
                
                regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                                    '{|}~-]+)*(@|\sat\s|\[at\])(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|'
                                    '\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)'))
                
                email = re.search(regex, description)
                if email:
                    if not email.group(0).startswith('//'):
                        print('\tEmail = ' + email.group())
                        f.write(email.group(0)+',')
                        k.write(email.group(0)+',')

                else:
                    print('\tEmail = null')
                    f.write('null,')
        else:
            print('\tDescription = null\n\tEmail = null')
            f.write('null,null,')

    # scrapes all the external links 
    def get_links():
        a = soup.find_all('a', 'about-channel-link ') # trailing space is required.
        for i in a:
            url = i.get('href')
            externalLinks.append(url)
            f.write(url+',')
            print('\t%s') % (url)

    # scrapes the related channels
    def get_related():
        s = soup.find_all('h3', 'yt-lockup-title')
        for i in s:
            t = i.find_all(href=re.compile('user'))
            for i in t:
                url = 'https://www.youtube.com'+i.get('href')
                related.write(url+'\n')
                #print('\t\t%s,%s') % (i.text, url)	

    # create output files
    f = open('meta-data.csv', 'w+')
    k = open('key-data.csv', 'w+')
    related = open('related-channels.csv', 'w+')

    # empy list to save pages we've already scraped
    visited = []

    externalLinks = []

    # disassemble YouTube search result page URL
    base = 'https://www.youtube.com/results?search_query='
    page = '&page='
    q = video_tags # enumerate all keywords here
    count = 1 # start on page 1
    pagesToScrape = 1 # the number of search result pages to scrape
    timeToSleep = 3 # the number of seconds between pings to the YouTube server

    # set outout csv file column labels
    f.write('url, title, subs, views, description, email, external links\n')

    for query in q:
        while count <= pagesToScrape:
            # assemble the URL to scrape
            scrapeURL = base + str(query) + page + str(count)
            
            print('\nScraping {} \n'.format(scrapeURL))
            externalLinks.append(scrapeURL)
            
            # ping and retrieve search result page HTML 
            r = requests.get(scrapeURL)

            # create Soup object from HTML 
            soup = BeautifulSoup(r.text)

            # parse channel container
            users = soup.find_all('div', 'yt-lockup-byline')
            
            for each in users:
                # parse all URLs that contain 'user'
                a = each.find_all(href=re.compile('user'))
                for i in a:
                    # assemble channel's about page; this is where our data is located
                    url = 'https://www.youtube.com'+i.get('href')+'/about'
                    
                    # check to see if channel has already been scraped
                    if url in visited:
                        print('\t%s has already been scraped\n\n') %(url)
                    else:
                        # ping and retreive channel's HTML, store as Soup object
                        r = requests.get(url)
                        soup = BeautifulSoup(r.text)

                        # output channel url to csv file & terminal
                        f.write(url + ',')
                        k.write(url +',')
                        print('\t%s') %(url)

                        # scrape the meta data
                        get_title()
                        get_subs()
                        get_description()
                        get_links()
                        get_related()

                        # formatting csv & terminal output
                        f.write('\n')	
                        print('\n')

                        # add url to visited list
                        visited.append(url)

                        # time delay between pings to YouTube server
                        time.sleep(timeToSleep)
            
            # iterate to the next search result page
            count += 1
            print('\n')
        
        # reset page count as we've iterated to next search term
        count = 1
        print('\n')	

    print (externalLinks)
    f.close()
    k.close()
    return (externalLinks)


class Piechart(APIView):
    def post(self, request, *args, **kwargs):
        video_id = request.data.get('video_id')
        t = piechartmain(video_id)
        return Response(t)
    
def piechartmain(video_id):
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey="AIzaSyBLiy3AiPuc33fl3z2xhLL0Nubv8tKeKp8")
    ucom = []
    video_response = youtube.videos().list(id=video_id, part='snippet,statistics,recordingDetails,contentDetails').execute()
    comment_count=video_response['items'][0]['statistics']['commentCount']
    def load_comments(match):
        for item in match["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            print("Comment by user {}: {}".format(author, text))
            ucom.append(text)

    def get_comment_threads(youtube, video_id, limit):
        results = youtube.commentThreads().list(
            part="snippet",
            maxResults=limit,
            videoId=video_id,
            textFormat="plainText"
        ).execute()
        return results

    def get_comment_thread(youtube, video_id, mytoken, limit):
        results = youtube.commentThreads().list(
            part="snippet",
            maxResults=limit,
            videoId=video_id,
            textFormat="plainText",
            pageToken=mytoken
        ).execute()
        return results


    limit1 = 100
    limit = int(comment_count)
    vid = video_id

    if limit>100:
        if limit%100==0:
            count=limit/100-1
        else:
            count=limit/100
    else:
        count=0
        limit1=limit
    
    match = get_comment_threads(youtube, video_id, limit1)
    # return (match)
    # if match["nextPageToken"]
    next_page_token = match["nextPageToken"]
    load_comments(match)

    while count>0:
        if count==1:
            match1 = get_comment_thread(youtube, video_id, next_page_token, (limit-(limit/100)*100))
        else:    
            match1 = get_comment_thread(youtube, video_id, next_page_token, 100)
        next_page_token = match1.get("nextPageToken")
        if not next_page_token:
            break
        load_comments(match1)
        count=count-1

    print(len(ucom))

    filtered_comments=[]
    def remove_emoji(string):
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    for comment in ucom:
        com = remove_emoji(comment)
        filtered_comments.append(com)
    print(filtered_comments)

    print(len(filtered_comments))


    nltk.download('vader_lexicon')
    sid=SentimentIntensityAnalyzer()

    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0
    track = []
    for comment in filtered_comments:
        i = sid.polarity_scores(comment)['compound']
        if (i == 0):  
                neutral += 1
        elif (i > 0 and i <= 0.3):
            wpositive += 1
        elif (i > 0.3 and i <= 0.6):
            positive += 1
        elif (i > 0.6 and i <= 1):
            spositive += 1
        elif (i > -0.3 and i <= 0):
            wnegative += 1
        elif (i > -0.6 and i <= -0.3):
            negative += 1
        elif (i > -1 and i <= -0.6):
            snegative += 1
        track.append(i)



    NoOfTerms = len(filtered_comments)


    positive = format(100 * float(positive) / float(NoOfTerms), '0.2f')
    wpositive = format(100 * float(wpositive) / float(NoOfTerms), '0.2f')
    spositive = format(100 * float(spositive) / float(NoOfTerms), '0.2f')
    negative = format(100 * float(negative) / float(NoOfTerms), '0.2f')
    wnegative = format(100 * float(wnegative) / float(NoOfTerms), '0.2f')
    snegative = format(100 * float(snegative) / float(NoOfTerms), '0.2f')
    neutral = format(100 * float(neutral) / float(NoOfTerms), '0.2f')



    Final_score = statistics.mean(track) 

    if Final_score>0:
        print("Using Vader Sentiment Analyzer: ")
        print("Overall Reviews are Positive with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
    elif Final_score<0:
        print("Using Vader Sentiment Analyzer: \n")
        print("Overall Reviews are Negative with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
    else :
        print("Using Vader Sentiment Analyzer: \n")
        print("Overall Reviews are Moderate with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))


    print()
    print("Detailed Report: ")
    print(str(positive) + "% people thought it was positive")
    print(str(wpositive) + "% people thought it was weakly positive")
    print(str(spositive) + "% people thought it was strongly positive")
    print(str(negative) + "% people thought it was negative")
    print(str(wnegative) + "% people thought it was weakly negative")
    print(str(snegative) + "% people thought it was strongly negative")
    print(str(neutral) + "% people thought it was neutral")


    from textblob import TextBlob

    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0
    track = []
    for comment in filtered_comments:
        analysis = TextBlob(comment)
        i = analysis.sentiment.polarity
        if (i == 0):  
                neutral += 1
        elif (i > 0 and i <= 0.3):
            wpositive += 1
        elif (i > 0.3 and i <= 0.6):
            positive += 1
        elif (i > 0.6 and i <= 1):
            spositive += 1
        elif (i > -0.3 and i <= 0):
            wnegative += 1
        elif (i > -0.6 and i <= -0.3):
            negative += 1
        elif (i > -1 and i <= -0.6):
            snegative += 1
        track.append(i)



    NoOfTerms = len(filtered_comments)


    positive = format(100 * float(positive) / float(NoOfTerms), '0.2f')
    wpositive = format(100 * float(wpositive) / float(NoOfTerms), '0.2f')
    spositive = format(100 * float(spositive) / float(NoOfTerms), '0.2f')
    negative = format(100 * float(negative) / float(NoOfTerms), '0.2f')
    wnegative = format(100 * float(wnegative) / float(NoOfTerms), '0.2f')
    snegative = format(100 * float(snegative) / float(NoOfTerms), '0.2f')
    neutral = format(100 * float(neutral) / float(NoOfTerms), '0.2f')



    Final_score = statistics.mean(track) 

    if Final_score>0:
        print("Using TextBlob Sentiment Analyzer: ")
        print("    Overall Reviews are Positive with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
    elif Final_score<0:
        print("Using TextBlob Sentiment Analyzer: \n")
        print("Overall Reviews are Negative with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))
    else :
        print("Using TextBlob Sentiment Analyzer: \n")
        print("Overall Reviews are Moderate with Score "+ str(format(100 * Final_score , '0.2f')+"% \n"))


    print()
    print("Detailed Report: ")
    print(str(positive) + "% people thought it was positive")
    print(str(wpositive) + "% people thought it was weakly positive")
    print(str(spositive) + "% people thought it was strongly positive")
    print(str(negative) + "% people thought it was negative")
    print(str(wnegative) + "% people thought it was weakly negative")
    print(str(snegative) + "% people thought it was strongly negative")
    print(str(neutral) + "% people thought it was neutral")


    #pie chart

    y = np.array([positive, wpositive, spositive, negative,wnegative,snegative,neutral])
    mylabels = ['positive', 'weak positive', 'strong positive', 'negative','weak negative','strong negative','neutral']
    t = y,mylabels
    # response_data = {
    #     'positive': float(positive),
    #     'weak positive':float(wpositive),
    #     'strong positive':float(spositive),
    #     'negative':float(negative),
    #     'weak negative':float(wnegative),
    #     'strong negative':float(snegative),
    #     'neutral':float(neutral)

    # }

    response_data = {
        'positive':int(float(positive)+float(wpositive)+float(spositive)),
        'negative':int(float(negative)+float(wnegative)+float(snegative)),
        # 'neutral':int(neutral)
    }

    return(response_data)



#testing
@api_view(['GET','POST',"DELETE"])
def get_all_meta_data(request):
    if request.method == 'GET':
        data = scraped_data.objects.all()
        serializer = scraped_data_Serializer(data,many = True)
        return Response(serializer.data)


















class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        response_data = super(LoginAPI, self).post(request, format=None)
        response_data.data['user_id'] = user.id
        return response_data

# Logout API
class LogoutAPI(KnoxLogoutView):
    pass
#testing
class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })







# 
    #path('download/', download_video, name='download_video'),
    # path('list/',title_list),#### To remove 


    # path('download/', download_video, name='download_video'),
    # path('display/', Profanity.as_view(), name='display data'),#To remove
    # path('download/', get_all_meta_data, name='display data'),#To remove
    

    
    
    # path('login/', LoginAPI.as_view(), name='login'),
    # path('logout/', LogoutAPI.as_view(), name='logout'),
    # path('register/', RegisterAPI.as_view(), name='register'),
    # path('register/', RegisterAPI.as_view(), name='register'),


    # path('csv/<str:video_id>/', csvconverter.as_view(), name='Put id in get'),###Test if need 
    


















# #dunmmy

# #testing
# @api_view(['GET','POST',"DELETE"])
# def get_all_meta_data(request):
#     if request.method == 'GET':
#         data = scraped_data.objects.all()
#         serializer = scraped_data_Serializer(data,many = True)
#         return Response(serializer.data)




# @api_view(['POST'])
# def download_video(request):
#     url = request.data.get('url')
#     yt = YouTube(url)

#     video = yt.streams.get_lowest_resolution()
#     video_url = video.url

#     response = requests.get(video_url)
#     content_type = response.headers['content-type']
#     content = response.content
#     response = HttpResponse(content, content_type)
#     response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'
#     return response


# # class Similar_video(APIView):
# #     def post(self,request):
# #         video_id = request.data.get('video_id')
# #         t= similar_video_main(video_id)
# #         return Response(t)
# def find_email(text):
#     pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#     emails = re.findall(pattern, text)
#     return emails

# def get_url_from_des(video_id):
#     youtube = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
#     video_response = youtube.videos().list(id=video_id, part='snippet,statistics,recordingDetails,contentDetails').execute()
#     description =video_response['items'][0]['snippet']['description']
#     s = description
    
  

#     lst = re.findall('\S+@\S+', s)     

#     print(lst) 
#     return lst

# class LoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)
#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         response_data = super(LoginAPI, self).post(request, format=None)
#         response_data.data['user_id'] = user.id
#         return response_data

# # Logout API
# class LogoutAPI(KnoxLogoutView):
#     pass
# #testing
# class RegisterAPI(generics.GenericAPIView):
#     serializer_class = UserSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response({
#             "user": UserSerializer(user, context=self.get_serializer_context()).data,
#             "token": AuthToken.objects.create(user)[1]
#         })


# @api_view(['GET','POST'])
# def title_list(request):
#     if request.method == 'GET':
#         titles = scraped_data.objects.all()  #complex data
#         serializer = scraped_data_Serializer(titles,many = True)
#         return Response(serializer.data)
    
# @api_view(['POST'])
# def download_video(request):
#     url = request.data.get('url')
#     yt = YouTube(url)
#     video = yt.streams.get_lowest_resolution()
#     video_url = video.url
#     response = requests.get(video_url)
#     content_type = response.headers['content-type']
#     content = response.content
#     response = HttpResponse(content, content_type)
#     response['Content-Disposition'] = f'attachment; filename="{yt.title}.mp4"'
#     return response


# class csvconverter(APIView):
#     def get(self, request, video_id):
#         youtube = discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
#         video_response = youtube.videos().list(id=video_id, part='snippet,statistics,recordingDetails').execute()
#         channelid = video_response["items"][0]['snippet']['channelId']
#         url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet&id={} &key={}'.format(channelid,DEVELOPER_KEY)
#         response = requests.get(url)

#         if response.status_code == 200:
#             channel_data = response.json()['items'][0]['snippet']

#         try:
#             title = video_response["items"][0]['snippet']['title']
#         except:
#             title = 'Nil'

#         try:
#             uploaddate = video_response["items"][0]['snippet']['publishedAt']
#         except:
#             uploaddate = 'Nil'
        
#         try:
#             channelid = video_response["items"][0]['snippet']['channelId']
#         except:
#             channelid = 'Nil'

#         try:
#             description =video_response['items'][0]['snippet']['description']
#         except:
#             description = 'Nil'
#         try:
#             video_id= video_response["items"][0]['etag']
#         except:
#             video_id = 'Nil'

#         try:
#             video_tags=video_response["items"][0]['snippet']['tags']
#         except:
#             video_tags = 'Nil'

#         try:    
#             view_count=video_response['items'][0]['statistics']['viewCount']
#         except:
#             view_count ='Nil'

#         try:
#             like_count=video_response['items'][0]['statistics']['likeCount']
#         except:
#             like_count='Nil'

#         try:
#             comment_count=video_response['items'][0]['statistics']['commentCount']
#         except:
#             comment_count= 'Nil'

#         try:
#             geoloaction=video_response['items'][0]['recordingDetails']
#         except:
#             geoloaction='Nil'
        
#         try:
#             thumbnail=video_response['items'][0]['snippet']['thumbnails']
#         except:
#             thumbnail='Nil'
            

#         video_tags_connected = ""
#         for i in video_tags:
#             if(i != video_tags[0]):
#                 video_tags_connected += ","
#             video_tags_connected += i
#         # return Response(geoloaction)
#         try:
#             location_description = geoloaction["locationDescription"]

#         except:
#             location_description='none'
        
#         try:
#             latitude = geoloaction['location']['latitude']
#             longitude = geoloaction['location']['longitude']
#         except:
#             latitude = 'Nil'
#             longitude = 'Nil'
        
#         try:
#             thumbnail = thumbnail['maxres']['url']
#         except:
#             thumbnail = 'Nil'


#         if response.status_code == 200:
#             channel_data = response.json()['items'][0]['snippet']
#         else:
#             print('Error:', response.status_code)



#         # try:
#         #     # Call the videos.list method to retrieve the video resource
#         #     video_response = youtube.videos().list(part='contentDetails',id=video_id).execute()

#         #     # Extract the duration from the video resource
#         #     duration = video_response['items'][0]['contentDetails']['duration']

#         # except:
#         #     duration = None

        
#         # duration=str(duration)
#         # list1 = []
#         # list1[:0] = duration
#         # duration2
#         # for i in range(len(list1)):
#         #     if list1[i] == 'H':
#         #         list1[i]='Hours'
#         #     if list1[i] == 'M':
#         #         list1[i]='Minutes'
#         #     if list1[i] == 'S':
#         #         list1[i]="Seconds" 

#         # for i in range(len(list1)):
#         #     if list1[i]=='T':
#         #         duration2="".join(list1[i+1:])



#         #return Response()
#         response_data = {
#             'title': title,
#             'uploaddate': uploaddate,
#             'channelid': channelid,
#             'description': description,
#             'video_id': video_id,
#             'video_tags': video_tags_connected,
#             'view_count': view_count,
#             'like_count': like_count,
#             'comment_count': comment_count,
#             'locationDescription'  : location_description,
#             'latitude' : latitude,
#             'longitude' : longitude,
#             'thumbnail' : thumbnail,
#             'channel_data' : channel_data,
#             'profile':channel_data["thumbnails"]["default"]["url"],
#             #'duration' : duration2,
#         }
#         # serializer = scraped_data_Serializer(data = response_data)

#         # if serializer.is_valid():
#         #     serializer.save()
#         # else:
#         #     return Response(serializer.errors)
        




#         print(channel_data["thumbnails"]["default"]["url"])
#         return Response(response_data)
    




# class Profanity(APIView): ####for Video Not using 
#     def post(self,request):
#         video_id = request.data.get('video_id')
#         a = profanity(video_id)
#         return Response(a)


# def profanity(video_id):
#     url = 'https://www.youtube.com/watch?v='+video_id+'/'
#     # url = 'https://www.youtube.com/watch?v=l5Y8jTdua2M'
    
#     yt = YouTube(url)

#     # Get the audio stream
#     audio_stream = yt.streams.filter(only_audio=True).first()

#     # Download the audio stream
#     output_path = "/content"
#     filename = "audio.mp3"
#     audio_stream.download(output_path=output_path, filename=filename)
#     print(url)
#     print(f"Audio downloaded to {output_path}/{filename}")
#     model = whisper.load_model("large")
#     result = model.transcribe("/content/sample.ogg", fp16=False)
#     with open ('writeme.txt', 'w') as file:  
#         file.write(str(result["text"]))  

#     print(result["text"])


#     import pandas as pd
#     df=pd.read_csv("profanity/profanity_en.csv")


#     with open('writeme.txt', 'r') as file:
#         data1=file.read()
#         words=data1.split()
#         a=[]
#         for i in range(len(words)):
#             if words[i] in list(df['text']):
#                 a.append(words[i])
#         frequency = {}
#         for j in a:
#             if j in frequency:
#                 frequency[j] +=1
#             else:
#                 frequency[j] =1

#         list1 = frequency.values() 
#         list1_sum=sum(list1)

#     print(list1_sum)
        
#     with open('Names.csv', 'w') as f:
#         for key in frequency.keys():
#             f.write("%s, %s\n" % (key, frequency[key]))

#     df=pd.read_csv("profanity/profanity_en.csv")

#     def countOccurrence(a):
#         frequency = {}
#         for j in a:
#             if j in frequency:
#                 frequency[j] +=1
#             else:
#                 frequency[j] =1
        
#         list1 = frequency.values() 
#         list1_sum=sum(list1)
#         print(list1_sum)
#         print(frequency)


#     with open('writeme.txt', 'r') as file:
#         data1=file.read()
#         words=data1.split()
#         a=[]
#         for i in range(len(words)):
#             if words[i] in list(df['text']):
#                 a.append(words[i])

#     countOccurrence(a)


#     return a