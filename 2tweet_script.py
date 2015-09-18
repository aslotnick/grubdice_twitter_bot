import twitter
import urllib
import json
import datetime

token=""
token_key=""
con_secret=""
con_secret_key=""

def daily_tweeter():
    tt = twitter.Twitter(auth=twitter.OAuth(token,token_key,con_secret,con_secret_key))
    response = urllib.urlopen('http://grubdice.co/api/public/score')
    html = response.read()
    j=json.loads(html)
    n=datetime.datetime.now().strftime('%A %B %d, %Y')
    first_name=[]
    second_name=[]
    third_name=[]
    for row in j:
        if row['place']==1:
            first_name.append(row['name'])
            first_score=row['score']
        if row['place']==2:
            second_name.append(row['name'])
            second_score=row['score']
        if row['place']==3:
            third_name.append(row['name'])
            third_score=row['score']        
    tweet="""#grubdice Leaderboard for {}
1st: {} ({})
2nd: {} ({})
3rd: {} ({})""".format(n,', '.join(first_name),first_score,', '.join(second_name),second_score,', '.join(third_name),third_score)
    print datetime.datetime.now()
    if datetime.datetime.now().hour == 15: #3pm GMT
        print tweet
        tt.statuses.update(status=tweet)

def hourly_update_tweeter():
    response = urllib.urlopen('http://grubdice.co/api/public/score')
    html = response.read()
    current_state=json.loads(html)
    with open('state.txt','rw') as state:
        prior_state=json.loads(state.read())
    if not prior_state==current_state:
        with open('state.txt','w') as state:
            state.write(json.dumps(current_state))
    changes=[]
    for prow in prior_state:
        for crow in current_state:   
            if prow['name'] == crow['name']:
                if not prow['place']==crow['place']:
                    changes.append({'name':prow['name'],'old_place':prow['place'],'old_score':prow['score'],'new_place':crow['place'],'new_score':crow['score']})
    tweet='#grubdice ranking update\n'
    for i in changes:
        tweet +=  i['name'] + ': '+str(i['old_place'])+' -> '+str(i['new_place'])+'\n'
    print tweet
    tt = twitter.Twitter(auth=twitter.OAuth(token,token_key,con_secret,con_secret_key))
    if len(tweet)>140:
        small_tweet=''
        for line in tweet.split('\n'):
            if len(small_tweet+line+'\n')<=140:
                small_tweet=small_tweet+line+'\n'
        tweet=small_tweet
    if not changes ==[]:
        tt.statuses.update(status=tweet)

if __name__ == "__main__":
    daily_tweeter()
    hourly_update_tweeter()
