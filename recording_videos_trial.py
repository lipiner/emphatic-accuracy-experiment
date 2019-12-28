#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################
# import stuff
from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound, parallel
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
from trial import trigValStartEx1, trigValEndEx1

#########################################

#########################################
# ## CONSTANTS ## #
MAX_STORY_NUMBER = 10
NO_KEY = ['k']
YES_KEY = ['f']

# PATH
FILE_NAME = C.LOG_FILE_NAME
OVERRIDE_SUBJECT_Q = "File name already exists. Do you wish to continue and override it?"  # msg for duplicated sub_id

DATA_FILE_TITLES = ["ParticipantID", "Serial", "MovieID", "MovieName", "MovieStartTime", "MovieEndTime", "timeTaken"]
SERIAL_DELIMITER = '-'

# FEMALE MESSAGES
FIRST_INSTRUCTIONS_F = "בחלק זה של הניסוי, אנו רוצים שתדברי על חוויות עם משקל רגשי משמעותי בחייך."
NUMBER_OF_EVENT_Q_F = "על כמה אירועים תדברי?"
RECORDING_INST_MSG1_F = "בחלק זה של הניסוי נצלם אותך מדברת על חוויות עם משקל רגשי משמעותי בחייך."
RECORDING_INST_MSG3_F = "יש להתחיל לדבר רק כאשר את רואה שהשעון מתחיל לרוץ."
RECORDING_INFO_MSG2_F = "כאשר את מוכנה, יש ללחוץ על מקש הרווח לתחילת הסרטון."
VIDEOS_BREAK_TIME_MSG_F = "אנא המתיני לפני מעבר לסיפור הבא"
SWITCHING_ARABIC_ORDER_MSG_F = "כעת תספרי את הסיפורים בסדר הפוך"

# MALE MESSAGES
FIRST_INSTRUCTIONS_M = "בחלק זה של הניסוי, אנו רוצים שתדבר על חוויות עם משקל רגשי משמעותי בחייך."
NUMBER_OF_EVENT_Q_M = "על כמה אירועים תדבר?"
RECORDING_INST_MSG1_M = "בחלק זה של הניסוי נצלם אותך מדבר על חוויות עם משקל רגשי משמעותי בחייך."
RECORDING_INST_MSG3_M = "יש להתחיל לדבר רק כאשר אתה רואה שהשעון מתחיל לרוץ."
RECORDING_INFO_MSG2_M = "כאשר אתה מוכן, יש ללחוץ על מקש הרווח לתחילת הסרטון."
VIDEOS_BREAK_TIME_MSG_M = "אנא המתין לפני מעבר לסיפור הבא"
SWITCHING_ARABIC_ORDER_MSG_M = "כעת תספר את הסיפורים בסדר הפוך"

# GENERAL MESSAGES
INVALID_INPUT_MSG = "קלט לא תקין, נא לנסות שוב."  # ""I'm sorry but this input is invalid. Let's try again"
EMPTY_INPUT_MSG = "לא הוקלד כלום, נא לנסות שוב."  # "I'm sorry but you didn't typed anything. Let's try again"
INVALID_EVENTS_NUMBER_MSG = "מספר לא תקין, יש לקליד מספר בין 1 ל- %d.\n " \
                            "נא לנסות שוב" % MAX_STORY_NUMBER
EVENT_NAME_Q = "מה הכותרת של סיפור מספר %d"  # "what is the title of story number %d"
REPEAT_ANS = "רשמת: %s"  # "You typed in: %s"
VERIFY_ANS_Q = "האם זה נכון? ]כ[ן ]ל[א"  # "Is that correct? [Y]es / [N]o:"
REPEAT_MSG = "בסדר, אז ננסה שוב."  # ""Ok, Lets try again."
HEBREW_STORY_TITLE_MSG = ")בעברית("
HEBREW_ARABIC_SWITCHING_MSG = "תחילה בעברית ואז בערבית"
ARABIC_HEBREW_SWITCHING_MSG = "תחילה בערבית ואז בעברית"
VERIFY_CAMERA_Q = "האם המצלמה הופעלה כראוי? ]כ[ן ]ל[א"
REPEAT_CAMERA_MSG = "בסדר, אז ננסה שוב. יש להפעיל את המצלמה וללחוץ על כל מקש בו זמנית"

START_RECORDING_MSG = "עכשיו נתחיל לצלם. יש להפעיל את המצלמה וללחוץ על כל מקש בו זמנית"

RECORDING_INST_MSG2 = "כדי להתחיל את ההקלטה של כל סיפור, יש ללחוץ על מקש הרווח."
RECORDING_INST_MSG2a = "אנו ממליצים להישאר בטווח הזמן של 2-3 דקות."
RECORDING_INST_MSG4 = "הסרטון הראשון יהיה תרגול, רק כדי לוודא שהכל מובן."
RECORDING_INST_MSG5 = "בסוף כל סיפור יש ללחוץ על מקש הרווח."
RECORDING_INST_MSG6 = "אם סיימת לקרוא, יש ללחוץ על מקש הרווח."

RECORDING_INFO_MSG1 = "הסרטון הבא הוא סיפור מספר: %d"  # 'The next video is video number: %d'
RECORDING_NEXT_INFO_MSG = "סרטון מספר: %d"  # 'Video Number: %d'
RECORDING_MSG = "*** מקליט ***"  # '*** Recording ***'
RECORDING_END_INFO_MSG = "בסוף הסיפור יש ללחוץ על מקש הרווח."
FINISH_RECORDING_MSG = "סיימת את הסיפור האחרון. תודה. נא לקרוא לנסיין/נסיינית."

STORY_DEMO_TITLE = "אימון"  # 'DEMO'

ARABIC_TITLE_IMG = "arabic.jpg"

#########################################


class RecordingVideosTrial (Trial):
    """
    Part A of the trial - record subjects' stories
    """
    def __init__(self, sub_id=None, gender=None):
        """
        Initialize the trial object
        """
        self.__sub_folder = None  # will be initialized in create_sub_folder method

        if sub_id is not None and gender is not None:
            self.__sub_id = sub_id
            self.set_gender(gender)
        else:
            self.__sub_id = self.initialize_trial()

        # checks if the folder is already exists and start over if so and the user wish for it
        while not self.__create_sub_folder():
            # Folder has not been created. Try again
            self.__sub_id = self.initialize_trial()

        Trial.__init__(self)
        self.__stories_titles = [STORY_DEMO_TITLE]

        if int(self.__sub_id) < 200 or int(self.__sub_id) > 400:
            self.__language = C.HEBREW
        else:
            if int(self.__sub_id) % 2 == 0:
                self.__language = C.AR_HE
            else:
                self.__language = C.HE_AR

    def __create_sub_folder(self):
        """
        Creates a folder for the new subject. If a folder with that subject id is already existed, the user
        can override it and continue or not.
        :return: True if the folder exists at the end of the method (when it was already existed and the user wished
        to continue or the folder was just created). False if the folder is already existed and the user canceled.
        """
        self.__sub_folder = C.EXPERIMENT1_FOLDER + str(self.__sub_id)

        path_validity = Trial.check_path(self.__sub_folder)
        if path_validity:
            os.mkdir(self.__sub_folder)  # creates the folder

        return path_validity

    def create_data_file(self):
        """
        Creates data output file
        :return: The output file object
        """
        output_name = self.__sub_folder + C.FILE_NAME_SEPARATOR + str(self.__sub_id) + FILE_NAME + C.DATA_FILE_EXTENSION
        header = (C.CELLS_DELIMITER.join(DATA_FILE_TITLES) + C.ROW_DELIMITER).encode('UTF-16')
        # Open output file in the relevant folder and write header
        return Trial.create_file(output_name, header)

    def set_gender(self, gender):
        """
        Sets the gender of the screen messages to fit the sub's gender
        :param gender: The gender of the sub
        """
        if gender == C.MALE:
            self.__first_instructions = FIRST_INSTRUCTIONS_M
            self.__number_of_event_q = NUMBER_OF_EVENT_Q_M
            self.__recording_inst_msg1 = RECORDING_INST_MSG1_M
            self.__recording_inst_msg3 = RECORDING_INST_MSG3_M
            self.__recording_info_msg2 = RECORDING_INFO_MSG2_M
            self.__videos_break_time_msg = VIDEOS_BREAK_TIME_MSG_M
            self.__switching_arabic_order_msg = SWITCHING_ARABIC_ORDER_MSG_M
        else:
            self.__first_instructions = FIRST_INSTRUCTIONS_F
            self.__number_of_event_q = NUMBER_OF_EVENT_Q_F
            self.__recording_inst_msg1 = RECORDING_INST_MSG1_F
            self.__recording_inst_msg3 = RECORDING_INST_MSG3_F
            self.__recording_info_msg2 = RECORDING_INFO_MSG2_F
            self.__videos_break_time_msg = VIDEOS_BREAK_TIME_MSG_F
            self.__switching_arabic_order_msg = SWITCHING_ARABIC_ORDER_MSG_F
        self.__invalid_input_msg = INVALID_INPUT_MSG
        self.__empty_input_msg = EMPTY_INPUT_MSG
        self.__invalid_events_number_msg = INVALID_EVENTS_NUMBER_MSG
        self.__event_name_q = EVENT_NAME_Q
        self.__repeat_ans = REPEAT_ANS
        self.__verify_ans_q = VERIFY_ANS_Q
        self.__repeat_msg = REPEAT_MSG
        self.__start_recording_msg = START_RECORDING_MSG
        # self.__start_recording_msg2 = START_RECORDING_MSG2
        self.__recording_inst_msg2 = RECORDING_INST_MSG2
        self.__recording_inst_msg2a = RECORDING_INST_MSG2a
        self.__recording_inst_msg4 = RECORDING_INST_MSG4
        self.__recording_inst_msg5 = RECORDING_INST_MSG5
        self.__recording_info_msg1 = RECORDING_INFO_MSG1
        self.__recording_next_info_msg = RECORDING_NEXT_INFO_MSG
        self.__recording_end_info_msg = RECORDING_END_INFO_MSG
        self.__finish_recording_msg = FINISH_RECORDING_MSG
        Trial.set_gender(self, gender)

    def __ask_user_input(self, question='', num_validity_check=False):
        """
        Asks the user for an input
        :param question: The question to present to the user when taking the input. The default value is an
        empty string
        :param num_validity_check a boolean parameter, when true the input will be checked if it is a
        valid number between 1 to max story number
        :return: The user input as a string
        """
        while True:
            # gets the user input and presents the result
            user_input = self.get_user_input(question)
            self.draw_text(self.__repeat_ans % user_input, y_pos=100, wrap_width=C.INSTRUCTION_WIDTH)
            self.win.flip(False)

            if user_input == C.QUIT_KEY_MARK:
                # User canceled
                self.win.flip()  # clear the screen
                return '0'

            if len(user_input) == 0:
                # empty input - let's try again
                self.draw_text(self.__empty_input_msg, wrap_width=C.INSTRUCTION_WIDTH)
                self.draw_advance()
                continue

            if num_validity_check:
                try:
                    # tries to cast the input to a number
                    user_input = int(user_input)
                except ValueError:
                    # ask again until if the input is invalid (not a valid number)
                    self.draw_text(self.__invalid_input_msg, wrap_width=C.INSTRUCTION_WIDTH)
                    self.draw_advance()
                    continue
                if user_input >= MAX_STORY_NUMBER or user_input < 1:
                    # ask again until if the input is too high or too low
                    self.draw_text(self.__invalid_events_number_msg, wrap_width=C.INSTRUCTION_WIDTH)
                    self.draw_advance()
                    continue

            # verify the input
            self.draw_text(self.__verify_ans_q, wrap_width=C.INSTRUCTION_WIDTH)
            self.win.flip()

            # gets key in a loop instead of waitKeys() so the program won't continue and collect the keys as next input
            ans = psychopy.event.getKeys()
            while ans not in [NO_KEY, YES_KEY, ['escape']]:
                ans = psychopy.event.getKeys()

            if ans == NO_KEY:
                self.draw_text(self.__repeat_msg, wrap_width=C.INSTRUCTION_WIDTH)
                self.draw_advance()
            else:
                return user_input

    def __record_stories(self):
        """
        The recording data part.
        Shows instruction to this part and than for each story presents the story details and start
        timing each video upon press (on space bar).
        The video's info will be saved in the output file.
        """
        # a loop for verifying that the camera turned on correctly
        while True:
            # START RECORDING ##################
            start_time = time.time()  # saves the time of starting the camera

            self.draw_text(VERIFY_CAMERA_Q, wrap_width=C.INSTRUCTION_WIDTH)
            self.win.flip()

            # gets key in a loop instead of waitKeys() so the program won't continue and collect the keys as next input
            ans = psychopy.event.getKeys()
            while ans not in [NO_KEY, YES_KEY, ['escape']]:
                ans = psychopy.event.getKeys()

            if ans != NO_KEY:
                break  # the camera turned on correctly - continue the trial
            # the camera was not turned on correctly - try again
            self.draw_text(REPEAT_CAMERA_MSG, wrap_width=C.INSTRUCTION_WIDTH)
            self.draw_advance()

        # more instruction messages after starting the camera
        self.draw_text(self.__recording_inst_msg1, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=250,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__recording_inst_msg2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=150,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__recording_inst_msg2a, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=115,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__recording_inst_msg3, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=50,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__recording_inst_msg4, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=-50,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_text(self.__recording_inst_msg5, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=-150,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_advance()

        if self.__language == C.AR_HE:
            arabic_first = True
        else:
            arabic_first = False
        if self.__language != C.HEBREW:
            arabic_record_again = True
        else:
            arabic_record_again = False
        i = 0
        # Starting video loop - presents instruction for each video and save the video data to the file
        while i < len(self.__stories_titles):
            if self.__language != C.HEBREW and i == int(len(self.__stories_titles) / 2 + 1) and arabic_record_again:
                # switching explanation screen
                arabic_first = not arabic_first  # switch arabic-hebrew recording order
                self.draw_text(self.__switching_arabic_order_msg, y_pos=150, wrap_width=C.INSTRUCTION_WIDTH)
                if arabic_first:
                    self.draw_text(ARABIC_HEBREW_SWITCHING_MSG, y_pos=100, wrap_width=C.INSTRUCTION_WIDTH)
                else:
                    self.draw_text(HEBREW_ARABIC_SWITCHING_MSG, y_pos=100, wrap_width=C.INSTRUCTION_WIDTH)
                self.draw_advance()

            # video information
            if self.__language != C.HEBREW:
                # arabic trail messages
                if arabic_record_again == arabic_first:
                    m_language = psychopy.visual.ImageStim(self.win, ARABIC_TITLE_IMG, pos=(-350, 250))
                else:
                    m_language = self.draw_text(HEBREW_STORY_TITLE_MSG, x_pos=-350, y_pos=250, height=40)
                m_language.setAutoDraw(True)

            self.draw_text(self.__recording_info_msg1 % i, y_pos=250)
            self.draw_text(self.__stories_titles[i], y_pos=150, wrap_width=C.INSTRUCTION_WIDTH)
            self.draw_text(self.__recording_info_msg2, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X + 40, y_pos=-50,
                           wrap_width=C.INSTRUCTION_WIDTH)
            self.draw_text(self.__recording_end_info_msg, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X + 40, y_pos=-150,
                           wrap_width=C.INSTRUCTION_WIDTH)
            self.win.flip()
            event.waitKeys(keyList=['space', 'escape'])

            # START TIMING THE VIDEO #
            start_story_time = time.time() - start_time  # taking video time
            movie_timer = core.CountdownTimer()  # start timing

            ######################################################################
            # Sending START triggers to MindWare here - BrainLabWorks Ltd.       #
            ######################################################################
            self.sending_mindware_triggers(trigValStartEx1)

            # presenting information during the recording
            m1 = self.draw_text(self.__recording_next_info_msg % i, C.WIN_CENTER_ALIGN, y_pos=250)
            m2 = self.draw_text(self.__stories_titles[i], C.WIN_CENTER_ALIGN, y_pos=150, wrap_width=C.INSTRUCTION_WIDTH)
            m3 = self.draw_text(RECORDING_MSG, C.WIN_CENTER_ALIGN, y_pos=50, height=59)
            timer = self.draw_text(str(-int(movie_timer.getTime())), C.WIN_CENTER_ALIGN, y_pos=-100, height=100)
            m4 = self.draw_text(self.__recording_end_info_msg, C.WIN_CENTER_ALIGN, y_pos=-250,
                                wrap_width=C.INSTRUCTION_WIDTH)
            self.win.flip()
            # sets all the messages to autoDraw so will be screened during the entire story
            m1.setAutoDraw(True)
            m2.setAutoDraw(True)
            m3.setAutoDraw(True)
            m4.setAutoDraw(True)
            timer.setAutoDraw(True)

            # waits to end keys
            wait = event.getKeys()
            while wait not in [['space'], ['escape']]:
                # update the screened countDown
                timer.setText(str(-int(movie_timer.getTime())), log=False)
                self.win.flip()
                wait = event.getKeys()

            # END VIDEO #
            if i != 0 or (i == 0 and not arabic_record_again):
                end_story_time = time.time() - start_time

                ####################################################################
                # Sending END triggers to MindWare here - BrainLabWorks Ltd.       #
                ####################################################################
                self.sending_mindware_triggers(trigValEndEx1)

                # Saves data
                if self.__language != C.HEBREW and i != 0:
                    # saves the video's language
                    if arabic_record_again == arabic_first:
                        self.__save_data(i, self.__stories_titles[i] + " (ערבית)", start_story_time, end_story_time)
                    else:
                        self.__save_data(i, self.__stories_titles[i] + " (עברית)", start_story_time, end_story_time)
                else:
                    # hebrew subjects. Doesn't need to save the language
                    self.__save_data(i, self.__stories_titles[i], start_story_time, end_story_time)

            timer.setAutoDraw(False)
            # clear the messages
            m1.setAutoDraw(False)
            m2.setAutoDraw(False)
            m3.setAutoDraw(False)
            m4.setAutoDraw(False)

            if not arabic_record_again:  # shouldn't record again, increment the counter
                i += 1
            if self.__language != C.HEBREW:
                arabic_record_again = not arabic_record_again  # flips for the next time
                m_language.setAutoDraw(False)
            if i != len(self.__stories_titles) and i != 0:  # i != 0 for arabic that has 2 practice
                # waits for 30 seconds between videos in case this is not the last video
                self.break_time_sleep(self.__videos_break_time_msg)

    def start_experiment(self):
        """
        Main method of the experiment. Runs the whole experiment
        """
        # shows instructions
        self.draw_text(self.__first_instructions, y_pos=100, wrap_width=C.INSTRUCTION_WIDTH)
        self.draw_advance()

        # gets number of stories and check validity
        user_input = self.__ask_user_input(self.__number_of_event_q, True)
        number_of_stories = int(user_input)

        # gets stories' name
        for i in range(number_of_stories):
            title = self.__ask_user_input(self.__event_name_q % (i + 1))
            self.__stories_titles.append(title)

        self.baseline()  # runs the baseline
        # instruction to start recording
        self.draw_text(self.__start_recording_msg, y_pos=150, wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()
        event.waitKeys()

        self.__record_stories()

        # Done recording message
        self.draw_text(self.__finish_recording_msg, C.WIN_RIGHT_ALIGN, x_pos=C.RIGHT_ALIGN_X, y_pos=150,
                       wrap_width=C.INSTRUCTION_WIDTH)
        self.win.flip()
        event.waitKeys(keyList=['space', 'escape'])

    def __save_data(self, movie_id, movie_name, movie_start_time, movie_end_time):
        """
        Saves the current video data into the output file
        :param movie_id: number of the video
        :param movie_name: name of the video
        :param movie_start_time: the current story's beginning time since start recording
        :param movie_end_time: the current story's end time since start recording
        """
        # Fixing movie id format
        if movie_id > 9:
            movie_id = str(movie_id)
        else:
            movie_id = '0' + str(movie_id)

        # Save data
        serial_number = self.__sub_id + SERIAL_DELIMITER + movie_id
        time_taken = movie_end_time - movie_start_time
        movie_name = movie_name.decode('UTF-8')  # decode movie name (in hebrew)
        output_str = C.CELLS_DELIMITER.join([self.__sub_id, serial_number, movie_id, movie_name, str(movie_start_time),
                                             str(movie_end_time), str(time_taken)]) + C.ROW_DELIMITER
        self.output_file.write(output_str.encode('UTF-16'))  # again must encode the hebrew characters


def main(sub_id=None, gender=None):
    """
    Runs the trial
    :param sub_id: the subject id, if known
    :param gender: the gender, if known
    """
    # create the trial object and run the trial info dialog
    if sub_id is not None and gender is not None:
        trial = RecordingVideosTrial(sub_id, gender)
    else:
        trial = RecordingVideosTrial()

    # runs the experiment
    trial.start_experiment()
    trial.close()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        if sys.argv[2] != C.FEMALE or sys.argv[2] != C.MALE:
            print "WRONG USAGE: No such gender"
            print "Usage: python recording_videos_trial.py <subject's ID> <subject's gender>"
            sys.exit()
        else:
            main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1:
        main()
    else:
        print "Usage: python recording_videos_trial.py <subject's ID> <subject's gender>"
        sys.exit()
