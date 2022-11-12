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
 - If you want to change font, font size or font color just edit this parameters. You will find theme in `create_text()` and `create_text2()` functions. TextClip documentation: https://moviepy-tburrows13.readthedocs.io/en/improve-docs/ref/VideoClip/TextClip.html
 ``` 
 self.sentence = TextClip(sentence, font="Arial-Black", fontsize=35, stroke_width=2.5, color="white", stroke_color="black", method="caption", size=background_video.size)
 ```
 ```
 self.sentence = TextClip(VG.delete_emoji(comment), font="Arial-Black", fontsize=35, stroke_width=2.5, color="white", stroke_color="black", method="caption", size=background_video.size)
```
 #### All done, now you can create your own customized Reddit videos
