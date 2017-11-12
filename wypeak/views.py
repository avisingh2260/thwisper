#!/Python27/python
#TO DO: encoding in hashtags chart
#Ankit Commit
from django.shortcuts import render
from twitter.oauth_dance import parse_oauth_tokens
from django.http import HttpResponseRedirect
import datetime
import os
import uuid
import urllib
import urlparse
from functools import partial
import cloudant
from cloudant.account import Cloudant
from cloudant.document import Document
import pygal
from django.http import HttpResponse
from urllib2 import time 
from urllib2 import URLError  
from httplib import BadStatusLine
import requests
from pygal.style import Style
import threading
import sys 
import twitter
from bson.json_util import dumps

CONSUMER_KEY = 'g8wzznMufD2Oy6FaNT4QRL5gT'
CONSUMER_SECRET ='HEmyIoFjMkeJXA0hiCVKtCzaVZpMGE11HlH4QgG2sSbsEJ7yJ4'

# shweta


OAUTH_CALLBACK = 'http://twhisper.mybluemix.net/oauth_helper'
#OAUTH_CALLBACK = 'http://ibm-twhisper.mybluemix.net/oauth_helper'
#OAUTH_CALLBACK = 'http://ibmtwhisper.mybluemix.net/oauth_helper'
#OAUTH_CALLBACK = 'http://127.0.0.1:8000/oauth_helper'

wave_url= 'http://twhisper.mybluemix.net/twitterwaves'
#wave_url= 'http://ibm-twhisper.mybluemix.net/twitterwaves'
#wave_url= 'http://ibmtwhisper.mybluemix.net/twitterwaves'
#wave_url= 'http://127.0.0.1:8000/twitterwaves'


#mehjabin cloudant
#USERNAME="37192f62-4f1d-41d9-80a1-8726ced949a8-bluemix"
#PASSWORD= "83dc8699353ad396c065b2e911e919762ce9d2abc7a6fb8422734c743930504d"       
#cloudantURL= "https://37192f62-4f1d-41d9-80a1-8726ced949a8-bluemix:83dc8699353ad396c065b2e911e919762ce9d2abc7a6fb8422734c743930504d@37192f62-4f1d-41d9-80a1-8726ced949a8-bluemix.cloudant.com"

#davide cloudant
#USERNAME="7239f7cd-1924-481b-9e25-e36ba34e6c13-bluemix"
#PASSWORD="6bbe6d4643bdefc129819c906c75c5b9d70a4f5c2ea4813b62069fe48e316212"
#cloudantURL= "https://7239f7cd-1924-481b-9e25-e36ba34e6c13-bluemix:6bbe6d4643bdefc129819c906c75c5b9d70a4f5c2ea4813b62069fe48e316212@7239f7cd-1924-481b-9e25-e36ba34e6c13-bluemix.cloudant.com"
      
apikey='eb727dac890e1125e16905c274442253563b9f67'


class globalSettings:
    def __init__(self, remoteUser="Anonymous", saveHistory = False,*args,**kwags):
        request = kwags.pop('request',None)
        if request:
            self.request = request
        self.return_code = "TWP0"
        self.remoteUser = remoteUser
        self.saveHistory = saveHistory
        self.summary_name = 'summary'
        self.appName ="wypeak"
        self.return_msg = {
                             "TWP0":"Operation succesfully executed", 
                             "TWP01":"Operation succesfully executing......Please wait",
                             "TWP010":"Too many retries. Quitting.", 
                             "TWP020":"Encountered 401 Error (Not Authorized)",
                             "TWP030":"Encountered 404 Error (Not Found)",
                             "TWP040":"Encountered 429 Error (Rate Limit Exceeded). Retrying in 15 minutes...",
                             "TWP050":"Encountered 429 Error (Rate Limit Exceeded). Quitting. Please retry in 15 minutes.",
                             "TWP060":"Encountered Errors. Retried with no success... Quitting. Please retry in 15 minutes.",
                             "TWP100":"Encountered Errors. Quitting.",
                             "TWP110":"URLError encountered. Retried with no success... Quitting.",
                             "TWP120":"Too many consecutive errors... bailing out",
                             "TWP130":"No data found",
                             "TWP140":"Twitter error",
                             "TWPDB010":"Not able to instantiate a database collection",
                             "TWPDB020":"Not able to save a collection on database",
                             "TWPDB030":"Not able to find a collection on database",
                             "TWPDB040":"Not able to open a database",
                             "TWPDB050":"Not able to delete a collection on database",
                             "TWPDB060":"Not able to insert a collection on database",
                 "TWPOAUTH":"your twitter credentials have expired or have been revoked",
                 "TWPQ010":"Query parameter not provided",
                 "TWPD010":"Domain not allowed to access api",
                 "TWPP010":"Python code error occured"
                             }
        self.set_db();
        
    def closeclient(self):
        try:
            self.client1.close()
            self.client2.close()
        except pymongo.errors.PyMongoError as e:
            pass
    def set_summary_name(self, summary_name):
        self.summary_name = summary_name
    def set_return_code(self, return_code):
        self.return_code = return_code
    def set_appName(self, appName):
        self.appName ="wypeak"
    def set_remoteUser(self, remoteUser):
        self.remoteUser = remoteUser
    def set_db(self):
        
        USERNAME1="37192f62-4f1d-41d9-80a1-8726ced949a8-bluemix"
        PASSWORD1= "83dc8699353ad396c065b2e911e919762ce9d2abc7a6fb8422734c743930504d"       
        cloudantURL1= "https://37192f62-4f1d-41d9-80a1-8726ced949a8-bluemix:83dc8699353ad396c065b2e911e919762ce9d2abc7a6fb8422734c743930504d@37192f62-4f1d-41d9-80a1-8726ced949a8-bluemix.cloudant.com"
 
        USERNAME2="2f15465e-7edf-4503-a332-4debffec215a-bluemix"
        PASSWORD2= "aa8438dc9f10fd5e4d4f7ad335516e9a0e416c381139987a7eb5234f17d58de6"       
        cloudantURL2= "https://2f15465e-7edf-4503-a332-4debffec215a-bluemix:aa8438dc9f10fd5e4d4f7ad335516e9a0e416c381139987a7eb5234f17d58de6@2f15465e-7edf-4503-a332-4debffec215a-bluemix.cloudant.com"
          
        try:  
            self.client1 = Cloudant(USERNAME1, PASSWORD1, url=cloudantURL1)
            self.client2 = Cloudant(USERNAME2, PASSWORD2, url=cloudantURL2)
            
        except StandardError as e:
            self.return_code = "TWPDB040" 
##############################################################################################
#Response to be sent to user       
def prepare_results(summary, oldTopTweeters, sortBy, userId, isLogar = False):
   
    sortByKey = {"rt":"rt", "tw":"tw", "im":"followers"}
    
    for item in summary["tweetsDetails"]:
        creation = item["creation"]
        creation=creation.split(" ")
        time=creation[3].split(":")
        creation=time[0]+":"+time[1]+" - "+creation[2]+" "+creation[1]+" "+creation[5] 
        item["creation"]=''.join(creation)
        
    response = {'uid':str(summary['uid']) ,'impression': summary["impression"],'tweeterCount': summary["tweeterCount"],'querytime':summary["querytime"], 'tweets': summary["tweets"], 'retweets': summary["retweets"], 'tweetsDetails': summary["tweetsDetails"], 'topTweeters':sorted(summary["topTweeters"], key=lambda x: x[sortByKey[sortBy]],reverse=True ),'sentiment':summary["sentiment"],'location':summary["location"],"screenName":userId,'numTweets':summary["numTweets"],'numRetweets':summary["numRetweets"]}
        
    newTopTweeters=summary["topTweeters"]
    
    temp=None
    for item in newTopTweeters:
        for oldItem in oldTopTweeters:
            if(oldItem["user"]==item["user"]):
                temp=oldItem
        if(temp!=None):
            if(temp["tw_rank"]>item["tw_rank"]): item["tw_status"]="UP" 
            elif(temp["tw_rank"]<item["tw_rank"]): item["tw_status"]="DOWN" 
            else: item["tw_status"]="EQ"
            if(temp["rt_rank"]>item["rt_rank"]): item["rt_status"]="UP"
            elif(temp["rt_rank"]<item["rt_rank"]): item["rt_status"]="DOWN" 
            else: item["rt_status"]="EQ"
            if(temp["impression_rank"]>item["impression_rank"]): item["impression_status"]="UP"
            elif(temp["impression_rank"]<item["impression_rank"]): item["impression_status"]="DOWN" 
            else: item["impression_status"]="EQ"          
        
        else:
            item["tw_status"]="UP"
            item["rt_status"]="UP"
            item["impression_status"]="UP"
        
        temp=None    
        
    response["topTweeters"]=newTopTweeters        
    
    if len(summary["mostRetweeted"]) > 0:
        response["mostRetweeted"] = sorted(summary["mostRetweeted"], key=lambda x: x["count"],reverse=True )
        #response["mostRetweeted"] = getSorting(summary["mostRetweeted"])
    else:
        response["mostRetweeted"]=[]
    
    if len(summary["tweets"]) > 0:
        response["tw_chart_json"]={"tweets":summary["tweets"],"retweets":summary["retweets"],"charttime":summary["charttime"]}
        response["tophash_chart_json"]=getTagSeries(summary["hashtags"])
        #response["tw_chart"] = getChart_Tweets(summary["tweets"], summary["retweets"], summary["charttime"],  summary["qs"]["q"], isLogar) 
    if len(summary["hashtags"]) > 0:
        response["tophash_chart_json"]=getTagSeries(summary["hashtags"])
        #response["tophash_chart"] = getChart_hashtags(summary["hashtags"]) 
    else:
        print "else"
    return response;
 
############################################################################################################################################
#
def find_popular_tweets( twitter_api, statuses, retweet_threshold = 3): 
    # You could also consider using the favorite_count parameter as part of # this heuristic, possibly using it to provide an additional boost to # popular tweets in a ranked formulation
    return [ status 
                for status in statuses 
                    if status['retweet_count'] > retweet_threshold ]

#***************************************************************************
def getUniqueFollowers(followersPerUser):
    #followersPerUser = [{"user":"john" , "followers" : 100},.....]
    usr = []
    uniquefollowersPerUser =[]
    for item in followersPerUser:
        if item["user"] not in usr:
            usr.append(item["user"]);
            mapfunc = partial(getFollowers, uname=item["user"])
            followers = map(mapfunc,followersPerUser)
            uniquefollowersPerUser.append({"user":item["user"] , "followers" : max(followers)})
    return uniquefollowersPerUser  
 
#****************************************************************************    
def getUniqueHashtags(hashtags):
    #followersPerUser = [{"user":"john" , "followers" : 100},.....]
    uniqueHashtags = []
    htext = []
    for item in hashtags:
        s= 0
        if item[1] not in htext:
            htext.append(item[1])
            s = sum(map(lambda y:y[0],filter(lambda x:x[1] == item[1], hashtags)))
            uniqueHashtags.append([s,item[1]])
    return uniqueHashtags   
#***************************************************************************getUniqueMostRetweets
def getUniqueMostRetweets(mostRetweeted):
    #mostRetweeted [{"rtcount":i, "id":id,"text":...},...]
    rt = []
    uniqueMostRetweeted = []
    cnt  = 0
    for item in mostRetweeted:
        try:
            if item["id"] not in rt:
                rt.append(item["id"])
                #changed 16/09/2014 replaced sum with max
                uniqueMostRetweeted.append({"count":max(map( lambda y:y["count"],filter(lambda x:x["id"] == item["id"], mostRetweeted))) , "user":item["user"],"path":item["path"], "id":item["id"], "text": item["text"], "pimage": item["pimage"]})
                if cnt==69:
                    break;
                else:
                    cnt=cnt+1;
        except KeyError, e:
            pass
    return uniqueMostRetweeted
#***************************************************************************getFollowers
def getFollowers(x,uname):
    if x["user"] == uname:
        return x["followers"]
#***************************************************************************
def setZeroToOne(x):
    if x == 0:
        return 1  
#*************************************************************************** 
def toBool(val):
    """ 
    Get the boolean value of the provided input.

        If the value is a boolean return the value.
        Otherwise check to see if the value is in 
        ["false", "f", "no", "n", "none", "0", "[]", "{}", "" ]
        and returns True if value is not in the list
    """

    if val is True or val is False:
        return val

    falseItems = ["false", "False","f", "no", "n", "none", "0", "[]", "{}", "" ]

    return not str( val ).strip().lower() in falseItems 

#*************************************************************************** Chart tweets    
'''
def getChart_Tweets(tweets, retweets, querytime, title, isLogar): 
    chrt = ''
    #print  >> sys.stderr, sum(tweets)
    if len(tweets) > 0:
        if isLogar:  
            try:
                map(setZeroToOne , tweets) 
                map(setZeroToOne , retweets) 
                #print >> sys.stderr,  'new tweets' , tweets
            except Exception, e:
                pass
                
        series1_full =  getSeries(tweets , querytime)
        series2_full =  getSeries(retweets, querytime)
        #print >> sys.stderr, 'isLogar==', toBool(isLogar)  
        
    custom_style = Style(
          background='transparent',
        plot_background='transparent',
        foreground='#FFFFFF',
        foreground_light='#FFFFFF',
        foreground_dark='#630C0D',
        opacity='.6',
        opacity_hover='.9',
        transition='400ms ease-in',
         colors=('#EBCA97','#E49D67'))
    try:
            tw_chart = pygal.Line(logarithmic=toBool(isLogar),human_readable=False, include_x_axis=True,x_labels_major_count=15,show_minor_x_labels=False, width=800, fill=True,style=custom_style, x_label_rotation=90,  major_label_font_size=22, label_font_size=20, legend_font_size=20, title_font_size=24, print_values=False, show_only_major_dots=True)
            tw_chart.x_labels = querytime
            tw_chart.add('Tweets', series1_full)
            tw_chart.add('Retweets', series2_full)
            tw_chart.title = urllib.unquote(title)
            chrt = tw_chart.render()
    except Exception,e:
            chrt = ""
    return chrt 
'''
#*************************************************************************** Chart hashtags    
'''
def getChart_hashtags(hashtags):
    custom_style = Style(
          background='transparent',
        plot_background='transparent',
        foreground='#FFFFFF',
        foreground_light='#FFFFFF',
        foreground_dark='#630C0D',
        opacity='.6',
        opacity_hover='.9',
        transition='400ms ease-in',
         colors=('#F29C11','#D1A930'))
    series_full =  getTagSeries(hashtags)
    series_full=sorted(series_full, key=lambda x: x['value'])
    #tophash_chart = horizontalbar.HorizontalBar()
    tophash_chart = pygal.HorizontalBar(include_x_axis=True,human_readable=False, show_x_labels=True, show_y_labels=True, label_font_size=20, legend_font_size=20,  major_label_font_size=24, title_font_size=24, value_font_size=22, show_y_guides=False, show_x_guides=False, print_values=True, show_minor_x_labels=False, show_stack_from_top=True, show_legend=False, style=custom_style)
    #map(lambda x:tophash_chart.add(x[1], [{'value':x[0],'label':x[1], 'xlink': 'http://twitter.com/hashtag/' + x[1]}]), hashtags[:10])
    tophash_chart.add('hashtags',series_full)
    
    hashtagLabels=[]
    
    for key in series_full:
        hashtagLabels.append(key['label'])
    
    tophash_chart.x_labels= hashtagLabels
    tophash_chart.title = "Top hashtags"
    
    try:
        chrt = tophash_chart.render()
    except Exception,e:
        chrt = ""
    return chrt
'''
#***************************************************************************
def extractTweeter(x):
    if "user" in x:
        if "screen_name" in x["user"]:
            return {"user": x["user"]["screen_name"],"pimage": x["user"]["profile_image_url"], "text": x["text"], "creation": x["created_at"], "tweet_id": str(x["id"]),"followers": x["user"]["followers_count"], "path": x["user"]["screen_name"]+"/status/"+ str(x["id"])}

#***************************************************************************
def extractLocation(x):
    if "place" in x:
        if x["place"]!=None:
            return {"place":x["place"]["name"],"latlang":x["place"]["bounding_box"]["coordinates"][0][0],"path": x["user"]["screen_name"]+"/status/"+ str(x["id"])}
                
#***************************************************************************
def extractFollowers(x):
    if "user" in x:
        if "followers_count" in x["user"] and "screen_name" in x["user"]:
            return {"user": x["user"]["screen_name"],"followers": x["user"]["followers_count"]}
#***************************************************************************
def extractSentiment(tweets,oldsentiment):
    text=""
    wholetext=""
    params={}
    sentiment = []
    i=0
    apikey='33e4f4f6f4d8ba38cd85ba44fe77082d9b5396ea'
    params['apikey'] = apikey
    params['outputMode'] = 'json'
    
    r=requests.Session()
    response=''
    url="https://gateway-a.watsonplatform.net/calls/info/GetAPIKeyInfo?apikey=33e4f4f6f4d8ba38cd85ba44fe77082d9b5396ea&outputMode=json"
    try:
        response=r.post(url=url)
    except Exception as e:
        print(e)
    transactions= response.json()
    if(transactions["status"]=="OK"):
        if(int(transactions["consumedDailyTransactions"])>1000):
            return []
    
    tweets = sorted(tweets,key=lambda x: x["followers"],reverse=True)
    
    for item in tweets:
        wholetext+=item["text"]
        text+=" "
        text+=item["text"]
        text+=" "
    
         

        if(len(text)<49860):
            print "success"
        else:
            text = text.encode("utf-8")
            post_data= {"sentiment":1,"text":text}
            url="https://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment?"+ urllib.urlencode(params).encode('utf-8')

           
            try:
                response=r.post(url=url,data=post_data)
            except Exception as e:
                print(e)
            sentiresponse= response.json()
          
            if(sentiresponse["status"]=="OK"):
                if(sentiresponse["docSentiment"]["type"]=="neutral"):
                    sentiment.append(0)
                    i+=1
                    
                else:
                    sentiment.append(sentiresponse["docSentiment"]["score"])
                    i+=1   
            else:
                return oldsentiment
            text=" "
        
    if(len(wholetext)<50000):
        wholetext = wholetext.encode("utf-8")
        post_data= {"sentiment":1,"text":wholetext}
        url="https://gateway-a.watsonplatform.net/calls/text/TextGetTextSentiment?"+ urllib.urlencode(params).encode('utf-8')

        try:
            response=r.post(url=url,data=post_data)
        except Exception as e:
            print(e)
        sentiresponse= response.json()
      
        if(sentiresponse["status"]=="OK"):
            if(sentiresponse["docSentiment"]["type"]=="neutral"):
                return {"TIMESTAMP":str(datetime.datetime.now()),"score":0}
               
            else:
                return {"TIMESTAMP":str(datetime.datetime.now()),"score":sentiresponse["docSentiment"]["score"]}
                
        else:
            return oldsentiment
    else:
        sum=0
        for item in sentiment:
            sum+=float(item)
        return {"TIMESTAMP":str(datetime.datetime.now()),"score":sum/len(sentiment)}
       
#***************************************************************************
def getSeries(v,l): 
    s = []
    for key in range(0,len(v)):
        try:
            s.append({'value':v[key], 'label':l[key]})
        except KeyError,e:
            pass
    ##print >> sys.stderr, 'Serie', json.dumps(s)   
    return s
#***************************************************************************
def getTagSeries(v): 
    s = []
    count=0
    for item in v:
        try:
            s.append({'value':item[0],'label':item[1], 'xlink': 'http://twitter.com/hashtag/' + item[1]})
            if count==9:
                break;
            else:
                count=count+1;
        except KeyError,e:
            pass
    return s 

#***************************************************************************   
#***************************************************************************
def delete_colls(settings):
    #map(lambda x:settings.db.drop_collection(settings.db[x]), filter(lambda y:y.startswith('monitor_'), settings.db.collection_names()))
    return


#***************************************************************************
def nowdate(sep="-"):
    now= datetime.date.today()
    return str(now.year) + sep + str(now.month) + sep + str(now.day)
#***************************************************************************
def oauth_login(userId,request):
    
    settings = globalSettings()
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")
    
    OAUTH_TOKEN=''
    OAUTH_TOKEN_SECRET=''
    try:
        if(cloudantDB =='primaryDB'):
            settings.client1.connect()
            db = settings.client1['userdb']
        else:
            settings.client2.connect()
            db = settings.client2['userdb']
        userDoc = db[userId] 
    except StandardError,e:
        pass
    OAUTH_TOKEN = userDoc["oauthToken"]
    OAUTH_TOKEN_SECRET = userDoc["oauthTokenSecret"]
        
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(domain='api.twitter.com', 
                              api_version='1.1',
                              auth=auth
                             )
    return twitter_api

#***************************************************************************
def twitter_trends(request):
    global CONSUMER_KEY
    global CONSUMER_SECRET
    global OAUTH_TOKEN
    global OAUTH_TOKEN_SECRET
    
    settings = globalSettings()
    #response = {"return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}
    #print >> sys.stderr, "qqq1"
    WW_WOE_ID = 1
    US_WOE_ID = 23424977
    IT_WOE_ID = 23424853
    
    woe_def = WW_WOE_ID
    qs = request.GET
    #print >> sys.stderr, "qqq2"
    qs = qs.dict()
    #print >> sys.stderr, "qqq3"
    woe_id = qs.get("woe", woe_def)
    #print >> sys.stderr, "qqq4"
        # Prefix ID with the underscore for query string parameterization.
        # Without the underscore, the twitter package appends the ID value
        # to the URL itself as a special-case keyword argument.
    twitter_api = oauth_login()
    #print >> sys.stderr, "qqq5"
    response = twitter_api.trends.place(_id=woe_id)
    return HttpResponse(dumps(response), content_type="application/json")  

#***************************************************************************            
def twitter_search(settings, twitter_api, rng, max_results, **kw):
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets and 
    # https://dev.twitter.com/docs/using-search for details on advanced 
    # search criteria that may be useful for keyword arguments
    
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets 
    statuses = [] 
    search_results = {} 
    #print >> sys.stderr, 'kw =' + json.dumps(kw)
    try:
        search_results = twitter_api.search.tweets(**kw)
    except Exception, e:
        #print >> sys.stderr, 'Twitter exception'
        settings.set_return_code("TWP140")
        raise
        
    try:
        statuses = search_results['statuses']
    except Exception, e:
        pass
    rng = min(180, rng)
    #print >> sys.stderr, 'pages =' + str(rng)
    #print >> sys.stderr, 'count =' + str(kw["count"])
    #print >> sys.stderr, 'max_results =' + str(max_results)
        
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    
    # Enforce a reasonable limit
   # max_results = min(18000, max_results)
    rng = rng -1
    for j in range(rng):
        #print >> sys.stderr, 'j =' + str(j)
        try:
            if 'search_metadata' in search_results:
                if 'next_results' in search_results['search_metadata']:
                    next_results = search_results['search_metadata']['next_results']
                    next_results = urlparse.parse_qsl(next_results[1:])
                    kwargs = dict(next_results)
                    search_results = twitter_api.search.tweets(**kwargs)
                    statuses += search_results['statuses']
            #next_results = urlparse.parse_qsl(next_results)
           # next_results.update((urlparse.parse_qsl(item)) for item in next_results.items())
        except Exception, e: # No more results when next_results doesn't exist
            #print >> sys.stderr, e
            #print >> sys.stderr, "No next_results found=" + next_results
            break
            
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
     #   kwargs = dict([ kv.split('=') 
      #                  for kv in next_results[1:].split("&") ])
       
        if len(statuses) > max_results: 
            #print >> sys.stderr, 'Too many results'
            break
    #print >> sys.stderr, "FOUND: " + str(len(statuses))   
    return statuses[:max_results]

    
#*************************************************************************************************************
def parse_tokens(result):
    for r in result.split('&'):
        k, v = r.split('=')
        if k == 'oauth_token':
            oauth_token = v
        elif k == 'oauth_token_secret':
            oauth_token_secret = v
        elif k== 'screen_name':
            screenName = v
    return oauth_token, oauth_token_secret, screenName    
#*************************************************************************************************************
def oauth_helper(request):
    
    settings = globalSettings()
    print >> sys.stderr, 'INIZIO oauth_helper'
    
    
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")
    oauth_verifier =qs.get("oauth_verifier")
    OAUTH_TOKEN= request.session['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET= request.session['OAUTH_TOKEN_SECRET']
       
    print >> sys.stderr, 'PRIMA: oauth_token='+OAUTH_TOKEN+'      '+'oauth_token_secret='+OAUTH_TOKEN_SECRET
    
    _twitter = twitter.Twitter(
        auth=twitter.OAuth(
            OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET),
        format='', api_version=None)
    
    callback_url= request.session["callback_url"]
    
    if(oauth_verifier==None):
        return HttpResponseRedirect(callback_url)
    
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET,screenName = parse_tokens(
        _twitter.oauth.access_token(oauth_verifier=oauth_verifier))

    print >> sys.stderr, 'DOPO: oauth_token='+OAUTH_TOKEN+'      '+'oauth_token_secret='+OAUTH_TOKEN_SECRET
    
    if(cloudantDB =='primaryDB'):
        settings.client1.connect()
        db = settings.client1['userdb']
    else:
        settings.client2.connect()
        db = settings.client2['userdb']
        
    #userDoc=""
    try:
        userDoc=db[screenName]
        if userDoc.exists():
            userDoc.delete()
    except StandardError,e:
        pass
       
        
    userData={'_id':screenName,'userId': screenName, 'oauthToken': OAUTH_TOKEN, 'oauthTokenSecret': OAUTH_TOKEN_SECRET}  
           
    db.create_document(userData)
    if(cloudantDB =='primaryDB'):
        settings.client1.disconnect()
    else:
        settings.client2.disconnect()
    
    request.session['userId']= screenName
    #request.session.set_expiry(300)
    callback_url= request.session["callback_url"]
    '''
    query= request.session["query"]
    query=urllib.quote(query)
    source= request.session["source"]
    userid=request.session["uid"]
    if '?' in callback_url:
        callback_url=callback_url +'&screenName='+screenName    
    else:
        callback_url=callback_url +'?screenName='+screenName    
    callback_url=callback_url +'&query='+query    
    callback_url=callback_url +'&source='+source    
    callback_url=callback_url +'&uid='+userid    
    '''
    print >> sys.stderr, 'FINE oauth_helper'
    return HttpResponseRedirect(callback_url)
  
#*****************************************************************************************    
def oauth_loginDance(request):
    
    print >> sys.stderr, 'INIZIO oauth_loginDance'
    
    qs = request.GET
    qs = qs.dict()
    dummy=""
    callback_url = qs.get("callback", wave_url)
    query=qs.get("query", dummy)
    userid=qs.get("uid", dummy)
    source=qs.get("source", dummy)
    request.session["callback_url"]= callback_url
    request.session["query"]= urllib.quote(query)
    request.session["source"]= source
    request.session["uid"]= userid
    #print "Hello "
    #vv = oauth_login(userid)
    #print vv
    
    #request.session.modified = True        
    _twitter = twitter.Twitter(auth=twitter.OAuth('', '', CONSUMER_KEY, CONSUMER_SECRET), format='', api_version=None)
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = parse_oauth_tokens(
            _twitter.oauth.request_token(oauth_callback=OAUTH_CALLBACK))
    
    request.session['OAUTH_TOKEN']= OAUTH_TOKEN
    request.session['OAUTH_TOKEN_SECRET']= OAUTH_TOKEN_SECRET
    
     
    oauth_url = ('https://api.twitter.com/oauth/authorize?oauth_token=' + OAUTH_TOKEN)

    return HttpResponseRedirect(oauth_url)
   
#*****************************

def waves(request):
    
    settings = globalSettings()
    apiname=request.META['HTTP_HOST']+request.path
    requestLog={"API":apiname,"TIMESTAMP":str(datetime.datetime.now()),"objectid":{},"uid":"","error_code":"","error_message":""}
    summary=""
    oldTopTweeters=""
    
    qs = request.GET
    qs = qs.dict()
    AppName = qs.get("App")

  
    if('HTTP_ORIGIN' in request.META):
        val=request.META['HTTP_ORIGIN']
        allowed=sanity_check(settings,val,request)
        #allowed=True
        requestLog["REQUESTER_DOMAIN"]=val
            
        if(allowed==False):
            requestLog["ACCESS_TYPE"]="UNAUTHORIZED"
            
            settings.set_return_code("TWPD010")
            requestLog["error_code"]=settings.return_code
            requestLog["error_message"]=settings.return_msg[settings.return_code]
            save_to_log(settings,requestLog,request)
            
            response={"return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}
            return HttpResponse(dumps(response), content_type="application/json")
    elif(AppName=="Elementi"):
        requestLog["REQUESTER_DOMAIN"]="SpinetiX Elementi"
        save_to_log(settings,requestLog,request)   
    else:

        
        requestLog["REQUESTER_DOMAIN"]="-"
        requestLog["ACCESS_TYPE"]="UNAUTHORIZED"
            
        settings.set_return_code("TWPD010")
        requestLog["error_code"]=settings.return_code
        requestLog["error_message"]=settings.return_msg[settings.return_code]            
        save_to_log(settings,requestLog,request)
        
        response={"return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}
        return HttpResponse(dumps(response), content_type="application/json")
    
    requestLog["ACCESS_TYPE"]="AUTHORIZED"
          
    qs=request.GET
    qs=qs.dict()
    id=qs.get("userid")
    twhisperDashboard = qs.get("tdashboard")  
    #userId = "AshutoshBhadke"
    if (twhisperDashboard=="1"):
        userId = id
    else:
        if 'userId' in request.session:
            userId = request.session['userId']
            #request.session.set_expiry(300)
        else:
            request.session.clear_expired()
            settings.set_return_code("TWPOAUTH")
            requestLog["error_code"]=settings.return_code
            requestLog["error_message"]=settings.return_msg[settings.return_code]
            save_to_log(settings,requestLog,request)
        #My Code--------------------
        
            response={"return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code],"Testing Data ":id}
        
            return HttpResponse(dumps(response), content_type="application/json")
        
    
    #try:
    q_def = '#Obama' 
    count_def = 20
    pages_def = 3
    result_type_def = "recent"
    max_results_def = 20000
    isLogar_def = False
    remoteUser_def = "Anonymous"
    sortBy_def = "im"
    source_def = "api"
    
    response = {"summary": {"q": q_def}, "return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}

    if (settings.return_code == "TWP0"):
        qs = request.GET
        qs = qs.dict()

        pages = int(qs.get("pages", pages_def))
        max_results = int(qs.get("max_results", max_results_def))
        isLogar = qs.get("isLogar", isLogar_def)   
        remoteUser = qs.get("remoteUser", remoteUser_def) 
        sortBy = qs.get("sortBy", sortBy_def)
        source = qs.get("source", source_def)
        settings.set_remoteUser(remoteUser)    
        qs['source']=source
        try:
            del qs['pages'];
        except KeyError,e:
            pass

        try:
            del qs['max_results'];
        except KeyError,e:
            pass
      
        if 'count' not in qs:
            qs["count"] = count_def
        
        if 'result_type' not in qs:
            qs["result_type"] = result_type_def
    
        if 'q' not in qs:
            qs["q"] = q_def

        try:      
            response["summary"]["q"] = qs["q"]
        except KeyError,e:
            response["summary"]["q"] = q_def
    #*******************************************************************************LOOP
    #uid is the unique identifier of a collection. 
    #For each monitor the uid must be exchanged between the client1 and the Server so the server is able
    #to retrieve the nth-collection where saving the nth wave of tweets.
    #The first time a query is invoked the uid is generated and saved into the monitor_xxx collection
    #The uid is returned to the client1 and for each next query the client1 must resend the uid as query string parameter
    #if uid= xxx -> monitor_xxx contains the collection counter  
    #the nth wave is saved into the collection monitor_xxx_n
    #The mongodb query to retrieve the series for the chart will be
    #series=[]
    #for i in range(1:counter):
    #    coll=db["monitor_xxx" + str(counter)]
    #    curs = coll.find()
    #    series.append(curs.count)
    #
    #*******************************************************************************    
        
        uid = userId+qs["q"]+"_"+nowdate()
        uid=uid.replace('#','_')
        uid=uid.replace('%2523','_')
        uid=uid.replace('%23','_')
        uid='monitor_'+uid
        master_coll = str(uid)
        requestLog["uid"]=uid
     
        
        try:
            del qs['uid'];
        except KeyError,e:
            pass    
        try:
            del qs['isLogar'];
        except KeyError,e:
            pass
     #print >> sys.stderr, 'isLogar= ', str(isLogar) 
        try:
            summary,oldTopTweeters = repeat_search(settings, request, master_coll, uid, pages, max_results,userId, **qs)
        except StandardError,e:
            pass

    response = prepare_results(summary,oldTopTweeters,sortBy,userId, isLogar)  
    response["return_code"] = settings.return_code
    response["return_message"] = settings.return_msg[settings.return_code]
 
    objectid=getObjectId(settings)
    requestLog["_id"]=objectid
    save_to_log(settings,requestLog,request)
 
    '''except StandardError,e:
        settings.set_return_code("TWPP010")
        requestLog["error_code"]=settings.return_code
        requestLog["error_message"]=settings.return_msg[settings.return_code]
        #requestLog["error_message"]=e
        save_to_log(settings,requestLog,request)
    '''
    return HttpResponse(dumps(response), content_type="application/json")
    
#***********************************************************************************    
def getObjectId(settings):
    try:
        uid = uuid.uuid1()
        uid=str(uid)
    except StandardError as e:   
        settings.return_code = "TWPDB010"
    return uid

#**********************************************************************************
def save_to_log(settings, requestlog, request):
    
    qs = request.GET 
    qs = qs.dict()
    
    cloudantDB = qs.get("cloudantDB")
    
    if(cloudantDB =='primaryDB'):
        settings.client1.connect()
        db = settings.client1['logdb']
    else:
        settings.client2.connect()
        db = settings.client2['logdb']
   
    try:
        db.create_document(requestlog)
    except StandardError as e:
        settings.return_code = "TWPDB010" 
        
    if(cloudantDB =='primaryDB'):
        settings.client1.disconnect()
    else:
        settings.client2.disconnect()
    
#**********************************************************************************

def sanity_check(settings,val,request):
    settings = globalSettings()
    
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")
    
    if(cloudantDB =='primaryDB'):
        settings.client1.connect()
        db = settings.client1['domaindb']
    else:
        settings.client2.connect()
        db = settings.client2['domaindb']
    
    try:
        userDoc = Document(db,urllib.quote(val, safe=''))
        if userDoc.exists():
            if (cloudantDB =='primaryDB'):
                settings.client1.disconnect()
            else:
                settings.client2.disconnect()
            return True
        else:
            return False
    except StandardError as e:
        settings.return_code = "TWPDB010" 
    return False    
   
#*********************************************************************************
def isAlive(request):
    response={"status":"True"}
    return HttpResponse(dumps(response), content_type="application/json")
    
#********************************************************************************    
def exportData(request):
    import xlwt
    settings = globalSettings()
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")
    dummy=""
    userid = qs.get("uid",dummy)
    #master_coll="monitor_f7cfc140-f7d5-11e4-a8e2-047d7b3d5dc3"    
    if (userid==''):
        settings.set_return_code("TWPQ010")
        
        response={"return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}
        return HttpResponse(dumps(response), content_type="application/json")
     
    if(cloudantDB =='primaryDB'):
            settings.client1.connect()
            db = settings.client1['tweetdb']
    else:
            settings.client2.connect()
            db = settings.client2['tweetdb']
   
    master_coll=str(userid)
    #summary = load_from_mongo(settings, master_coll, True,  {"name":settings.summary_name} )
    #try:
    summary = db[master_coll]
    #except StandardError as e:
        #settings.return_code = "TWPDB010" 
            
    if(cloudantDB =='primaryDB'):
        settings.client1.disconnect()
    else:
        settings.client2.disconnect()
    
    if summary==None:
        settings.set_return_code("TWPDB030")
        
        response={"return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}
        return HttpResponse(dumps(response), content_type="application/json")
        
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=report.xls'
    wb = xlwt.Workbook(encoding='ascii')
    
    
    ws = wb.add_sheet("Summary")
    style_col = "font: bold on; borders: bottom thin,top thin,left thin,right thin;pattern: pattern solid, fore_colour gray25;"
    style_row = "font: bold off; borders: bottom thin,top thin,left thin,right thin;pattern: pattern solid, fore_colour white;"
    styleCol = xlwt.easyxf(style_col)
    styleRow = xlwt.easyxf(style_row)
    for col_num in xrange(0,5):
        ws.col(col_num).width = 4000  # set column width
    
    ws.write(0,0,'Summary',styleCol)
    ws.write(0,1,'',styleCol)
    ws.write(1,0,'#Tweets',styleRow)
    ws.write(2,0,'#Retweets',styleRow)
    ws.write(3,0,'#Tweeters',styleRow)
    ws.write(4,0,'Impressions',styleRow)
    
    
    ws.write(1,1,sum(summary["tweets"]),styleRow)
    ws.write(2,1,sum(summary["retweets"]),styleRow)
    ws.write(3,1,summary["tweeterCount"],styleRow)
    ws.write(4,1,summary["impression"],styleRow)
    

    ws = wb.add_sheet("TopTweeters")
    
    row_num = 0
    
    columns = [
    (u"User", 6000),
    (u"Tweets", 2500),
    (u"Retweets", 2500),
        (u"Impressions", 3500)
    
    ]

    
    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], styleCol)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    tweetdata= summary["topTweeters"]
    for obj in tweetdata:
        row_num += 1
        row = [
            obj["user"],
        obj["tw"],
            obj["rt"],
            obj["followers"]
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], styleRow)
    
    ws = wb.add_sheet("Hashtags")

    row_num = 0
    
    columns = [
        (u"Hashtag", 4500),
        (u"Count", 2000),
    ]

    
    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], styleCol)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    tagdata= summary["hashtags"]
    for obj in tagdata:
        row_num += 1
        row = [
            obj[1],
            obj[0]
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], styleRow)
    

    ws = wb.add_sheet("MostRetweeted")
    row_num = 0
    
    columns = [
        (u"User", 6000),
    (u"Text", 32000),
    (u"Count", 2000)
    ]

   
    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], styleCol)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    retweetdata= summary["mostRetweeted"]
    retweetdata = sorted(retweetdata, key=lambda x: x["count"],reverse=True )
    for obj in retweetdata:
        row_num += 1
        row = [
            obj["user"],
            obj["text"],
            obj["count"]
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], styleRow)
    
    
    ws = wb.add_sheet("Trend")

    row_num = 0
    
    columns = [
        (u"Tweets", 2000),
        (u"Retweets", 2500),
    (u"Time", 6000)
    ]

  
    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], styleCol)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    tweets= summary["tweets"]
    retweets= summary["retweets"]
    time= summary["querytime"]

    for i in xrange(len(tweets)):
        row_num += 1
        row = [
            tweets[i],
        retweets[i],
        time[i]
    ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], styleRow)
    

    wb.save(response)
    return response
#**********************************************************************************************WAVE SERVICE
def wave_service(request):
    #print >> sys.stderr, 'ACCESS ' 
    #Defaults
    settings = globalSettings()
    q_def = '#Obama' 
    count_def = 100
    pages_def = 12
    ################################################################################ Updated 29 Sept 2014
    #source specifies if results must be directly read from mongodb or retrieved by live twitter
    #source = api means invoke the twitter api
    #source = store means get from local db
    sortBy_def = "im"
    remoteUser_def = "Anonymous"
    source_def = "api"
    isLogar_def = False
    max_results_def = 20000
    result_type_def = "recent"
    
    response = {}
    #print >> sys.stderr, 'return_code =' + settings.return_code 
    if (settings.return_code == "TWP0" ):
        qs = request.GET
        qs = qs.dict()
        cloudantDB = qs.get("cloudantDB")
        pages = int(qs.get("pages", pages_def))
        #print >> sys.stderr, 'pages =' + str(pages)
        max_results = int(qs.get("max_results", max_results_def))
        source = qs.get("source", source_def)
        sortBy = qs.get("sortBy", sortBy_def)
        isLogar = qs.get("isLogar", isLogar_def)
        remoteUser = qs.get("remoteUser", remoteUser_def)
        
        if sortBy == '':
            sortBy = sortBy_def
        try:
            del qs['pages'];
        except KeyError,e:
            pass
        try:
            del qs['source'];
        except KeyError,e:
            pass
        try:
            del qs['sortBy'];
        except KeyError,e:
            pass
        try:
            del qs['max_results'];
        except KeyError,e:
            pass
        try:
            del qs['type'];
        except KeyError,e:
            pass
            
        if 'count' not in qs:
            qs["count"] = count_def
            
        if 'result_type' not in qs:
            qs["result_type"] = result_type_def
    #*******************************************************************************LOOP
    #uid is the unique identifier of a collection. 
    #For each monitor the uid must be exchanged between the client1 and the Server so the server is able
    #to retrieve the nth-collection where saving the nth wave of tweets.
    #The first time a query is invoked the uid is generated and saved into the monitor_xxx collection
    #The uid is returned to the client1 and for each next query the client1 must resend the uid as query string parameter
    #*******************************************************************************
        if 'q' not in qs:
            qs["q"] = q_def    
        if 'uid' not in qs:
            uid = uuid.uuid1()
            master_coll = "monitor_" + str(uid)
            #print >> sys.stderr, 'q = ' + str(qs["q"])
        else:
            uid = qs['uid']
            master_coll = "monitor_" + str(uid)
        try:
            del qs['uid'];
        except KeyError,e:
            pass
        try:
            del qs['isLogar'];
        except KeyError,e:
            pass
        try:
            del qs['remoteUser'];
        except KeyError,e:
            pass
        #print >> sys.stderr, 'source = ' + source
        #print >> sys.stderr, 'count = ' + str(qs["count"])
        settings.set_remoteUser(remoteUser)
        if source == "store" and str(uid) != '':
        #read summary from mongodb
            #print >> sys.stderr, 'GET FROM STORE'   
            #print >> sys.stderr, master_coll         
            #summary = load_from_mongo(settings, master_coll, True,  {"name":settings.summary_name} )
            #print >> sys.stderr, "found n results:" + str(summary.count())
            if summary==None:
                response = prepare_results(summary[0], sortBy, isLogar) 
            else:
                settings.set_return_code("TWP130") 
        else:
        #live search API
            #print >> sys.stderr, 'LAUNCH THREAD' 
            response = {'uid':str(uid)}
            thargs = [settings, master_coll, uid, pages, max_results]
            t = threading.Thread(target = repeat_search, name='Thread-01', args= thargs, kwargs=qs)
            t.setDaemon(True)
            current_milli_time = lambda: int(round(time.time() * 1000))
            now = current_milli_time()
            #settings.set_return_code("TWP0")
            s = t.start()
            interval = current_milli_time() - now
            if settings.return_code == "TWP0":
                while interval < 40000 and t.is_alive():
                    if settings.return_code != "TWP0":
                        break;
                        #print >> sys.stderr, str(interval) + ' - ' + settings.return_code
                    interval = current_milli_time() - now
                #print str(interval) + str(t.is_alive())
                if t.is_alive() and settings.return_code == "TWP0":
                    settings.set_return_code("TWP01")
                #summary = load_from_mongo(settings, master_coll, True,  {"name":settings.summary_name} )
                #print >> sys.stderr, 'summary', str(summary[0]['tweets'][0])
                if summary!=None :
                        response = prepare_results(summary[0],sortBy, isLogar)  
        if(cloudantDB =='primaryDB'):
            settings.closeclient1()
        else:
            settings.closeclient2()
    response["return_code"] = settings.return_code
    response["return_message"] = settings.return_msg[settings.return_code]

    return HttpResponse(dumps(response), content_type="application/json")

#********************************************************************Clear database
def clear(request):
    
    settings = globalSettings()
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")
    
    response = {"return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}
    if (settings.return_code == "TWP0"):
        message = "Operation completed succesfully. The data have been successfully cleared"
        rc = 200
        try:
            delete_colls(settings)
        except pymongo.errors.OperationFailure: 
            message ="Error: operation failure deleting data"
            rc = -1
        response = {"return_code":settings.return_code, "message": settings.return_msg[settings.return_code]}
    if(cloudantDB =='primaryDB'):
        settings.closeclient1()
    else:
        settings.closeclient2()
    return HttpResponse(dumps(response),content_type="application/json")
#********************************************************************Repair database
def repair(request):
    
    settings = globalSettings()
    settings.return_code = "TWPDB001" 
        
    try:
        settings.db.command(settings.db.repairDatabase())
    except StandardError as e:
        settings.return_code = "TWPDB020" 
        
    response = {"return_code":settings.return_code, "message": "Database Repaired successfully"}
    
    return HttpResponse(dumps(response),content_type="application/json")

#*************************************************************************************
def get_rate_status(request):
    global CONSUMER_KEY
    global CONSUMER_SECRET
    global OAUTH_TOKEN
    global OAUTH_TOKEN_SECRET
    
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")
    
    settings = globalSettings()
    response = {"return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}
    if (settings.return_code == "TWP0"):
        twitter_api = oauth_login()
        d= twitter_api.application.rate_limit_status()
        response = {"rate_limits_status":d}
    if(cloudantDB =='primaryDB'):
        settings.closeclient1()
    else:
        settings.closeclient2()
    return HttpResponse(dumps(response), content_type="application/json")  
#********************************************************************Clear database
def search(request):
    global CONSUMER_KEY
    global CONSUMER_SECRET
    global OAUTH_TOKEN
    global OAUTH_TOKEN_SECRET
    
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")
    
    settings = globalSettings()
    response = {"return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}
    if (settings.return_code == "TWP0"):
        twitter_api = oauth_login()
        
        qs = request.GET
        qs = qs.dict()
        
        pages = int(qs.get("pages", 4))
        count = int(qs.get("count", 30))
        
        q = qs.get("q", "#Obama")
        kw = {"count": count,"q":q}
        results = twitter_search(settings, twitter_api, pages, 18000, **kw)
        totals = len(results);
        #response = {"totals": totals }
        response["totals"] = totals
        response["results"]= results
        
    if(cloudantDB =='primaryDB'):
        settings.closeclient1()
    else:
        settings.closeclient2()    
    return HttpResponse(dumps(response), content_type="application/json")  
#**********************************************************************************************WAVE SERVICE
def wave_topTweeters(request):
    
    settings = globalSettings()
    
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")
    
    response = {"topTweeters":[],  "return_code":settings.return_code, "return_message":settings.return_msg[settings.return_code]}
    if (settings.return_code == "TWP0"):
        uid_def = ''
        #sortBy can assume tw|rt|im
        sortBy_def = "im"
        summary_name = "summary"
        sortByKey = {"rt":"rt", "tw":"tw", "im":"followers"}
        
        qs = request.GET
        qs = qs.dict()
        uid = qs.get("uid", uid_def)
        sortBy = qs.get("sortBy", sortBy_def)
        
    
        if uid != '':
            master_coll = "monitor_" + uid
            #summary = load_from_mongo(settings, master_coll, True,  {"name":summary_name} )
            response["return_code"] = settings.return_code
            if summary!= None:
                summary = summary[0]
                if len(summary["topTweeters"]) > 0:
                    response["topTweeters"] = sorted(summary["topTweeters"], key=lambda x: x[sortByKey[sortBy]],reverse=True )[:10]
        
    
        if(cloudantDB =='primaryDB'):
            settings.closeclient1()
        else:
            settings.closeclient2()
    return HttpResponse(dumps(response), content_type="application/json")  


#***********************************************************************************
def repeat_search(settings, request, master_coll, uid, pages, max_results, userId, **qs):
    # Default settings of 15 intervals and 1 API call per interval ensure that 
    # you will not exceed the Twitter rate limit.
    summary_name = settings.summary_name;
    saveHistory = settings.saveHistory;
    first_id = 0
    source = qs["source"]
    
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")
        
    summary=None
    summaryStatus=''
    usr =[]
    try:
        ocount = qs["count"] 
    except KeyError, e:
        ocount = 100
    twitter_api = oauth_login(userId,request)
    #print >> sys.stderr, 'Starting repeat_search' 
    #Load summary from db
    def handle_twitter_http_error(settings, e, wait_period = 2, sleep_when_rate_limited = False): 
        
        
        if wait_period > 3600: # Seconds 
            #print >> sys.stderr, 'Too many retries. Quitting.' 
            settings.return_code = "TWP010"
            return None
            #raise e 
        # See https:// dev.twitter.com/ docs/ error-codes-responses for common codes 
        if e.e.code == 401: 
            #print >> sys.stderr, 'Encountered 401 Error (Not Authorized)' 
            settings.return_code =  "TWP020"
            return None 
        elif e.e.code == 404: 
            #print >> sys.stderr, 'Encountered 404 Error (Not Found)' 
            settings.return_code =  "TWP030"
            return None 
        elif e.e.code == 429: 
            #print >> sys.stderr, 'Encountered 429 Error (Rate Limit Exceeded)' 
            if sleep_when_rate_limited: 
                #print >> sys.stderr, "Retrying in 15 minutes... ZzZ..." 
                sys.stderr.flush() 
                time.sleep( 60* 15 + 5) 
                #print >> sys.stderr, '... ZzZ... Awake now and trying again.' 
                settings.return_code =  "TWP040"
                return 2
            else:
                settings.return_code =  "TWP050"
                return None
            # Caller must handle the rate limiting issue 
        elif e.e.code in (500, 502, 503, 504): 
            #print >> sys.stderr, 'Encountered %i Error. Retrying in %i seconds' % (e.e.code, wait_period) 
            time.sleep( wait_period) 
            wait_period *= 1.5 
            settings.return_code =  "TWP060" 
            return wait_period 
        else:
            settings.return_code =  "TWP100"
            return None
            #raise e
       
        # End of nested helper function 
    #summary = load_from_mongo(settings, master_coll, True,  {"name":summary_name} )
    try:
        if(cloudantDB =='primaryDB'):
            settings.client1.connect()
            db = settings.client1['tweetdb']
        else:
            settings.client2.connect()
            db = settings.client2['tweetdb']

        summary = db[master_coll] 
        
        if(cloudantDB =='primaryDB'):
            settings.client1.disconnect()
        else:
            settings.client2.disconnect()
    
    except StandardError,e:
        pass
    if source=='api' or '' or summary==None:    
        summary = dict({"name" : summary_name,"uid":str(uid),"charttime":[],"remoteUser":settings.remoteUser ,"tweets":[], "retweets":[],"numTweets":0,"numRetweets":0, "tweetsDetails":[],"hashtags":[], "retweeters":[] , "mostRetweeted":[] , "uniqueFollowersPerUser":[],"uniqueRetweetersFollowers":[],"retweetsPerUser":[], "impression":0,"tweeterCount":0,"topTweeters":[], "location":[], "max_ids":[],"querytime":[],"qs":qs, "q":qs['q'], "return_codes":[], "wave":0,"sentiment":[]})
        oldTopTweeters=""
        if saveHistory == False:
            qs["count"] = 1
            pages = 1
        #print >> sys.stderr, 'Get summary...qs=' +  json.dumps(summary["qs"] )+ "  uid= "+ str(summary["uid"])
    else:
        oldTopTweeters=summary["topTweeters"]
        summaryStatus = 'old'
        #print >> sys.stderr, 'FOUND summary' +  json.dumps(summary["qs"]) + "  uid= "+ str(summary["uid"])
        first_id = summary["max_ids"][-1]
    
    #print >> sys.stderr, "max_id",first_id
    #Get Query string
    qs = dict(summary["qs"])
    if first_id != 0:
        qs["since_id"] = first_id 
    qs["count"] = ocount
    #get values from previous waves
    cloudantDB = qs.get("cloudantDB")
    tweetsDetails = summary["tweetsDetails"]
    location = summary["location"]
    followersPerUser = summary["uniqueFollowersPerUser"]
    uniqueFollowersPerUser = summary["uniqueFollowersPerUser"]
    retweetersFollowers = summary["uniqueRetweetersFollowers"]
    retweetsPerUser = summary["retweetsPerUser"]
    prevsentiment = summary["sentiment"]
    retweetersWave = []
    retweetersGlobal =  summary["retweeters"]
    #now = datetime.datetime.today().strftime("%c")
    now = datetime.datetime.now()
    charttime = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    summary["statuses"] = []
    #Perform a new search
    ##################################################################################################################################################
    #statuses = twitter_search(twitter_api, pages, max_results, **qs)
    chk = True;
    wait_period = 2 
    error_count = 0
    max_errors = 2
    statuses = []
    #print >> sys.stderr, 'Before while'  
    while chk:
        try: 
            #print >> sys.stderr, 'max_results= ' + str(max_results)  
            #print >> sys.stderr, 'qs= ' + json.dumps(qs)
            
            statuses = twitter_search(settings,twitter_api, pages, max_results, **qs)
            #print >> sys.stderr, "FOUND 1: " + str(len(statuses)) 
            #print >> sys.stderr, 'After search while'  
            chk = False
        except twitter.api.TwitterHTTPError, e: 
            error_count = 0 
            wait_period = handle_twitter_http_error(settings,e, wait_period) 
            if wait_period is None: 
                chk = False 
        except URLError, e: 
            error_count += 1 
            #print >> sys.stderr, "URLError encountered. Continuing." 
            if error_count > max_errors: 
                settings.set_return_code("TWP110")
                #print >> sys.stderr, "Too many consecutive errors... bailing out." 
                #raise 
        except BadStatusLine, e: 
            error_count += 1
            #print >> sys.stderr, "BadStatusLine encountered. Continuing."
            if error_count > max_errors: 
                settings.set_return_code("TWP120")
                #print >> sys.stderr, "Too many consecutive errors... bailing out." 
        except Exception, e:
            #print >> sys.stderr, 'Twitter exception'
            settings.set_return_code("TWP140")
            #raise  
          
            #print >> sys.stderr, "BadStatusLine encountered. Continuing."
                #print >> sys.stderr, "Too many consecutive errors... bailing out." 
            #raise
    ##################################################################################################################################################
    
    #print >> sys.stderr, "FOUND 2: " + str(len(statuses)) 
    #print >> sys.stderr, "saveHistory: " ,saveHistory
    
    try:
        first_id = str(statuses[0]["id"])
    except Exception,e:
        pass
    
    if summary["wave"] == 0 and saveHistory == False:
        statuses = []
    #retweetsPerUser=""
    if len(statuses) != 0:
        summary["statuses"] = dumps(statuses, indent=1)
        #Get Tweets and Retweets
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' retweetsPerUser [{'user':name, "rt":n}]    
        retweetersWave =  map(lambda y:y['user']['screen_name'],filter(lambda x:'retweeted_status' in x,statuses))     
        retweetersGlobal =  retweetersWave + summary["retweeters"]
        retweetsPerUser = [{"rt":retweetersGlobal.count(tweeterName), "user":tweeterName} for tweeterName in set(retweetersGlobal)]
        summary["retweetsPerUser"] = retweetsPerUser
        
        #mostRetweeted [{"rtcount":i, "id":id,"text":...},...]
        mostRetweeted = map(lambda y:{"user":y['retweeted_status']['user']['screen_name'],"pimage":y['retweeted_status']['user']['profile_image_url'],"count": y['retweeted_status']['retweet_count'],"id":y['retweeted_status']['id'],"path":y['user']['screen_name']+"/status/"+ y['retweeted_status']['id_str'],"text":y['retweeted_status']['text']}, filter(lambda x:'retweeted_status' in x,statuses))
        #mostRetweeted = map(lambda y:{"count": y['retweet_count'],"id":y['id'],"path":y['user']['screen_name']+"/status/"+ y['id_str'],"text":y['text']}, filter(lambda x:'retweeted_status' in x,statuses))
        mostRetweeted +=  summary["mostRetweeted"] 
        
        summary["mostRetweeted"] = getUniqueMostRetweets(mostRetweeted)
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' Impression        
        #Calculate the followers: {"user": x["user"]["screen_name"],"followers": x["user"]["followers_count"]}
        followersPerUser += map(extractFollowers, statuses)
        #Calculate the Unique followers per user getting the max number of followers: {"user": x["user"]["screen_name"],"followers": x["user"]["followers_count"]}
        uniqueFollowersPerUser = getUniqueFollowers(followersPerUser)
        sumv = 0
        for item in followersPerUser:
            sumv += item["followers"] 
      
        summary['impression'] = sumv
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' Impression end

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' Hashtags             
        #Get the Hashtags for the current wave
        hashtags = [ hashtag['text'] for status in statuses for hashtag in status['entities']['hashtags'] ]
        hashtags = map(lambda x:x.lower(),hashtags)
        #Add to the previous hashtags
        #Get the top hashtags
        if (len(hashtags) > 0):
            hashtagsTuple =  [[hashtags.count(item), item] for item in set(hashtags)]
            hashtagsTuple.extend(summary["hashtags"])
            uniqueHashtags = getUniqueHashtags(hashtagsTuple)
                        
            summary["hashtags"] = sorted(uniqueHashtags, key=lambda x: x[0], reverse=True)
#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' Hashtags end

#'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' Top Tweeters     
        #Get Tweeters= ["name1",..."namen"]
    loc=[]; 
    tweeters_len= len(tweetsDetails)   
    tweetsDetails += map(extractTweeter, statuses)
    loc += map(extractLocation, statuses)
    sentiment=summary["sentiment"]
    if (tweeters_len<len(tweetsDetails) and len(tweetsDetails)!=0):
        sentiment = extractSentiment(tweetsDetails,sentiment) 
    for item in loc:
        if(item!=None):
            location.append(item)
        #get Top Tweeters = [(20,'JohnDoe'), (14, 'maryJane'),.....]
        #if (len(tweetsDetails) > 0):
            #topTweeters = sorted(({"tw":tweeters.count(tweeterName), "user":tweeterName, "followers":0} for tweeterName in set(tweetsDetails)), key=lambda x: x["tw"],reverse=True)
            
    uniqueTweeters=[]
    topTweeters=[]
    count = 0
    if (len(tweetsDetails) > 0):
        for item in tweetsDetails:
                uniqueTweeters.append(item["user"])
                                   
    if (len(tweetsDetails) > 0):
        for item in tweetsDetails:
            try:
                if item["user"] not in usr :
                    usr.append(item["user"])
                    topTweeters.append({"tw":uniqueTweeters.count(item["user"]), "user":item["user"], "followers":0, "pimage":item["pimage"]})
                    if count==69:
                        break;
                    else:
                        count=count+1;
            except KeyError,e :
                pass    
        
        #get Top Tweeters = [(20,'JohnDoe'), (14, 'maryJane'),.....]
        if (len(tweetsDetails) > 0):
            topTweeters = sorted(topTweeters, key=lambda x: x["tw"],reverse=True)    
            tweetsDetails = sorted(tweetsDetails, key=lambda x: x["creation"],reverse=True)    
    
    summary["impression"]=0 
    rank=1   
    for item in topTweeters:
        item["followers"] = map(lambda y:y["followers"],filter(lambda x:x["user"] == item["user"],uniqueFollowersPerUser))[0]
        userRetweets = filter(lambda x:x['user'] == item['user'], retweetsPerUser)
        if len(userRetweets) > 0:
            rtdata = userRetweets[0]
            item["rt"] = rtdata["rt"]
        else:
            item["rt"] = 0
        item["tw"] = item["tw"]-item["rt"] 
        item["followers"] = (item["rt"]+item["tw"])*item["followers"]
        summary["impression"]= summary["impression"]+item["followers"]
        item["tw_rank"]=rank
        rank=rank+1 
    
    rank=1
    if (len(tweetsDetails) > 0):
            topTweeters = sorted(topTweeters, key=lambda x: x["tw"],reverse=True)    
    for item in topTweeters:
        item["tw_rank"]=rank
        rank=rank+1
    
    rank=1
    if (len(tweetsDetails) > 0):
            topTweeters = sorted(topTweeters, key=lambda x: x["rt"],reverse=True)    
    for item in topTweeters:
        item["rt_rank"]=rank
        rank=rank+1
    
    
    rank=1
    if (len(tweetsDetails) > 0):
            topTweeters = sorted(topTweeters, key=lambda x: x["followers"],reverse=True)    
    for item in topTweeters:
        item["impression_rank"]=rank
        rank=rank+1
        
    summary["topTweeters"] = topTweeters
    summary["tweeterCount"] = len(topTweeters)
    summary["tweets"].append((len(statuses)-(len(retweetersWave))))
    summary["numTweets"] = sum(summary["tweets"])
    summary["retweets"].append(len(retweetersWave))
    summary["numRetweets"] = sum(summary["retweets"])
    summary["retweetsPerUser"] = retweetsPerUser
    summary["sentiment"]=sentiment    
    
    summary["uniqueFollowersPerUser"] = uniqueFollowersPerUser 
    summary["wave"] = summary["wave"] + 1
    summary["max_ids"].append(first_id)
    summary["querytime"].append(now.strftime("%c"))
    summary["charttime"].append(charttime)
    summary["tweetsDetails"] = tweetsDetails
    summary["location"] = location 
  
    summary["retweeters"]= retweetersGlobal
    summary["return_codes"].append(settings.return_code)
    if(cloudantDB =='primaryDB'):
        settings.client1.connect()
        db = settings.client1['tweetdb']
    else:
        settings.client2.connect()
        db = settings.client2['tweetdb']
   
    
    #try:
    summary['_id'] = master_coll
    
    if source=='api' or '' or summaryStatus=='':  
        try:
            userDoc=db[master_coll]
            userDoc.delete()
        except StandardError as e:
            #settings.return_code = "TWPDB050" 
            error=" deleted"
            pass
        db.create_document(summary)
    else:
        summary.save()
    
    #except StandardError as e:
    #    settings.return_code = "TWPDB020" 
       
    if(cloudantDB =='primaryDB'):
        settings.client1.disconnect()
    else:
        settings.client2.disconnect()
    #print >> sys.stderr, 'SEARCH END'
    return summary,oldTopTweeters

#*****************************************************************************************************


def getPersonInsights(request):
    
    userId='AshutoshBhadke'
    rng=180
    max_results=20000
    statuses=[]
    text="""aCall me Ishmael. Some years ago-never mind how long precisely-having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen and regulating the circulation.
    Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a 
    strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people's hats off-then, I account it high time to get to sea as soon as I can. This is my substitute for pistol and ball. With a philosophical flourish Cato throws himself upon his sword; I quietly take to 
    the ship. There is nothing surprising in this. If they but knew it, almost all men in their degree, some time or other, cherish very nearly the same feelings towards the ocean with me. There now is your insular city of the Manhattoes, belted round by wharves as Indian isles by coral reefs-commerce surrounds it with 
    her surf. Right and left, the streets take you waterward. Its extreme downtown is the battery, where that noble mole is washed by waves, and cooled by breezes, which a few hours previous were out of sight of land. Look at the crowds of water-gazers there. Circumambulate the city of a dreamy Sabbath afternoon. Go from Corlears Hook to Coenties Slip, and from thence, by Whitehall, northward. What do you see?-Posted like silent sentinels all around the town, stand thousands upon thousands of mortal men fixed in ocean reveries. Some leaning against the spiles; some seated upon the pier-heads; some looking over the bulwarks of ships from China; some high aloft in the rigging, as if striving to get a still better seaward peep. But these are all landsmen; of week days pent up in lath and plaster-tied to counters, nailed to benches, clinched to desks. How then is this? Are the green fields gone? What do they here? But look! here come more crowds, pacing straight for the water, and seemingly bound for a dive. Strange! Nothing will content them but the extremest limit of the land; loitering under the shady lee of yonder warehouses will not suffice. No. They must get just as nigh the water as they possibly can without falling in. And there they stand-miles of them-leagues. Inlanders all, they come from lanes and alleys, streets and avenues-north, east, south, and west. Yet here they all unite. Tell me, does the magnetic virtue of the needles of the compasses of all those ships attract them thither? Once more. Say you are in the country; in some high land of lakes. Take almost any path you please, and ten to one it carries you down in a dale, and leaves you there by a pool in the stream. There is magic in it. Let the most absent-minded of men be plunged in his deepest reveries-stand that man on his legs, set his feet a-going, and he will infallibly lead you to water, if water there be in all that region. Should you ever be athirst in the great American desert, try this experiment, if your caravan happen to be supplied with a metaphysical professor. Yes, as every one knows, meditation and water are wedded for ever. But here is an artist. He desires to paint you the dreamiest, shadiest, quietest, most enchanting bit of romantic landscape in all the valley of the Saco. What is the chief element he employs? There stand his trees, each with a hollow trunk, as if a hermit and a crucifix were within; and here sleeps his meadow, and there sleep his cattle; and up from yonder cottage goes a sleepy smoke. Deep into distant woodlands winds a mazy way, reaching to overlapping spurs of mountains bathed in their hill-side blue. But though the picture lies thus tranced, and though this pine-tree shakes down its sighs like leaves upon this shepherd's head, yet all were vain, unless the shepherd's eye were fixed upon the magic stream before him. Go visit the Prairies in June, when for scores on scores of miles you wade knee-deep among Tiger-lilies-what is the one charm wanting?-Water-there is not a drop of water there! Were Niagara but a cataract of sand, would you travel your thousand miles to see it? Why did the poor poet of Tennessee, upon suddenly receiving two handfuls of silver, deliberate whether to buy him a coat, which he sadly needed, or invest his money in a pedestrian trip to Rockaway Beach? Why is almost every robust healthy boy with a robust healthy soul in him, at some time or other crazy to go to sea? Why upon your first voyage as a passenger, did you yourself feel such a mystical vibration, when first told that you and your ship were now out of sight of land? Why did the old Persians hold the sea holy? Why did the Greeks give it a separate deity, and own brother of Jove? Surely all this is not without meaning. And still deeper the meaning of that story of Narcissus, who because he could not grasp the tormenting, mild image he saw in the fountain, plunged into it and was drowned. But that same image, we ourselves see in all rivers and oceans. It is the image of the ungraspable phantom of life; and this is the key to it all. Now, when I say that I am in the habit of going to sea whenever I begin to grow hazy about the eyes, and begin to be over conscious of my lungs, I do not mean to have it inferred that I ever go to sea as a passenger. For to go as a passenger you must needs have a purse, and a purse is but a rag unless you have something in it. Besides, passengers get sea-sick-grow quarrelsome-don't sleep of nights-do not enjoy themselves much, as a general thing;-no, I never go as a passenger; nor, though I am something of a salt, do I ever go to sea as a Commodore, or a Captain, or a Cook. I abandon the glory and distinction of such offices to those who like them. For my part, I abominate all honourable respectable toils, trials, and tribulations of every kind whatsoever. It is quite as much as I can do to take care of myself, without taking care of ships, barques, brigs, schooners, and what not. And as for going as cook,-though I confess there is considerable glory in that, a cook being a sort of officer on ship-board-yet, somehow, I never fancied broiling fowls;-though once broiled, judiciously buttered, and judgmatically salted and peppered, there is no one who will speak more respectfully, not to say reverentially, of a broiled fowl than I will. It is out of the idolatrous dotings of the old Egyptians upon broiled ibis and roasted river horse, that you see the mummies of those creatures in their huge bake-houses the pyramids. No, when I go to sea, I go as a simple sailor, right before the mast, plumb down into the forecastle, aloft there to the royal mast-head. True, they rather order me about some, and make me jump from spar to spar, like a grasshopper in a May meadow. And at first, this sort of thing is unpleasant enough. It touches one's sense of honour, particularly if you come of an old established family in the land, the Van Rensselaers, or Randolphs, or Hardicanutes. And more than all, if just previous to putting your hand into the tar-pot, you have been lording it as a country schoolmaster, making the tallest boys stand in awe of you. The transition is a keen one, I assure you, from a schoolmaster to a sailor, and requires a strong decoction of Seneca and the Stoics to enable you to grin and bear it. But even this wears off in time. What of it, if some old hunks of a sea-captain orders me to get a broom and sweep down the decks? What does that indignity amount to, weighed, I mean, in the scales of the New Testament? Do you think the archangel Gabriel thinks anything the less of me, because I promptly and respectfully obey that old hunks in that particular instance? Who ain't a slave? Tell me that. Well, then, however the old sea-captains may order me about-however they may thump and punch me about, I have the satisfaction of knowing that it is all right; that everybody else is one way or other served in much the same way-either in a physical or metaphysical point of view, that is; and so the universal thump is passed round, and all hands should rub each other's shoulder-blades, and be content. Again, I always go to sea as a sailor, because they make a point of paying me for my trouble, whereas they never pay passengers a single penny that I ever heard of. On the contrary, passengers themselves must pay. And there is all the difference in the world between paying and being paid. The act of paying is perhaps the most uncomfortable infliction that the two orchard thieves entailed upon us. But BEING PAID,-what will compare with it? The urbane activity with which a man receives money is really marvellous, considering that we so earnestly believe money to be the root of all earthly ills, and that on no account can a monied man enter heaven. Ah! how cheerfully we consign ourselves to perdition! Finally, I always go to sea as a sailor, because of the wholesome exercise and pure air of the fore-castle deck. For as in this world, head winds are far more prevalent than winds from astern (that is, if you never violate the Pythagorean maxim), so for the most part the Commodore on the quarter-deck gets his atmosphere at second hand from the sailors on the forecastle. He thinks he breathes it first; but not so. In much the same way do the commonalty lead their leaders in many other things, at the same time that the leaders little suspect it. But wherefore it was that after having repeatedly smelt the sea as a merchant sailor, I should now take it into my head to go on a whaling voyage; this the invisible police officer of the Fates, who has the constant surveillance of me, and secretly dogs me, and influences me in some unaccountable way-he can better answer than any one else. And, doubtless, my going on this whaling voyage, formed part of the grand programme of Providence that was drawn up a long time ago. It came in as a sort of brief interlude and solo between more extensive performances. I take it that this part of the bill must have run something like this: "GRAND CONTESTED ELECTION FOR THE PRESIDENCY OF THE UNITED STATES. "WHALING VOYAGE BY ONE ISHMAEL. "BLOODY BATTLE IN AFFGHANISTAN." Though I cannot tell why it was exactly that those stage managers, the Fates, put me down for this shabby part of a whaling voyage, when others were set down for magnificent parts in high tragedies, and short and easy parts in genteel comedies, and jolly parts in farces-though I cannot tell why this was exactly; yet, now that I recall all the circumstances, I think I can see a little into the springs and motives which being cunningly presented to me under various disguises, induced me to set about performing the part I did, besides cajoling me into the delusion that it was a choice resulting from my own unbiased freewill and discriminating judgment. Chief among these motives was the overwhelming idea of the great whale himself. Such a portentous and mysterious monster roused all my curiosity. Then the wild and distant seas where he rolled his island bulk; the undeliverable, nameless perils of the whale; these, with all the attending marvels of a thousand Patagonian sights and sounds, helped to sway me to my wish. With other men, perhaps, such things would not have been inducements; but as for me, I am tormented with an everlasting itch for things remote. I love to sail forbidden seas, and land on barbarous coasts. Not ignoring what is good, I am quick to perceive a horror, and could still be social with it-would they let me-since it is but well to be on friendly terms with all the inmates of the place one lodges in. By reason of these things, then, the whaling voyage was welcome; the great flood-gates of the wonder-world swung open, and in the wild conceits that swayed me to my purpose, two and two there floated into my inmost soul, endless processions of the whale, and, mid most of them all, one grand hooded phantom, like a snow hill in the air."""
    r=requests.Session()
    response=''
    params={}
    username = 'c9423ec3-0fd5-4f30-b300-0e75bcf95467'
    password = 'R8DH5FzfaDQ9'
    
    text = text.encode("utf-8")
    #post_data={"username":username,"password":password,"data":text}        
    url="https://gateway.watsonplatform.net/personality-insights/api/v2/profile"
    
    '''
    username='61492ca2-e291-42a2-b559-325e9a46f3ec'
    password='EmT0ckJ8ImkH'
    url="https://gateway.watsonplatform.net/personality-insights/api"
    '''

    #try:
    response=r.post(url=url,auth=(username,password),headers = {"content-type": "text/plain"}, data=text)
    #except Exception as e:
    #    print(e)
    twitter_api=oauth_login(userId,request)
    
        
    # Iterate through batches of results by following the cursor until we
    # reach the desired number of results, keeping in mind that OAuth users
    # can "only" make 180 search queries per 15-minute interval. See
    # https://dev.twitter.com/docs/rate-limiting/1.1/limits
    # for details. A reasonable number of results is ~1000, although
    # that number of results may not exist for all queries.
    
    # Enforce a reasonable limit
   # max_results = min(18000, max_results)
    for j in range(rng):
        #print >> sys.stderr, 'j =' + str(j)
        try:
            search_results = twitter_api.statuses.user_timeline(screen_name="AshutoshBhadke", count=200)
            for tweet in search_results:
                statuses += tweet['text']
                print statuses
                print 'Hi'
        except Exception, e: # No more results when next_results doesn't exist
            #print >> sys.stderr, e
            #print >> sys.stderr, "No next_results found=" + next_results
            break
            
            
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
     #   kwargs = dict([ kv.split('=') 
      #                  for kv in next_results[1:].split("&") ])
       
    #print >> sys.stderr, "FOUND: " + str(len(statuses))   
    return HttpResponse(statuses)
    
    
   
    return  HttpResponse(search_results)
'''
def delete_request(val):
    settings = globalSettings()
    settings.client1.connect()
    db = settings.client1["userdb"]
    doc = db[val]
    doc.delete()

    return index(request)
'''    
def delete_query(request):
    settings = globalSettings()
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")

    if(cloudantDB =='primaryDB'):
        settings.client1.connect()
        db = settings.client1['userdb']
    else:
        settings.client2.connect()
        db = settings.client2['userdb']
    #print "Inside delete_request"

    query = qs.get("query")
    rash =  delete_from_db(request,query,'querydb')
    
    return HttpResponse("Document Successfully Deleted")

def delete_request(request):
    settings = globalSettings()
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")

    if(cloudantDB =='primaryDB'):
        settings.client1.connect()
        db = settings.client1['userdb']
    else:
        settings.client2.connect()
        db = settings.client2['userdb']
    print "Inside delete_request"
    
    user = qs.get("user_name")
    rash =  delete_from_db(request,user,'userdb')

    
    return HttpResponse("Document Successfully Deleted")
        
def delete_from_db(request,val,dbname):
    settings = globalSettings()
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")

    if(cloudantDB =='primaryDB'):
        settings.client1.connect()
        db = settings.client1[dbname]
    else:
        settings.client2.connect()
        db = settings.client2[dbname]
    doc = db[val]
    doc.delete()    
    
def add_request(request):
    settings = globalSettings()
    qs=request.GET
    qs=qs.dict()
    val = qs.get("query")
    cloudantDBval = qs.get("cloudantDB")
    #print val
    
    #if(is_present(val,cloudantDBval)==True):
    #    raise NameError("Query already present in the list")
    db = connect_to_db2("querydb",cloudantDBval)

    obj_str_id = insert_to_querydb('querydb',val,db)
    return index(request)

def insert_to_querydb(dbname,val,db):
    settings = globalSettings()
    #db = connect_to_db2("querydb",cloudantDBval)
    doc = {'_id':val}
    obj_id = db.create_document(doc)
    obj_id_str = str(obj_id)
    return obj_id_str

'''def is_present(val,cloudantDB):
    settings = globalSettings()
    db = connect_to_db2("querydb",cloudantDBval)
    record = read_from_querydb("querydb",val)
    if record:
        return True
    else:
        return False 

def read_from_querydb(dbname,val):
    settings = globalSettings()
    db = connect_to_db2("querydb",cloudantDBval)
    record= []
    for docs in db:
        if(docs['doc']['_id']==val):
            return record

    return record 
'''
def connect_to_db(dbname,request):
    settings = globalSettings()
    qs = request.GET
    qs = qs.dict()
    cloudantDB = qs.get("cloudantDB")

    if(cloudantDB =='primaryDB'):
        settings.client1.connect()
        db = settings.client1[dbname]
    else:
        settings.client2.connect()
        db = settings.client2[dbname]
    return db

def index(request):
    settings = globalSettings()
    db=connect_to_db("querydb",request)
    #record,total = read_from_querydb("querydb")
    return HttpResponse("Query added successfully!")
    #return render(request,'/admin.html')

def read_from_db(request):
    settings = globalSettings()
    qs=request.GET
    qs=qs.dict()
    val = qs.get("db")
    
    if (val=="userid"):
        db = connect_to_db("userdb",request)
    else:
        db = connect_to_db("querydb",request)
   
    record= []
    #record = db.all_docs()
    for docs in db:
        record.append(docs)
    print record
    #return record
    return HttpResponse(dumps(record), content_type="application/json")

def connect_to_db2(dbname,cloudantDBval):
    settings = globalSettings()

    if(cloudantDBval =='primaryDB'):
        settings.client1.connect()
        db = settings.client1[dbname]
    else:
        settings.client2.connect()
        db = settings.client2[dbname]
    return db