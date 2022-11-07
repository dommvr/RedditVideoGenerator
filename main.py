import praw
from gtts import gTTS
from moviepy.editor import *
from mutagen.mp3 import MP3
from nltk import tokenize
import re
import os
import math
import magic
import random

clear = lambda: os.system('cls')

class VideoGenerator:

    def __init__(self):
        self.reddit = praw.Reddit(client_id='client_id',
                             client_secret='secret', password='password',
                             user_agent='user_agent', username='username')

        self.mime = magic.Magic(mime=True)

        self.submissions = []
        self.stickied_submissions = []
        self.background_videos = []
        self.files_to_delete = []

    def create_necessary_folders(self):
        self.current_directory = os.getcwd()
        self.folder_directory = os.path.join(self.current_directory, 'Reddit_videos')

        if not os.path.exists(self.folder_directory):
            os.makedirs(self.folder_directory)

        self.folder_directory = os.path.join(self.current_directory, 'Temporary_files')
        self.tf_folder_directory = self.folder_directory

        if not os.path.exists(self.folder_directory):
            os.makedirs(self.folder_directory)

    def options(self):
        #One video + comments
        #Multiple videos + comments
        while True:
            print(f"Which type of video do you want to create?\nOne video [1]\nMultiple videos [2]\nOne video + comments [3]\nMultiple videos + comments [4]")
            self.option = input('Choose an option: ')
            try:
                self.option = int(self.option)
            except:
                pass
            if self.option == 1 or self.option == 3:
                clear()
                while True:
                    self.submission_id = input('Submission ID: ')
                    if VG.submission_exists(self.submission_id):
                        clear()
                        break
                    else:
                        print("Submission with given ID does not exist. Try again.")
                break
            elif self.option == 2 or self.option == 4:
                clear()
                while True:
                    self.subreddit = self.reddit.subreddit(input('Subreddit: '))
                    if VG.subreddit_exists(self.subreddit):
                        break
                    else:
                        print("Subreddit with given name does not exist. Try again.")
                while True:
                    clear()
                    print(f"Submission listing: \nHot [1]\nNew [2]\nTop All Time [3]")
                    self.listing_option = input('Choose an option: ')
                    try:
                        self.listing_option = int(self.listing_option)
                    except:
                        pass
                    if self.listing_option == 1 or self.listing_option == 2 or self.listing_option == 3:
                        break
                while True:
                    clear()
                    self.number_of_submissions = input('Number of submissions: ')
                    try:
                        self.number_of_submissions = int(self.number_of_submissions)
                        clear()
                        break
                    except:
                        pass
                break
            else:
                clear()

    def comment_option(self, submission):
        while True:
            self.comments_limit = input(f"Number of comments for submission '{submission.title}': ")
            try:
                self.comments_limit = int(self.comments_limit)
                clear()
                break
            except:
                pass

    def choose_background_video(self, submission):
        self.current_directory = os.getcwd()
        self.folder_directory = os.path.join(self.current_directory, 'Background_videos')
        self.all_files = os.listdir(self.folder_directory)

        if not os.path.exists(self.folder_directory):
            print('Background_videos folder is required. Please create one.')
            exit()
        for file in self.all_files:
            self.file_path = os.path.join(self.folder_directory, file)
            if os.path.isfile(self.file_path):
                self.file_to_check = self.mime.from_file(self.file_path)
                if self.file_to_check.find('video') != -1:
                    self.background_videos.append(file)
        if len(self.background_videos) == 0:
            print('No video files in Background_videos folder. Please add some.')
            exit()

        while True:
            print(f"Choose background video for submission '{submission.title}':\nRandom video from background_videos folder [1]\nChoose video from background_videos folder [2]")
            self.option = input('Choose an option: ')
            try:
                self.option = int(self.option)
            except:
                pass
            if self.option == 1:
                self.background_video = random.choice(self.background_videos)
                self.background_video = VideoFileClip(os.path.join(self.folder_directory, self.background_video))
                clear()
                break
            elif self.option == 2:
                clear()
                while True:
                    print('Available videos:')
                    for video in self.background_videos:
                        print(video)
                    self.background_video = input('Video name: ')
                    if self.background_video in self.background_videos:
                        self.background_video = VideoFileClip(os.path.join(self.folder_directory, self.background_video))
                        clear()
                        break
                    else:
                        clear()
                break
            else:
                clear()

        return self.background_video

    def submission_exists(self, submission_id):
        self.exists = True
        try:
            (self.reddit.submission(id=submission_id)).selftext
        except:
            self.exists = False
        return self.exists

    def subreddit_exists(self, subreddit):
        self.exists = True
        try:
            self.reddit.subreddits.search_by_name(subreddit, exact=True)
        except:
            self.exists = False
        return self.exists

    def no_stickies(self):
        for submission in self.subreddit.hot(limit=2):
            if submission.stickied:
                self.stickied_submissions.append(submission.id)

    def submission_list(self):
        if self.option == 1 or self.option == 3:
            self.submissions.append(self.reddit.submission(id=self.submission_id))
        else:
            if self.listing_option == 1:
                #hot
                VG.no_stickies()
                self.selected_submissions = self.subreddit.hot(limit=self.number_of_submissions+len(self.stickied_submissions))
                for submission in self.selected_submissions:
                    if submission.id not in self.stickied_submissions:
                        self.submissions.append(submission)
            elif self.listing_option == 2:
                #new
                self.selected_submissions = self.subreddit.new(limit=self.number_of_submissions)
                for submission in self.selected_submissions:
                    self.submissions.append(submission)
            else:
                #top_all_time
                self.selected_submissions = self.subreddit.top("all", limit=self.number_of_submissions)
                for submission in self.selected_submissions:
                    self.submissions.append(submission)

    def go_throw_submissions(self):
        #One video
        #Multiple videos
        if self.option == 1 or self.option == 2:
            for submission in self.submissions:
                if submission.selftext:
                    VG.create_video(submission)

        #One video + comments
        #Multiple videos + comments
        elif self.option == 3 or self.option == 4:
            for submission in self.submissions:
                VG.create_video2(submission)

    def delete_emoji(self, text):
        self.emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U0001F1F2-\U0001F1F4"  # Macau flag
            u"\U0001F1E6-\U0001F1FF"  # flags
            u"\U0001F600-\U0001F64F"
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            u"\U0001f926-\U0001f937"
            u"\U0001F1F2"
            u"\U0001F1F4"
            u"\U0001F620"
            u"\u200d"
            u"\u2640-\u2642"
            "]+", flags=re.UNICODE)

        return self.emoji_pattern.sub(r'', text)

    def create_text(self, submission, audio_length, background_video):
        #One video
        #Multiple videos
        self.video_text = []
        self.text_title = VG.delete_emoji(("".join(x for x in submission.title if x.isalpha() or x.isnumeric() or x.isspace())).replace(" ", "_")+'.txt')
        self.text_title = os.path.join(self.tf_folder_directory, self.text_title) ###
        self.files_to_delete.append(self.text_title) ###
        self.text_file = open(self.text_title, "w")
        self.ready_text = VG.delete_emoji(submission.selftext)
        self.text_file.write(self.ready_text)
        self.text_file.close()
        self.text_file = open(self.text_title, "r")
        self.text = self.text_file.read()
        self.text_file.close()
        self.words_in_text = len(VG.delete_emoji(submission.title).split()) + len(self.text.split())
        self.split_text = tokenize.sent_tokenize(self.text)
        self.split_text.insert(0, VG.delete_emoji(submission.title))

        self.start_time = 0
        for sentence in self.split_text:
            self.words_in_sentence = len(sentence.split())
            self.duration = (self.words_in_sentence / self.words_in_text) * audio_length
            self.sentence = TextClip(sentence, font="Arial-Black", fontsize=35, stroke_width=2.5, color="white", stroke_color="black", method="caption", size=background_video.size)
            self.sentence = self.sentence.set_start(self.start_time)
            self.sentence = self.sentence.set_pos("center").set_duration(self.duration)
            self.video_text.append(self.sentence)
            self.start_time += self.duration

    def create_text2(self, submission_comments, background_video):
        #One video + comments
        #Multiple videos + comments
        self.video_text = []
        self.comments_audio = []
        self.start_time = 0
        for comment in submission_comments:
            self.audio = gTTS(text=comment, lang="en", slow=False)
            self.comment_path = os.path.join(self.tf_folder_directory, (comment[0:10] + ".mp3"))
            self.files_to_delete.append(self.comment_path)
            self.audio.save(self.comment_path)
            self.audio = AudioFileClip(self.comment_path)
            self.comments_audio.append(self.audio)
            self.duration = MP3(self.comment_path).info.length
            self.sentence = TextClip(VG.delete_emoji(comment), font="Arial-Black", fontsize=35, stroke_width=2.5, color="white", stroke_color="black", method="caption", size=background_video.size)
            self.sentence = self.sentence.set_start(self.start_time)
            self.sentence = self.sentence.set_pos("center").set_duration(self.duration)
            self.video_text.append(self.sentence)
            self.start_time += self.duration
        self.audio = concatenate_audioclips(self.comments_audio)
        self.audio.write_audiofile(os.path.join(self.tf_folder_directory, "final_audio.mp3"))
        self.files_to_delete.append(os.path.join(self.tf_folder_directory, "final_audio.mp3"))

    def get_submission_comments(self, submission):
        self.submission_comments = []
        self.submission_comments.append(VG.delete_emoji(submission.title))
        submission.comments.replace_more(limit=0, threshold=0)
        self.x = 1
        for comment in submission.comments:
            self.submission_comments.append(VG.delete_emoji(comment.body))
            if self.x == self.comments_limit:
                break
            self.x += 1

        return self.submission_comments
            
    def create_background_video(self, background_video, additional_video, audio_length):
        if background_video.duration == audio_length:
            pass
        elif background_video.duration > audio_length:
            background_video = background_video.subclip(0, audio_length)
        else:   
            self.video_audio_ratio = math.floor(audio_length / background_video.duration)
            if self.video_audio_ratio > 1:
                for _ in range(self.video_audio_ratio - 1):
                    background_video = concatenate_videoclips([background_video, additional_video])
                background_video = concatenate_videoclips([background_video, additional_video.subclip(0, (audio_length - background_video.duration))])
            else:
                background_video = concatenate_videoclips([background_video, additional_video.subclip(0, (audio_length - background_video.duration))])
        return background_video     

    def create_video(self, submission):
        #One video
        #Multiple videos
        self.background_video = VG.choose_background_video(submission)
        self.audio = gTTS(text=VG.delete_emoji(submission.title + submission.selftext), lang="en", slow=False)
        self.audio_title = VG.delete_emoji(("".join(x for x in submission.title if x.isalpha() or x.isnumeric() or x.isspace())).replace(" ", "_")+'.mp3')
        self.audio_title = os.path.join(self.tf_folder_directory, self.audio_title) ###
        self.video_title = VG.delete_emoji(("".join(x for x in submission.title if x.isalpha() or x.isnumeric() or x.isspace())).replace(" ", "_")+'.mp4')
        self.audio.save(self.audio_title)
        self.audio = AudioFileClip(self.audio_title)
        self.audio_length = MP3(self.audio_title).info.length
        self.files_to_delete.append(self.audio_title) ###
    
        self.final_video = VG.create_background_video(self.background_video, self.background_video, self.audio_length).set_audio(self.audio)
        VG.create_text(submission, self.audio_length, self.background_video)

        for i in range(len(self.video_text)):
            self.final_video = CompositeVideoClip([self.final_video, self.video_text[i]])
        
        self.folder_directory = os.path.join(self.current_directory, 'Reddit_videos')
        self.final_video.write_videofile(os.path.join(self.folder_directory,self.video_title))

    def create_video2(self, submission):
        #One video + comments
        #Multiple videos + comments
        VG.comment_option(submission)
        self.background_video = VG.choose_background_video(submission)
        self.video_title = VG.delete_emoji(("".join(x for x in submission.title if x.isalpha() or x.isnumeric() or x.isspace())).replace(" ", "_")+'.mp4')
        VG.create_text2(VG.get_submission_comments(submission), self.background_video)
        self.audio = AudioFileClip(os.path.join(self.tf_folder_directory, "final_audio.mp3"))
        self.audio_length = MP3(os.path.join(self.tf_folder_directory, "final_audio.mp3")).info.length
        self.final_video = VG.create_background_video(self.background_video, self.background_video, self.audio_length).set_audio(self.audio) 

        for i in range(len(self.video_text)):
            self.final_video = CompositeVideoClip([self.final_video, self.video_text[i]])
        
        self.folder_directory = os.path.join(self.current_directory, 'Reddit_videos')
        self.final_video.write_videofile(os.path.join(self.folder_directory,self.video_title))

    def delete_files(self):
        for path in self.files_to_delete:
            os.remove(path)



VG = VideoGenerator()
VG.create_necessary_folders()
VG.options()
VG.submission_list()
VG.go_throw_submissions()
VG.delete_files()