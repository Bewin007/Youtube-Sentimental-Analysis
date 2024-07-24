import re
from googleapiclient.discovery import build
# import nltk

def comment(video_id):
    # nltk.download('punkt')

    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    # youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey="AIzaSyBLiy3AiPuc33fl3z2xhLL0Nubv8tKeKp8")
    youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey="AIzaSyBtGrN3LJ-jluuy_V56GZBlmt5tHfVAGB0")
    ucom = []

    video_response = youtube.videos().list(id=video_id, part='snippet,statistics,recordingDetails,contentDetails').execute()
    comment_count = video_response['items'][0]['statistics']['commentCount']

    def load_comments(match):
        for item in match["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            # print("Comment by user {}: {}".format(author, text))
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

    if limit > 100:
        if limit % 100 == 0:
            count = limit / 100 - 1
        else:
            count = limit / 100
    else:
        count = 0
        limit1 = limit
    
    match = get_comment_threads(youtube, video_id, limit1)

    if "nextPageToken" in match:
        next_page_token = match["nextPageToken"]
        load_comments(match)

        while count > 0:
            if count == 1:
                match1 = get_comment_thread(youtube, video_id, next_page_token, (limit-(limit/100)*100))
            else:    
                match1 = get_comment_thread(youtube, video_id, next_page_token, 100)
            next_page_token = match1.get("nextPageToken")
            if not next_page_token:
                break
            load_comments(match1)
            count = count - 1

        # print(len(ucom))
    
    else:
        load_comments(match)
        # print(len(ucom))

    filtered_comments = []

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

    # You can return or process the filtered comments here as per your requirements
comment('w_CcsOanlIQ')