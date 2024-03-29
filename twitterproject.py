import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import datetime
import pymongo
import time

PAGE_CONFIG = {"page_title":"MyApp"
              }

st.set_page_config(**PAGE_CONFIG)
# REQUIRED VARIABLES
tweets_df = pd.DataFrame()
st.write("# Twitter Search")
option = st.selectbox('Please select the type of search',('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+option, 'covid')
start = st.date_input("Select the start date", datetime.date(2022, 1, 1),key='d1')
end = st.date_input("Select the end date", datetime.date(2023, 1, 1),key='d2')
tweet_c = st.slider('How many tweets to scrape', 0, 1000, 10)
tweets_list = []

# SCRAPE DATA USING TwitterSearchScraper
if word:
    if option=='Keyword':
        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>=tweet_c:
                break
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
    else:
        for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} + since:{start} until:{end}').get_items()):
            if i>tweet_c:
                break            
            tweets_list.append([ tweet.id, tweet.date,  tweet.content, tweet.lang, tweet.user.username, tweet.replyCount, tweet.retweetCount,tweet.likeCount, tweet.source, tweet.url ])
        tweets_df = pd.DataFrame(tweets_list, columns=['ID','Date','Content', 'Language', 'Username', 'ReplyCount', 'RetweetCount', 'LikeCount','Source', 'Url'])
else:
    st.warning(option,' cant be empty', icon="⚠️")

#SIDEBAR
with st.sidebar:   
    st.info('DETAILS', icon="ℹ️")
    if option=='Keyword':
        st.info('Keyword is '+word)
    else:
        st.info('Hashtag is '+word)
    st.info('Starting Date is '+str(start))
    st.info('End Date is '+str(end))
    st.info("Number of Tweets "+str(tweet_c))
    st.info("Total Tweets Scraped are "+str(len(tweets_df)))
 

# DOWNLOAD AS CSV
@st.cache_data # IMPORTANT: Cache the conversion to prevent computation on every rerun
def convert_df(df):    
    return df.to_csv().encode('utf-8')

if not tweets_df.empty:
    col1, col2, col3 = st.columns(3)
    with col1:
        csv = convert_df(tweets_df) # CSV
        c=st.download_button(label="Download data as CSV",data=csv,file_name='Twitter_data.csv',mime='text/csv',)        
    with col2:    # JSON
        json_string = tweets_df.to_json(orient ='records')
        j=st.download_button(label="Download data as JSON",file_name="Twitter_data.json",mime="application/json",data=json_string,)

    with col3: # SHOW
        y=st.button('Show Tweets',key=2)
        
    # UPLOAD DATA TO DATABASE
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # To connect to MONGODB
    mydb = client["Twitter_Database"]    # To create a DATABASE
    if st.button('Upload Tweets to Database'):
        coll=word
        coll=coll.replace(' ','_')+'_Tweets'
        mycoll=mydb[coll]
        dict=tweets_df.to_dict('records')
        if dict:
            mycoll.insert_many(dict) 
            ts = time.time()
            mycoll.update_many({}, {"$set": {"KeyWord_or_Hashtag": word+str(ts)}}, upsert=False, array_filters=None)
            st.success('Successfully uploaded to database', icon="✅")
        else:
            st.warning('Cant upload because there are no tweets', icon="⚠️")


if c:
    st.success("Successfully Downloaded",icon="✅")  
if j:
    st.success("Successfully Downloaded",icon="✅")     
if y: # DISPLAY
    st.success("The Tweets are:",icon="✅")
    st.write(tweets_df)
