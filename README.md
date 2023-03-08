# twitter-scraping-with-streamlit

By using the “snscrape” Library, Scraping the twitter data from Twitter.
Creating a dataframe with date, id, url, tweet content, user,reply count, retweet count,language, source, like count.
Storing each collection of data into a document into Mongodb along with the hashtag or key word we use to  Scrape from twitter. 

Created a GUI using streamlit that contains the feature to enter the keyword or Hashtag to be searched, select the date range and limit the tweet count. After scraping, the data is displayed in the page and buttons are available to upload the data into Database and download the data into csv and json format.

http://192.168.1.8:8501 here you can checkout the streamlit app i've developed to scrape twitter data.
