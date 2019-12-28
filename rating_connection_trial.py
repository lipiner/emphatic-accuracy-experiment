#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################
# import stuff
from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os
import sys
import numpy as np
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import psychopy.core

import time

from trial import Trial, Constants as C
from trial import LPTAddress, outDuration, trigValStartEx2, trigValEndEx2, isMindWareConnected

#########################################

#########################################
# ## CONSTANTS ## #
# FILES' NAMES
DATA_FILE_NAME = '_RatingLog'
EMOTION_FILE_NAME = '_EmotionsLog'

# FEMALE MESSAGES
PRACTICE_MSG_F = "לפני שנתחיל, קחי קצת זמן להתנסות בסולם המדידה. הזיזי את העכבר להזזת הסמן."
# VIDEOS_BREAK_MSG_F = "סוף סרטון. אנא המתיני לפני מעבר לסרטון הבא"
VIDEOS_BREAK_MSG_F = "בעוד 03 שניות תוכלי לעבור לסרטון הבא."
# MALE MESSAGES
PRACTICE_MSG_M = "לפני שנתחיל, קח קצת זמן להתנסות בסולם המדידה. הזז את העכבר להזזת הסמן."
# VIDEOS_BREAK_MSG_M = "סוף סרטון. אנא המתן לפני מעבר לסרטון הבא"
VIDEOS_BREAK_MSG_M = "בעוד 03 שניות תוכל לעבור לסרטון הבא."
# GENERAL MESSAGES
LOADING_VIDEO_MSG = "הניסוי בטעינה. נא להמתין."
DONE_LOADING_VIDEO_MSG = "הניסוי מוכן!"
BETWEEN_VIDEOS_VALIDITY_CHECK = "נא לקרוא לנסיין/ית"
NEXT_VIDEO_MSG = "להתחלת הסרטון הבא, נא ללחוץ על מקש הרווח"
VIDEO_NOT_LOADED_MSG = "לא ניתן לטעון את הסרטון"
VIDEOS_BREAK_MSG1 = "לאחר שהנסיין/ית יוצא/ת מהחדר,"
VIDEOS_BREAK_MSG2 = "יש ללחוץ על מקש הרווח להתחלת הקלטה של 03 שניות של מדידות רגועות."
VIDEOS_BREAK_MSG3 = "יש לנסות לזוז כמה שפחות ולנסות להישאר רגועים ושלווים."
FINISH_MSG = "זהו! סיימת! נא לפתוח את הדלת ולהודיע לנסיין/נסיינית על סוף הניסוי."
FINISH_MSG2 = "יש להישאר בישיבה עד הגעת הנסיין/נסיינית."
# REMINDER_MSG = "Press the space bar once you feel comfortable using this slider"  # removed!
FILLER_MSG = "תגובות נרשמות"

# RATING SCALE INFO
SCALE_HEIGHT = 1
SCALE_WIDTH = 480
SCALE_NONE_LABEL = "שלילי"  # "None"
SCALE_VERY_LABEL = "חיובי"  # "very"
LABEL_SIZE = 20
SCALE_CENTER_HEIGHT = 20
SCALE_CENTER_WIDTH = 1
HANDLE_RADIUS = 10
SLIDER_BEGIN_X = -240
SLIDER_END_X = 240

# RECORD EMOTION RATE INFO
TIME_INTERVAL = 0.5  # how frequently to sample / record scale responses

PRACTICE_MOV_FILE = 'practice_video.mp4'

# EMOTION RATING
EMOTIONS_LIST = ["מבוכה", "כעס", "עצב", "שמחה", "גועל", "גאווה", "פחד", "התרגשות"]
CHOOSE_INST_MSG_M = "דרג עם הספרות ולחץ אנטר"
CHOOSE_INST_MSG_F = "דרגי עם הספרות ולחצי אנטר"
RATES_OPTIONS = "9   8   7   6   5   4   3   2   1"
RATES_LABELS = "במידה רבה                               כלל לא"
MIN_RATE = 1
MAX_RATE = 9
INVALID_RATE_MSG = "קלט לא חוקי. נא לנסות שוב"

MOV_IDX = 0
TRIG_START_IDX = 1
TRIG_END_IDX = 2

BASELINE_START_TRIGGER = 12
BASELINE_END_TRIGGER = 13

QUIT_TRIAL_KEY = ['q']
EEG_AUDIO_SCREEN = '+'
between_videos_check = False

#########################################


class RatingConnectionTrial (Trial):
    """
    The rating videos' emotion part of the trial
    """
    def __init__(self, experiment_folder):
        """
        Initialize the trial object
        """
        Trial.__init__(self)
        self.__experiment_folder = experiment_folder
        self.emotions_file = self.create_emotions_file()
        self.videos_name = []

    def create_emotions_file(self):
        """
        Creates emotions output file
        :return: The emotions file object
        """
        pass

    def set_gender(self, gender):
        """
        Sets the gender of the screen messages to fit the sub's gender
        :param gender: The gender of the sub
        """
        if gender == C.MALE:
            self.__practice_msg = PRACTICE_MSG_M
            self.__choose_inst_msg = CHOOSE_INST_MSG_M
            self.__videos_break_time_msg = VIDEOS_BREAK_MSG_M
        else:
            self.__practice_msg = PRACTICE_MSG_F
            self.__choose_inst_msg = CHOOSE_INST_MSG_F
            self.__videos_break_time_msg = VIDEOS_BREAK_MSG_F
        # self.__reminder_msg = REMINDER_MSG
        self.__loading_video_msg = LOADING_VIDEO_MSG
        self.__done_loading_video_msg = DONE_LOADING_VIDEO_MSG
        self.__finish_msg = FINISH_MSG
        self.__invalid_rate_msg = INVALID_RATE_MSG
        Trial.set_gender(self, gender)

    def play_video(self, video_info, scale, video_id=0, is_practice=False):
        """
        Plays the given video with the rating dial
        :param video_info: a tuple of: (movie or audio object, trigger value)
        :param scale: a scale object
        :param video_id: the movie number (its index in self.videos_name + 1)
        :param is_practice: a boolean parameter for practice trial (default=False)
        """
        # sets the keys to stop the video
        stop_key_list = ['escape']
        if is_practice:
            mov = video_info
        else:
            mov = video_info[MOV_IDX]

        if not is_practice:
            ################################################################
            # Sending start triggers to MindWare here - BrainLabWorks Ltd. #
            ################################################################
            self.sending_mindware_triggers(video_info[TRIG_START_IDX])

        # # in case it's a practice - shows instructions and updates the stop key list
        # if is_practice:
        #     # stop_key_list.append('space')
        #     self.draw_text(self.__practice_msg, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=100,
        #                    wrap_width=C.INSTRUCTION_WIDTH)
        #     self.draw_advance()

        # prepare the video and the scale
        if scale:
            scale.set_draw()
        try:
            video_duration = mov.duration
            mov.setAutoDraw(True)
        except AttributeError:
            video_duration = mov.getDuration()
            mov.play()
        self.win.flip()
        # recording data info
        start_time = time.time()
        i = 0

        self.mouse.getPos()  # gets the current pos so the getRel will be reset to the current position
        # while video.status != visual.FINISHED and not event.getKeys(stop_key_list):
        while time.time() <= start_time + video_duration and not event.getKeys(stop_key_list):
            if scale:
                mouse_x = scale.move_mouse()  # update the scale and gets the value for saving

                if not is_practice:  # saves data
                    cur_time = time.time()
                    # query and record rating info every 0.1 seconds
                    if (cur_time - start_time) >= (TIME_INTERVAL * i):
                        i += 1
                        # normalize the slider value between 0 to 100
                        slider_value = round((mouse_x - SLIDER_BEGIN_X) / (SLIDER_END_X - SLIDER_BEGIN_X) * 100, 0)
                        output_time = round(cur_time - start_time, 2)
                        self.save_emotion_data(slider_value, output_time, video_id)
            else:
                # there is no scale object - meaning run EEG trial without rating dial
                self.draw_text(EEG_AUDIO_SCREEN, C.WIN_CENTER_ALIGN, height=100)  # when no scale, draws fixation
                self.win.flip()

        # # the video has ended but user didn't press at the stop key on practice mode
        # if is_practice and video.status == visual.FINISHED:
        #     reminder = self.draw_text(self.__reminder_msg, C.WIN_CENTER_ALIGN, height=20, wrap_width=400)
        #     # replace practice video with instructions
        #     while not event.getKeys(stop_key_list):
        #         reminder.draw()
        #         scale.move_mouse()

        # video has ended or key interrupted
        try:
            mov.setAutoDraw(False)
        except AttributeError:
            mov.stop()  # the file is an audio

        if scale:
            scale.set_off()

        # changes the screen to give participants something to look at during the weird lag
        self.draw_text(FILLER_MSG, wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()

        if not is_practice:
            ##############################################################
            # Sending end triggers to MindWare here - BrainLabWorks Ltd. #
            ##############################################################
            self.sending_mindware_triggers(video_info[TRIG_END_IDX])

        self.rate_emotions(video_id, not is_practice)  # saves the emotions ratings

    def additional_questions(self):
        """
        shows any additional questions
        """
        return []

    def save_emotion_data(self, rating, record_time, movie_id):
        """
        Saves the data of the user's emotions rating while watching the video
        :param rating: sub's rating
        :param record_time: The time it was recorded
        :param movie_id: The movie id that is being recorded
        """
        pass

    def prepare_videos(self, files_list=None):
        """
        Prepare the videos for the trial- loads the needed videos. Must be implemented in each trial class that
        inheritance from this class and uses this class's start_experiment method
        :param files_list: list of videos files to load. If not specified, take all the files in the videos dir
        :return: list of movie objects, contains all the videos objects for the trial
        """
        return []  # returns an empty list so it won't crash in case the function won't be implemented by derived class

    def show_instructions(self):
        """
        The function shows the trial's first instructions for the begging of the trial.
        Should be implemented in each trial class that
        inheritance from this class with its own instructions
        """
        pass

    def show_trial_instructions(self):
        """
        The function shows the trial's instructions- instructions for begging the actual trial part.
        Should be implemented in each trial class that
        inheritance from this class with its own instructions
        """
        pass

    def rate_emotions(self, movie_id, save_data):
        """
        Asks the user to rate its emotions.
        :param movie_id: the current movie id
        :param save_data: boolean parameter to determine whether or not to save the data
        """
        emotion_rates = [self.videos_name[movie_id - 1]]  # adds the video file name to the list for first column
        # Rating options - should be presented for all the emotions so is being autoDraw
        m2 = self.draw_text(RATES_OPTIONS, C.WIN_CENTER_ALIGN, y_pos=150, wrap_width=C.INSTRUCTION_WIDTH)
        m3 = self.draw_text(RATES_LABELS, C.WIN_CENTER_ALIGN, x_pos=20, y_pos=115, wrap_width=C.INSTRUCTION_WIDTH)
        m4 = self.draw_text(self.__choose_inst_msg, C.WIN_CENTER_ALIGN, y_pos=-200, wrap_width=C.INSTRUCTION_WIDTH)
        m2.setAutoDraw(True)
        m3.setAutoDraw(True)
        m4.setAutoDraw(True)
        for emotion in EMOTIONS_LIST:
            # presents the question for the current emotion
            question = self.scale_q + emotion + "?"
            m1 = self.draw_text(question, C.WIN_CENTER_ALIGN, y_pos=250, wrap_width=C.INSTRUCTION_WIDTH)
            m1.setAutoDraw(True)  # should be presented the whole time while the user is writing his rate
            self.win.flip()  # replace and show the current emotion
            rate = self.get_user_input()
            while rate != C.QUIT_KEY_MARK and (not rate.isdigit() or int(rate) < MIN_RATE or int(rate) > MAX_RATE):
                # while the user input is invalid (not a number from 1 to 9 but not the escape key for quiting)
                self.draw_text(self.__invalid_rate_msg, C.WIN_CENTER_ALIGN, wrap_width=C.INSTRUCTION_WIDTH)
                self.win.flip()
                rate = self.get_user_input()
            emotion_rates.append(rate)  # adds the rate
            m1.setAutoDraw(False)  # remove the last emotion from the screen
        # remove all messages
        m2.setAutoDraw(False)
        m3.setAutoDraw(False)
        m4.setAutoDraw(False)

        additional_ans = self.additional_questions()

        if save_data:
            self.emotions_file.write((C.CELLS_DELIMITER.join(emotion_rates + additional_ans) +
                                      C.ROW_DELIMITER).encode('UTF-16'))

    def start_experiment(self):
        """
        Main method of the experiment. Runs the whole experiment
        """
        self.draw_text(self.__loading_video_msg, wrap_width=1000)
        self.win.flip()

        # Load sub's videos
        practice_mov = self.load_video(self.__experiment_folder + PRACTICE_MOV_FILE)
        videos_list = self.prepare_videos()

        # Alert experimenter that the videos have been loaded
        self.draw_text(self.__done_loading_video_msg)
        self.draw_advance()

        self.baseline()  # runs baseline

        self.show_instructions()  # shows this part of the trial instructions

        scale = self.Scale(self)  # creates scale object
        self.play_video(practice_mov, scale, is_practice=True)  # play practice video

        # continue with instructions for real part
        self.show_trial_instructions()
        video_id = 1  # starting from 1 for displaying but reduce 1 later for right indexing
        tries = 0  # in case there are unloaded videos due to MemoryError
        videos_num = len(videos_list)
        while tries < 2 and video_id < len(self.videos_name):
            for video in videos_list:
                try:
                    video_duration = video[MOV_IDX].duration
                except AttributeError:
                    video_duration = video[MOV_IDX].getDuration()
                if video_duration < 0:
                    continue  # ERROR

                self.play_video(video, scale, video_id)  # play trial video

                if video_id < len(videos_list):
                    self.between_videos_instructions()
                    video_id += 1

            # check if there are more videos that could not be loaded before
            if video_id < len(self.videos_name):
                # There are some unloaded videos
                self.draw_text("נא להמתין", wrap_width=C.INSTRUCTION_WIDTH)
                self.win.flip()
                del videos_list
                additional_videos = self.videos_name[video_id:]
                self.videos_name = self.videos_name[:video_id]
                videos_list = self.prepare_videos(additional_videos)
                videos_num += len(videos_list)
                if len(videos_list) > 0:
                    self.between_videos_instructions()
                else:
                    break
            tries += 1

        if len(self.videos_name) - video_id == 0:
            print "all videos were successfully loaded"
        else:
            print "*** ATTENTION ****"
            print str(len(self.videos_name) - video_id) + " VIDEO/S COULD NOT BE LOADED"
            print self.videos_name[video_id:]

        # done experiment
        self.draw_text(self.__finish_msg, wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(FINISH_MSG2, y_pos=-35, wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()
        self.wait_for_input(['space', 'escape'])

    def between_videos_instructions(self, fixation=True):
        """
        Shows instructions for loading more videos
        """
        if fixation:
            if between_videos_check:
                # calling for the experimenter msg
                self.draw_text(BETWEEN_VIDEOS_VALIDITY_CHECK, C.WIN_CENTER_ALIGN, y_pos=150,
                               wrap_width=C.INSTRUCTION_WIDTH)
                self.win.flip()
                if event.waitKeys(keyList=['space', 'escape'] + QUIT_TRIAL_KEY)[0] in QUIT_TRIAL_KEY:
                    self.close()
                self.draw_text(VIDEOS_BREAK_MSG1, C.WIN_CENTER_ALIGN, y_pos=70, wrap_width=C.INSTRUCTION_WIDTH)
            # There are more videos to rate - prints continues message
            # waits for 30 seconds between videos in case this is not the last video
            self.draw_text(VIDEOS_BREAK_MSG2, C.WIN_CENTER_ALIGN, y_pos=0, wrap_width=C.INSTRUCTION_WIDTH)
            self.draw_text(VIDEOS_BREAK_MSG3, C.WIN_CENTER_ALIGN, y_pos=-70, wrap_width=C.INSTRUCTION_WIDTH)
            self.win.flip()
            if event.waitKeys(keyList=['space', 'escape'] + QUIT_TRIAL_KEY)[0] in QUIT_TRIAL_KEY:
                self.close()
            self.sending_mindware_triggers(BASELINE_START_TRIGGER)
            self.break_time_sleep(self.__videos_break_time_msg, VIDEOS_BREAK_MSG3)
            self.sending_mindware_triggers(BASELINE_END_TRIGGER)

        # next video message
        self.draw_text(NEXT_VIDEO_MSG, C.WIN_CENTER_ALIGN, y_pos=150, wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()
        if event.waitKeys(keyList=['space', 'escape']+QUIT_TRIAL_KEY)[0] in QUIT_TRIAL_KEY:
            self.close()

    def close(self):
        self.emotions_file.close()
        Trial.close(self)

    class Scale:
        """
        A scale object containing all the sub-objects and information related to the scale
        """
        def __init__(self, trial):
            """
            Initialize the scale with creating the object from which it is composed
            :param trial: The outer trial object that the scale is related to
            """
            # Defines the position of the scale
            self.__x = 0
            self.__y = -200
            self.__trial = trial
            self.__rating_scale = self.__draw_rectangle(SCALE_HEIGHT, SCALE_WIDTH)  # Draw Rating scale
            self.__scale_center = self.__draw_rectangle(SCALE_CENTER_HEIGHT, SCALE_CENTER_WIDTH)  # mark the center
            self.__handle = self.__draw_circle()
            self.__mouse_x = 0  # mouse start position in x-axis

            # Draw Labels (creates the label objects without drawing them)
            label_y = self.__y - 25  # The position in y-axis of the labels
            # Draw "None" label
            self.__none_label = self.__trial.draw_text(SCALE_NONE_LABEL, x_pos=SLIDER_BEGIN_X,
                                                       y_pos=label_y, height=LABEL_SIZE, to_draw=False)
            # Draw "Very" label
            self.__very_label = self.__trial.draw_text(SCALE_VERY_LABEL, x_pos=SLIDER_END_X,
                                                       y_pos=label_y, height=LABEL_SIZE, to_draw=False)

            title_y = C.VIDEO_Y + 225
            self.__title1 = self.__trial.draw_text(self.__trial.scale_instr1, y_pos=title_y,
                                                   height=25, wrap_width=650, to_draw=False)
            self.__title2 = self.__trial.draw_text(self.__trial.scale_instr2, y_pos=title_y-30,
                                                   height=25, wrap_width=550, to_draw=False)

        def __draw_rectangle(self, height=0.5, width=0.5):
            """
            Creates a rectangle of given width and height using psychopy.visual.Rect.
            :param height: The default value is 0.5 (same as the Rect function default value)
            :param width: The default value is 0.5 (same as the Rect function default value)
            :return: The Rect object
            """
            return psychopy.visual.Rect(self.__trial.win, height=height, width=width, pos=[self.__x, self.__y])

        def __draw_circle(self, radius=HANDLE_RADIUS):
            """
            Creates a rectangle of given width and height using psychopy.visual.Rect.
            :param radius: The default value is 0.5 (same as the Rect function default value)
            :return: The Rect object
            """
            return psychopy.visual.Circle(self.__trial.win, radius=radius, pos=[self.__x, self.__y])

        def set_draw(self):
            """
            Prepare the scale: sets all the scale's object to be autoDraw and sets the needed values for start
            """
            self.__mouse_x = 0  # mouse start position in x-axis
            self.__trial.mouse.setPos()  # moves the mouse to the center so it won't get stuck at the end of the screen
            self.__handle.setPos([self.__mouse_x, self.__y])  # nullify the handle to the center
            self.__rating_scale.setAutoDraw(True)
            self.__scale_center.setAutoDraw(True)
            self.__handle.setAutoDraw(True)
            self.__none_label.setAutoDraw(True)
            self.__very_label.setAutoDraw(True)
            self.__title1.setAutoDraw(True)
            self.__title2.setAutoDraw(True)

        def set_off(self):
            """
            Clear the scale: remove all the scale's drawn objects
            """
            self.__rating_scale.setAutoDraw(False)
            self.__scale_center.setAutoDraw(False)
            self.__handle.setAutoDraw(False)
            self.__none_label.setAutoDraw(False)
            self.__very_label.setAutoDraw(False)
            self.__title1.setAutoDraw(False)
            self.__title2.setAutoDraw(False)

        def move_mouse(self):
            """
            Update the scale's slider value depending on the current position of the mouse in related to the last
            measured position
            :return: The current value of the slider
            """
            mouse_rel = self.__trial.mouse.getRel()  # gets the position in related to the previous one
            self.__mouse_x += mouse_rel[0]
            # Make sure the mouse is not out of the borders of the scale
            if self.__mouse_x > SLIDER_END_X:
                self.__mouse_x = SLIDER_END_X
            if self.__mouse_x < SLIDER_BEGIN_X:
                self.__mouse_x = SLIDER_BEGIN_X
            self.__handle.setPos([self.__mouse_x, self.__y])  # updates scale position
            # Draw changes
            self.__handle.draw()
            self.__trial.win.flip()

            return self.__mouse_x
