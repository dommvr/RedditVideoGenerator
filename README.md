# RedditVideoGenerator

Simple project that automatically creates TikTok style videos based on reddit posts and comments

# Setup

Change PRAW token information 

 - Get token information: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
``` 
self.reddit = praw.Reddit(client_id='client_id',
                             client_secret='secret', password='password',
                             user_agent='user_agent', username='username')
```

 - Add your background videos to `Background_videos`

 #### All done, now you can create your own customized Reddit videos
