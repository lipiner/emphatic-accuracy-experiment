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

import time, random

from trial import Trial, Constants as C
from rating_connection_trial import RatingConnectionTrial
from rating_connection_trial import DATA_FILE_NAME, EMOTION_FILE_NAME, EMOTIONS_LIST
from trial import (trigValStartEx2_full, trigValEndEx2_full, trigValStartEx2_videoOnly, trigValEndEx2_videoOnly,
                   trigValStartEx2_audioOnly, trigValEndEx2_audioOnly, isEEG)

#########################################

#########################################
# ## CONSTANTS ## #
# PATH
DATA_FILE_TITLES = 'SubID,MovieID,Serial,Rating,Time,Version\n'
VIDEOS_DIR = ".\\part_b_videos"
REGULAR_VIDEOS_MARK = "_Full"
AUDIOLESS_VIDEOS_MARK = "_VideoOnly"
AUDIO_VIDEOS_MARK = "_AudioOnly"

# FEMALE MESSAGES
INSTRUCTIONS1_MSG_F = "בניסוי זה יופיעו סיפורים שונים. תוך כדי הסיפור, חשבי מה היו רגשות"
INSTRUCTIONS2_MSG_F = "מספר/ת הסיפור בזמן הקלטת הסיפור."
INSTRUCTIONS4_2_MSG_F = "שימי לב, יש לדרג את רגשות המספר/ת בזמן שהם סיפרו את הסיפור."
INSTRUCTIONS5_MSG_F = "שימי לב, כעת לפעמים לא תהיי חשופה לכל הסיפור. יהיו מקרים בהם תראי"
INSTRUCTIONS5_EEG_COND_MSG_F = "שימי לב, לפעמים לא תהיי חשופה לכל הסיפור. יהיו מקרים בהם תראי"
INSTRUCTIONS6_MSG_F = "את מספר/ת הסיפור ללא קול, יהיו מקרים בהם רק תשמעי את הסיפור ללא"
INSTRUCTIONS7_MSG_F = "תמונה ויהיו מקרים בהם גם תראי וגם תשמעי את מספר/ת הסיפורים."
INSTRUCTIONS8_MSG_F = "יש לנסות להיות כמה שיותר מדויק בעזרת הנתונים שיש לך."
TRIAL_INSTRUCTION_MSG2_F = "זכרי להזיז את הסמן כדי לדווח על העוצמה ועל כיוון הרגש של מספר/ת"
TRIAL_INSTRUCTION_MSG2_EEG_COND_F = "זכרי לחשוב מה לדעתך היו רגשות מספר/ת הסיפור בכל רגע נתון בזמן הקלטת הסיפור."
TRIAL_INSTRUCTION_MSG3_F = "הסיפור בכל רגע נתון בזמן הקלטת הסיפור."
TRIAL_INSTRUCTION_MSG4_F = "לאחר יציאת הנסיינית יש ללחוץ על מקש הרווח להצגת הסרטון הראשון."
ADDITION_Q_F = "האם את מכירה את מספר/ת הסיפור? ]כ[ן ]ל[א"  # "Is that correct? [Y]es / [N]o:"
# MALE MESSAGES
INSTRUCTIONS1_MSG_M = "בניסוי זה יופיעו סיפורים שונים. תוך כדי הסיפור, חשוב מה היו רגשות"
INSTRUCTIONS2_MSG_M = "מספר/ת הסיפור בזמן הקלטת הסיפור."
INSTRUCTIONS4_2_MSG_M = "שים לב, יש לדרג את רגשות המספר/ת בזמן שהם סיפרו את הסיפור."
INSTRUCTIONS5_MSG_M = "שים לב, כעת לפעמים לא תהיה חשוף לכל הסיפור. יהיו מקרים בהם תראה"
INSTRUCTIONS5_EEG_COND_MSG_M = "שים לב, לפעמים לא תהיה חשוף לכל הסיפור. יהיו מקרים בהם תראה"
INSTRUCTIONS6_MSG_M = "את מספר/ת הסיפור ללא קול, יהיו מקרים בהם רק תשמע את הסיפור ללא"
INSTRUCTIONS7_MSG_M = "תמונה ויהיו מקרים בהם גם תראה וגם תשמע את מספר/ת הסיפורים."
INSTRUCTIONS8_MSG_M = "יש לנסות להיות כמה שיותר מדויק בעזרת הנתונים שיש לך."
TRIAL_INSTRUCTION_MSG2_M = "זכור להזיז את הסמן כדי לדווח על העוצמה ועל כיוון הרגש של מספר/ת"
TRIAL_INSTRUCTION_MSG2_EEG_COND_M = "זכרי לחשוב מה לדעתך היו רגשות מספר/ת הסיפור בכל רגע נתון בזמן הקלטת הסיפור."
TRIAL_INSTRUCTION_MSG3_M = "הסיפור בכל רגע נתון בזמן הקלטת הסיפור."
TRIAL_INSTRUCTION_MSG4_M = "לאחר יציאת הנסיינית יש ללחוץ על מקש הרווח להצגת הסרטון הראשון."
ADDITION_Q_M = "האם אתה מכיר את מספר/ת הסיפור? ]כ[ן ]ל[א"  # "Is that correct? [Y]es / [N]o:"
# GENERAL MESSAGES
INSTRUCTIONS3_MSG = "כעת, המשימה שלך היא לדווח על כיוון ועוצמת הרגש של מספר/ת הסיפור, בכל זמן"
INSTRUCTIONS4_MSG = "נתון לאורך כל הסרטון, על ידי הזזת העכבר ימין או שמאל על סולם המדידה."
INSTRUCTIONS9_MSG = "לצפייה בדוגמא, יש ללחוץ על מקש הרווח."
TRIAL_INSTRUCTION_MSG1 = "זה הזמן להתחיל את הניסוי."
INSTRUCTIONS3_EEG_COND_MSG = "המשימה שלך היא לחשוב על מה היו לדעתך רגשות מספר/ת הסיפור,"
INSTRUCTIONS4_EEG_COND_MSG = "בכל זמן נתון לאורך כל הסרטון."
INSTRUCTIONS9_EEG_COND_MSG = "כאשר אין וידאו, יש להקשיב לסיפור ולהסתכל על ה + שבמרכז. אין לעצום עיניים."
FINISH_EEG_COND_MSG = "חלק זה של הניסוי הסתיים. נא לקרוא לנסיין/ית"

# instruction text
CONTINUE_FOR_EXAMPLE_MSG = "לקבלת דוגמה יש ללחוץ על כל מקש"  # "Press any key to continue"
SCALE_INSTRUCTIONS1 = "מה לדעתך הייתה העוצמה והכיוון של הרגש של מספר/ת הסיפור"
SCALE_INSTRUCTIONS2 = "בכל רגע נתון, בזמן הקלטת הסיפור?"
SCALE_QUESTION_MSG = "לדעתך, בזמן הקלטת הסיפור, עד כמה מספר/ת הסיפור הרגיש/ה תחושת "

# OTHER
NO_KEY = ['k']
YES_KEY = ['f']
YES_NO_VALUES = {NO_KEY[0]: "NO", YES_KEY[0]: "YES", 'escape': 'ESCAPE'}
EMOTIONS_FILE_ADDITION_TITLES = ["מכיר את המספר"]
VERSIONS_NUM = 3
VIDEOS_NUM = 3  # number of videos of each type (videos/audios/full)

#########################################


class RatingTrialPartBTrial(RatingConnectionTrial):
    """
    Part B of the trial.
    Rating videos' emotion part of the trial - subjects rate partner's video
    """

    def __init__(self, sub_id=None, gender=None, version=None):
        """
        Initialize the trial object
        :param sub_id: the subject id, if known
        :param gender: the gender, if known
        :param version: the version of the trial, if known
        """
        # will be initialized in __check_trial_validity method
        self.__output_file_name = None

        if sub_id is not None and gender is not None and version in range(1, VERSIONS_NUM + 1):
            self.__sub_id = sub_id
            self.set_gender(gender)
        else:
            self.__sub_id, version = self.initialize_trial(VERSIONS_NUM)

        # checks if the subject_id is existed and valid
        while not self.__check_trial_validity():
            self.__sub_id, version = self.initialize_trial(VERSIONS_NUM)
        self.__version = str(version)
        self.__videos_dir = VIDEOS_DIR + self.__version
        RatingConnectionTrial.__init__(self, C.EXPERIMENT2_FOLDER)
        self.__eeg_videos = []
        self.__eeg_cond = False  # eeg trials should not be presented

    def __check_trial_validity(self):
        """
        Creates a folder for the new subject. If a folder with that subject id is already existed, the user
        can override it and continue or not.
        :return: True if the folder exists at the end of the method (when it was already existed and the user wished
        to continue or the folder was just created). False if the folder is already existed and the user canceled.
        """
        self.__sub_folder = C.EXPERIMENT2_FOLDER + str(self.__sub_id)

        path_validity = Trial.check_path(self.__sub_folder)
        if path_validity:
            os.mkdir(self.__sub_folder)  # creates the folder

        # Open output file and write header
        self.__output_file_name = self.__sub_folder + C.FILE_NAME_SEPARATOR + str(self.__sub_id) + DATA_FILE_NAME + \
            C.DATA_FILE_EXTENSION

        return path_validity

    def create_data_file(self):
        """
        Creates data output file
        :return: The output file object
        """
        return Trial.create_file(self.__output_file_name, DATA_FILE_TITLES)

    def create_emotions_file(self):
        """
        Creates emotions output file
        :return: The emotions file object
        """
        file_name = self.__sub_folder + C.FILE_NAME_SEPARATOR + str(self.__sub_id) + EMOTION_FILE_NAME + \
            C.DATA_FILE_EXTENSION
        # decode and encode for the Hebrew
        titles = "MovieID" + C.CELLS_DELIMITER + C.CELLS_DELIMITER.join(
            EMOTIONS_LIST + EMOTIONS_FILE_ADDITION_TITLES).decode('UTF-8') + C.ROW_DELIMITER
        return Trial.create_file(file_name, titles.encode('UTF-16'))

    def set_gender(self, gender):
        """
        Sets the gender of the screen messages to fit the sub's gender
        :param gender: The gender of the sub
        """
        if gender == C.MALE:
            self.__instr1 = INSTRUCTIONS1_MSG_M
            self.__instr2 = INSTRUCTIONS2_MSG_M
            self.__instr4_2 = INSTRUCTIONS4_2_MSG_M
            self.__instr5 = INSTRUCTIONS5_MSG_M
            self.__instr5_eeg = INSTRUCTIONS5_EEG_COND_MSG_M
            self.__instr6 = INSTRUCTIONS6_MSG_M
            self.__instr7 = INSTRUCTIONS7_MSG_M
            self.__instr8 = INSTRUCTIONS8_MSG_M
            self.__trial_instr_msg2 = TRIAL_INSTRUCTION_MSG2_M
            self.__trial_eeg_instr_msg2 = TRIAL_INSTRUCTION_MSG2_EEG_COND_M
            self.__trial_instr_msg3 = TRIAL_INSTRUCTION_MSG3_M
            self.__trial_instr_msg4 = TRIAL_INSTRUCTION_MSG4_M
            self.__addition_q = ADDITION_Q_M
        else:
            self.__instr1 = INSTRUCTIONS1_MSG_F
            self.__instr2 = INSTRUCTIONS2_MSG_F
            self.__instr4_2 = INSTRUCTIONS4_2_MSG_F
            self.__instr5 = INSTRUCTIONS5_MSG_F
            self.__instr5_eeg = INSTRUCTIONS5_EEG_COND_MSG_F
            self.__instr6 = INSTRUCTIONS6_MSG_F
            self.__instr7 = INSTRUCTIONS7_MSG_F
            self.__instr8 = INSTRUCTIONS8_MSG_F
            self.__trial_instr_msg2 = TRIAL_INSTRUCTION_MSG2_F
            self.__trial_eeg_instr_msg2 = TRIAL_INSTRUCTION_MSG2_EEG_COND_F
            self.__trial_instr_msg3 = TRIAL_INSTRUCTION_MSG3_F
            self.__trial_instr_msg4 = TRIAL_INSTRUCTION_MSG4_F
            self.__addition_q = ADDITION_Q_F
        self.__instr3 = INSTRUCTIONS3_MSG
        self.__instr4 = INSTRUCTIONS4_MSG
        self.__instr3_eeg = INSTRUCTIONS3_EEG_COND_MSG
        self.__instr4_eeg = INSTRUCTIONS4_EEG_COND_MSG
        self.__instr9_eeg = INSTRUCTIONS9_EEG_COND_MSG
        self.__finish_eeg = FINISH_EEG_COND_MSG
        self.__instr9 = INSTRUCTIONS9_MSG
        self.__trial_instr_msg1 = TRIAL_INSTRUCTION_MSG1
        self.__continue_for_example = CONTINUE_FOR_EXAMPLE_MSG
        self.scale_instr1 = SCALE_INSTRUCTIONS1
        self.scale_instr2 = SCALE_INSTRUCTIONS2
        self.scale_q = SCALE_QUESTION_MSG
        RatingConnectionTrial.set_gender(self, gender)

    def __load_video_audio_to_list(self, video_file_name, regular_videos, audioless_videos, audio_videos):
        """
        Load the given video/audio file and adds it to the relevant list from the given lists (the video
        will be added to exactly one relevant list.
        In case of MemoryError the video will not be added to any of the lists.
        :param video_file_name: video/audio file name
        :param regular_videos: the list of full videos (audio+video)
        :param audioless_videos: the list of video only files
        :param audio_videos: the list of audio only files
        """
        if C.VIDEO_FILE_EXTENSION in video_file_name.upper():  # each video
            try:
                mov = self.load_video(os.path.join(self.__videos_dir, video_file_name))
                if mov is not None:  # The video is valid
                    if REGULAR_VIDEOS_MARK in video_file_name:
                        regular_videos.append(((mov, trigValStartEx2_full, trigValEndEx2_full), video_file_name))
                    elif AUDIOLESS_VIDEOS_MARK in video_file_name:
                        audioless_videos.append(((mov, trigValStartEx2_videoOnly, trigValEndEx2_videoOnly),
                                                 video_file_name))
            except MemoryError:  # the video couldn't be loaded due to memory error (the file is too big)
                return
        elif C.AUDIO_EXTENSION in video_file_name:
            try:
                mov = self.load_audio(os.path.join(self.__videos_dir, video_file_name))
                if mov is not None:  # The video is valid
                    audio_videos.append(((mov, trigValStartEx2_audioOnly, trigValEndEx2_audioOnly),
                                         video_file_name))
            except MemoryError:  # the video couldn't be loaded due to memory error (the file is too big)
                return

    def prepare_videos(self, files_list=None):
        """
        Prepare the videos for the trial- loads the needed videos
        :param files_list: list of videos files to load. If not specified, take all the files in the videos dir
        :return: list of movie objects, contains all the videos objects for the trial
        """
        check_validity = files_list is None
        if files_list is None:
            # Define videos: all the videos in part b videos dir
            files_list = os.listdir(self.__videos_dir)  # list of all the files' name in the subject directory

        videos_list = []
        regular_videos = []
        audioless_videos = []
        audio_videos = []
        for video_file_name in files_list:
            self.__load_video_audio_to_list(video_file_name, regular_videos, audioless_videos, audio_videos)

        if check_validity and (len(regular_videos) != VIDEOS_NUM or len(audioless_videos) != VIDEOS_NUM or
                               len(audio_videos) != VIDEOS_NUM):
            print "ERROR - missing videos/audios files"
            print "Full_videos: %d, VideoOnly_videos: %d, AudioOnly_videos: %d" % (len(regular_videos),
                                                                                   len(audioless_videos),
                                                                                   len(audio_videos))
            self.close()

        # ## FOR DEBUGGING ## #
#        videos_list, self.videos_name = zip(*(regular_videos + audio_videos + audioless_videos))
#        return videos_list

        random.shuffle(regular_videos)
        random.shuffle(audioless_videos)
        random.shuffle(audio_videos)

        current_options = [regular_videos, audio_videos, audioless_videos]

        if not check_validity:
            # if the videos list was given, then do not choose randomly per list.
            # Only takes the videos and returns them
            for videos in current_options:
                for video, name in videos:
                    videos_list.append(video)
                    self.videos_name.append(name)
            return videos_list

        last_choice = None
        if isEEG:
            # Choose first 3 videos for the EEG condition - without taking off the videos
            # Should load the video again since after loading it changes the object (not sure about that)
            first_choice = self.__choose_eeg_video(current_options)
            second_choice = self.__choose_eeg_video(current_options)
            last_choice = self.__choose_eeg_video(current_options)
            current_options = [first_choice, second_choice]

        for i in range(VIDEOS_NUM):
            # Chooses the order of the videos in which they will be presented:
            # Chooses the type (full, video, audio) of the first one, then the next will be chosen from the two left
            # options and then the last type that were left. In the next round - the first type can't be the last
            # type of the previous round, but after choosing the first type, retrieve the last one from the previous
            # round
            first_choice = self.__choose_video(current_options, videos_list)
            if last_choice is not None:
                current_options.append(last_choice)
            second_choice = self.__choose_video(current_options, videos_list)
            last_choice = self.__choose_video(current_options, videos_list)

            current_options = [first_choice, second_choice]

        # ### for debugging ###
        # video_file_name = './videos/subs/ID51_vid4.mp4'
        # mov = self.load_video(video_file_name)  # Load Conversation Video
        # videos_list = [self.load_video(C.EXPERIMENT2_FOLDER + "practice_video.mp4"),
        #                self.load_video(C.EXPERIMENT2_FOLDER + "practice_video.mp4")]
        # self.videos_name.append("video1")
        # self.videos_name.append("video2")

        # videos_list = []
        # self.videos_name = []
        # files_list = os.listdir("audio_test")
        # for video_file_name in files_list:
        #     mov = self.load_audio(os.path.join("audio_test", video_file_name))
        #     if mov is not None:  # The video is valid
        #         videos_list.append(mov)
        #         self.videos_name.append(video_file_name)

        return videos_list

    def __choose_eeg_video(self, current_options):
        """
        Adds a random video from the given current_options list to the eeg_videos:
        chooses randomly a videos group (list) from the current_options list of list, and then chooses randomly a
        video from that group, loads it into the eeg_videos list and remove the chosen videos group from
        current_list.
        :param current_options: list of videos list.
        :return: the chosen videos group.
        """
        choice = random.choice(current_options)
        chosen_video = random.choice(choice)
        self.videos_name.append(chosen_video[1])  # adds the video name so it will save it correctly
        self.__load_video_audio_to_list(chosen_video[1], self.__eeg_videos, self.__eeg_videos, self.__eeg_videos)
        current_options.remove(choice)
        return choice

    def __choose_video(self, current_options, videos_list):
        """
        Adds a random video from the given current_options list to the given videos_list:
        chooses randomly a videos group (list) from the current_options list of list, and then takes the first
        video from that group, adds it into the given videos_list and finally remove the video from the list and
        the chosen videos group from current_list.
        :param current_options: list of videos list.
        :param videos_list: list that the chosen video should be added to
        :return: the chosen videos group.
        """
        choice = random.choice(current_options)
        videos_list.append(choice[0][0])  # the list chosen list should be shuffled so it is ok to take the first one
        self.videos_name.append(choice.pop(0)[1])  # adds the video name so it will save it correctly
        current_options.remove(choice)
        return choice

    def __eeg_trial(self):
        """
        Shows instructions for the EEG trials
        """
        self.__eeg_cond = True  # for the next section, performs as eeg condition trials
        self.draw_text(self.__instr1, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=200,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=155,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr3_eeg, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=50,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr4_eeg, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=5,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_advance()
        self.draw_text(self.__instr5_eeg, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=220,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr6, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=175,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr7, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=130,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr8, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=75,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr9_eeg, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=-10,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__trial_eeg_instr_msg2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=-105,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__trial_instr_msg4, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=-200,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()
        if self.wait_for_input(['space', 'escape', 'q'])[0] == 'q':
            self.close()

        for i in range(len(self.__eeg_videos)):
            self.play_video(self.__eeg_videos[i][0], None, 1)  # play trial video
            self.videos_name.pop(0)  # removing the video after displaying it

            if i < len(self.__eeg_videos) - 1:
                self.between_videos_instructions(fixation=False)

        self.draw_text(self.__finish_eeg, wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()
        event.waitKeys()

        self.__eeg_cond = False  # done with eeg trials

    def rate_emotions(self, movie_id, save_data):
        """
        Asks the user to rate its emotions at non-eeg condition. At eeg condition- saves the video' name.
        :param movie_id: the current movie id
        :param save_data: boolean parameter to determine whether or not to save the data
        """
        if save_data and self.__eeg_cond:
            self.emotions_file.write((self.videos_name[movie_id - 1] + C.ROW_DELIMITER).encode('UTF-16'))
        else:
            RatingConnectionTrial.rate_emotions(self, movie_id, save_data)

    def show_instructions(self):
        """
        The function shows the trial's first instructions for the begging of the trial.
        Should be implemented in each trial class that
        inheritance from this class with its own instructions
        """
        if isEEG:
            self.__eeg_trial()
        else:
            self.draw_text(self.__instr1, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=200,
                           wrap_width=C.INSTRUCTION_WIDTH)
            self.draw_text(self.__instr2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=155,
                           wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr3, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=50,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr4, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=5,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr4_2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=-40,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_advance()
        self.draw_text(self.__instr5, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=200,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr6, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=155,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr7, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=110,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr8, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=65,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr9, C.WIN_CENTER_ALIGN, y_pos=-250, wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()
        self.wait_for_input(keyList=['space', 'escape'])

    def show_trial_instructions(self):
        """
        The function shows the trial's instructions- instructions for begging the actual trial part.
        Should be implemented in each trial class that
        inheritance from this class with its own instructions
        """
        self.draw_text(self.__trial_instr_msg1, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=250,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__trial_instr_msg2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=205,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__trial_instr_msg3, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=160,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr4_2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=100,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__trial_instr_msg4, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=40,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()
        event.waitKeys(keyList=['space', 'escape'])

    def additional_questions(self):
        """
        shows any additional questions
        """
        self.draw_text(self.__addition_q, wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()

        # gets key in a loop instead of waitKeys() so the program won't continue and collect the keys as next input
        ans = psychopy.event.getKeys()
        while ans not in [NO_KEY, YES_KEY, ['escape']]:
            ans = psychopy.event.getKeys()

        return [YES_NO_VALUES[ans[0]]]

    def save_emotion_data(self, rating, record_time, movie_id=0):
        """
        Saves the data of the user's emotions rating while watching the video
        :param rating: sub's rating
        :param record_time: The time it was recorded
        :param movie_id: a parameter that is relevant for part a of the trial and will be ignored in this part
        """
        # Fixing movie id format
        if movie_id > 9:
            serial_number = self.__sub_id + "-" + str(movie_id)
        else:
            serial_number = self.__sub_id + "-0" + str(movie_id)
        video_file_name = self.videos_name[movie_id - 1]

        output_str = ','.join([self.__sub_id, video_file_name, serial_number, str(rating), str(record_time),
                               self.__version]) + '\n'
        self.output_file.write(output_str)


def main(sub_id=None, gender=None, version=None):
    """
    Runs the trial
    :param sub_id: the subject id, if known
    :param gender: the gender, if known
    :param version: the version of the trial, if known
    """
    # create the trial object and run the trial info dialog
    if sub_id is not None and gender is not None and version in range(1, VERSIONS_NUM + 1):
        trial = RatingTrialPartBTrial(sub_id, gender, version)
    else:
        trial = RatingTrialPartBTrial()

    # runs the experiment
    trial.start_experiment()
    trial.close()


if __name__ == "__main__":
    if len(sys.argv) == 4:
        if sys.argv[3] != C.FEMALE or sys.argv[3] != C.MALE:
            print "WRONG USAGE: No such gender"
            print "Usage: python rating_trial_part_b.py <subject's ID> <subject's gender> <version number>"
            sys.exit()
        else:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 1:
        main()
    else:
        print "Usage: python rating_trial_part_b.py <subject's ID> <subject's gender> <version number>"
        sys.exit()
