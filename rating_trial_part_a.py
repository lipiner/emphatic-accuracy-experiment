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
from rating_connection_trial import RatingConnectionTrial
from rating_connection_trial import DATA_FILE_NAME, EMOTION_FILE_NAME, EMOTIONS_LIST
from trial import trigValStartEx2, trigValEndEx2

#########################################

#########################################
# ## CONSTANTS ## #
# PATH
DATA_FILE_TITLES = 'SubID,MovieID,Serial,Rating,Time\n'

WRONG_SUB_ID_MSG = "subject id is not existed. Please try again"

# FEMALE MESSAGES
INSTRUCTIONS1_MSG_F = "כעת, את תצפי בסרטונים שצילמנו. תוך כדי צפייה, חשבי מה היו תחושותייך בכל"
INSTRUCTIONS2_MSG_F = "רגע נתון, כשסיפרת את הסיפור"
INSTRUCTIONS3_MSG_F = "המשימה שלך היא לדווח על כיוון ועוצמת הרגש שלך בכל זמן נתון בזמן שסיפרת"
INSTRUCTIONS4_MSG_F = "את הסיפור. את תעשי זאת על ידי הזזת העכבר."
TRIAL_INSTRUCTION_MSG1_F = "עכשיו שאת מרגישה בנוח עם הזזת הסמן של סולם המדידה, זה הזמן להתחיל"
TRIAL_INSTRUCTION_MSG2_F = "את חלק זה של הניסוי. זכרי להזיז את הסמן כדי לדווח על העוצמה ועל כיוון הרגש"
TRIAL_INSTRUCTION_MSG3_F = "שלך בכל רגע נתון בזמן שסיפרת את הסיפור. הסרטון יחל מיד לאחר מסך זה."
# MALE MESSAGES
INSTRUCTIONS1_MSG_M = "כעת, אתה תצפה בסרטונים שצילמנו. תוך כדי צפייה, חשוב מה היו תחושותיך בכל"
INSTRUCTIONS2_MSG_M = "רגע נתון, כשסיפרת את הסיפור"
INSTRUCTIONS3_MSG_M = "המשימה שלך היא לדווח על כיוון ועוצמת הרגש שלך בכל זמן נתון בזמן שסיפרת"
INSTRUCTIONS4_MSG_M = "את הסיפור. אתה תעשה זאת על ידי הזזת העכבר."
TRIAL_INSTRUCTION_MSG1_M = "עכשיו שאתה מרגיש בנוח עם הזזת הסמן של סולם המדידה, זה הזמן להתחיל"
TRIAL_INSTRUCTION_MSG2_M = "את חלק זה של הניסוי. זכור להזיז את הסמן כדי לדווח על העוצמה ועל כיוון הרגש"
TRIAL_INSTRUCTION_MSG3_M = "שלך בכל רגע נתון בזמן שסיפרת את הסיפור. הסרטון יחל מיד לאחר מסך זה."
# GENERAL MESSAGES
CONTINUE_FOR_EXAMPLE_MSG = "לקבלת דוגמה יש ללחוץ על כל מקש"  # "Press any key to continue"
SCALE_INSTRUCTIONS1 = "מה הייתה העוצמה והכיוון של הרגש שלך"
SCALE_INSTRUCTIONS2 = "בכל רגע נתון, כשסיפרת את הסיפור?"
SCALE_QUESTION_MSG = "כשסיפרת את הסיפור, עד כמה הרגשת "

#########################################


class RatingTrialPartATrial (RatingConnectionTrial):
    """
    Part A of the rating videos' emotion part of the trial - subjects rate their own videos
    """
    def __init__(self, sub_id=None, gender=None):
        """
        Initialize the trial object
        :param sub_id: the subject id, if known
        :param gender: the gender, if known
        """
        # will be initialized in __check_trial_validity method
        self.__sub_folder = None
        self.__output_file_name = None

        if sub_id is not None and gender is not None:
            self.__sub_id = sub_id
            self.set_gender(gender)
        else:
            self.__sub_id = self.initialize_trial()

        # checks if the subject_id is existed and valid
        while not self.__check_trial_validity():
            self.__sub_id = self.initialize_trial()
        RatingConnectionTrial.__init__(self, C.EXPERIMENT1_FOLDER)

    def __check_trial_validity(self):
        """
        Checks the validity of the experiment's parameters: the sub_id is existed and hasn't done this part
        of the trial
        :return: True iff the trial is valid and can continue. False if the trials parameters needs to be load again
        """
        self.__sub_folder = C.EXPERIMENT1_FOLDER + str(self.__sub_id)
        if not os.path.exists(self.__sub_folder):
            # subject is not exists
            dialog = psychopy.gui.Dlg()
            dialog.addText(WRONG_SUB_ID_MSG)
            dialog.show()

            if not dialog.OK:
                core.quit()  # User canceled

            return False

        # Open output file and write header
        self.__output_file_name = self.__sub_folder + C.FILE_NAME_SEPARATOR + str(self.__sub_id) + DATA_FILE_NAME + \
            C.DATA_FILE_EXTENSION
        return Trial.check_path(self.__output_file_name)

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
        titles = "MovieID" + C.CELLS_DELIMITER + C.CELLS_DELIMITER.join(EMOTIONS_LIST).decode('UTF-8') + C.ROW_DELIMITER
        return Trial.create_file(file_name, titles.encode('UTF-16'))

    def set_gender(self, gender):
        """
        Sets the gender of the screen messages to fit the sub's gender
        :param gender: The gender of the sub
        """
        if gender == C.MALE:
            self.__instr1 = INSTRUCTIONS1_MSG_M
            self.__instr2 = INSTRUCTIONS2_MSG_M
            self.__instr3 = INSTRUCTIONS3_MSG_M
            self.__instr4 = INSTRUCTIONS4_MSG_M
            self.__trial_instr_msg1 = TRIAL_INSTRUCTION_MSG1_M
            self.__trial_instr_msg2 = TRIAL_INSTRUCTION_MSG2_M
            self.__trial_instr_msg3 = TRIAL_INSTRUCTION_MSG3_M
        else:
            self.__instr1 = INSTRUCTIONS1_MSG_F
            self.__instr2 = INSTRUCTIONS2_MSG_F
            self.__instr3 = INSTRUCTIONS3_MSG_F
            self.__instr4 = INSTRUCTIONS4_MSG_F
            self.__trial_instr_msg1 = TRIAL_INSTRUCTION_MSG1_F
            self.__trial_instr_msg2 = TRIAL_INSTRUCTION_MSG2_F
            self.__trial_instr_msg3 = TRIAL_INSTRUCTION_MSG3_F
        self.__continue_for_example = CONTINUE_FOR_EXAMPLE_MSG
        self.scale_instr1 = SCALE_INSTRUCTIONS1
        self.scale_instr2 = SCALE_INSTRUCTIONS2
        self.scale_q = SCALE_QUESTION_MSG
        RatingConnectionTrial.set_gender(self, gender)

    def prepare_videos(self, files_list=None):
        """
        Prepare the videos for the trial- loads the needed videos
        :param files_list: list of videos files to load. If not specified, take all the files in the videos dir
        :return: list of movie objects, contains all the videos objects for the trial
        """
        if files_list is None:
            # Define videos: Videos are named / loaded based on subID
            files_list = os.listdir(self.__sub_folder)  # list of all the files' name in the subject directory

        videos_list = []
        additional_videos = []
        for video_file_name in files_list:
            if C.VIDEO_APPENDIX in video_file_name:  # each video
                try:
                    mov = self.load_video(os.path.join(self.__sub_folder, video_file_name))
                    if mov is not None:  # The video is valid
                        videos_list.append((mov, trigValStartEx2, trigValEndEx2))
                        self.videos_name.append(video_file_name)
                except MemoryError:  # the video couldn't be loaded due to memory error (the file is too big)
                    additional_videos.append(os.path.join(self.__sub_folder, video_file_name))

        self.videos_name += additional_videos  # adds videos that couldn't be loaded if there are any

        # ### for debugging ###
        # video_file_name = './videos/subs/ID51_vid4.mp4'
        # mov = self.load_video(video_file_name)  # Load Conversation Video
        # videos_list = [mov]

        return videos_list

    def show_instructions(self):
        """
        The function shows the trial's first instructions for the begging of the trial.
        Should be implemented in each trial class that
        inheritance from this class with its own instructions
        """
        self.draw_text(self.__instr1, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=250,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=215,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr3, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=100,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__instr4, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=65,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__continue_for_example, C.WIN_CENTER_ALIGN, y_pos=-250, wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()
        self.wait_for_input()

    def show_trial_instructions(self):
        """
        The function shows the trial's instructions- instructions for begging the actual trial part.
        Should be implemented in each trial class that
        inheritance from this class with its own instructions
        """
        self.draw_text(self.__trial_instr_msg1, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=250,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__trial_instr_msg2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=215,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__trial_instr_msg3, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=180,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_advance()

    def save_emotion_data(self, rating, record_time, movie_id):
        """
        Saves the data of the user's emotions rating while watching the video
        :param rating: sub's rating
        :param record_time: The time it was recorded
        :param movie_id: The movie id that is being recorded
        """
        # Fixing movie id format
        if movie_id > 9:
            serial_number = self.__sub_id + "-" + str(movie_id)
        else:
            serial_number = self.__sub_id + "-0" + str(movie_id)
        video_file_name = self.videos_name[movie_id - 1]

        output_str = ','.join([self.__sub_id, video_file_name, serial_number, str(rating), str(record_time)]) + '\n'
        self.output_file.write(output_str)


def main(sub_id=None, gender=None):
    """
    Runs the trial
    :param sub_id: the subject id, if known
    :param gender: the gender, if known
    """
    # create the trial object and run the trial info dialog
    if sub_id is not None and gender is not None:
        trial = RatingTrialPartATrial(sub_id, gender)
    else:
        trial = RatingTrialPartATrial()

    # runs the experiment
    trial.start_experiment()
    trial.close()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        if sys.argv[2] != C.FEMALE or sys.argv[2] != C.MALE:
            print "WRONG USAGE: No such gender"
            print "Usage: python rating_trial_part_a.py <subject's ID> <subject's gender>"
            sys.exit()
        else:
            main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1:
        main()
    else:
        print "Usage: python rating_trial_part_a.py <subject's ID> <subject's gender>"
        sys.exit()
