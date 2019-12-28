#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#########################################
# import stuff
from __future__ import absolute_import, division
from psychopy import visual, locale_setup, gui, core, data, event, logging, sound, parallel
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
import shutil  # for removing a directory

################################################################
# Related to sending triggers to MindWare - BrainLabWorks Ltd. #
################################################################
# Settings:
LPTAddress = 0x3FE8				# LPT port's address
outDuration = 10				# Output duration (ms.)
trigValStartEx1 = 10			# "Start" trigger value (1-255 or 0x01-0xFF)
trigValEndEx1 = 11				# "End" trigger value (1-255 or 0x01-0xFF)
trigValStartEx2 = 12 			# "Start" trigger value (1-255 or 0x01-0xFF)
trigValEndEx2 = 13				# "End" trigger value (1-255 or 0x01-0xFF)
trigValStartEx2_full = 1
trigValEndEx2_full = 2
trigValStartEx2_videoOnly = 3
trigValEndEx2_videoOnly = 4
trigValStartEx2_audioOnly = 5
trigValEndEx2_audioOnly = 6
trigValStartBaseline = 14
trigValEndBaseline = 15


isMindWareConnected = True
isEEG = False

#####################
# ##  CONSTANTS  ## #
#####################
OVERRIDE_SUBJECT_Q = "File name already exists. Do you wish to continue and override it?"  # msg for duplicated sub_id

# DIALOG INFO TITLES
SUBJECT_TITLE = "Subject ID: "
GENDER_TITLE = "Gender: "
VERSION_TITLE = "Version: "

# SCREEN INFO
# Define screen size
WIN_WIDTH = 1280
WIN_HEIGHT = 1024
# Define screen center
CENTER_X = 0
CENTER_Y = 0

ADVANCE = "יש ללחוץ על כל מקש להמשך"  # "Press any key to continue"
ADVANCE_Y = -250

# FEMALE MESSAGES
BASELINE_MSG1_F = "בשלב זה אנו צריכים שתשבי בצורה רגועה על הכיסא עם שתי כפות הרגליים"
BASELINE_MSG2_F = "על הקרקע וידיים על הברכיים."
BASELINE_MSG3_F = "במסך הבא יופיע + למשך 2 דקות."
BASELINE_MSG4_F = "אנו רוצים שתנסי להיות כמה שיותר רגועה ושקטה."
BASELINE_MSG5_F = "בתום שתי הדקות המסך יתחלף באופן עצמאי ותתבקשי להמתין לנסיין/ית."
BASELINE_END_MSG_F = "תודה, אנא המתיני לנסיין/ית"

# MALE MESSAGES
BASELINE_MSG1_M = "בשלב זה אנו צריכים שתשב בצורה רגועה על הכיסא עם שתי כפות הרגליים"
BASELINE_MSG2_M = "על הקרקע וידיים על הברכיים."
BASELINE_MSG3_M = "במסך הבא יופיע + למשך 2 דקות."
BASELINE_MSG4_M = "אנו רוצים שתנסה להיות כמה שיותר רגוע ושקט."
BASELINE_MSG5_M = "בתום שתי הדקות המסך יתחלף באופן עצמאי ותתבקש להמתין לנסיין/ית."
BASELINE_END_MSG_M = "תודה, אנא המתן לנסיין/ית"

BASELINE_MSG6 = "לאחר שהנסיין/ית יוצא מהחדר, יש ללחוץ על מקש הרווח"

BASELINE_SCREEN = "+"
BASELINE_DURATION = 120


class Constants:
    # PATH
    EXPERIMENT1_FOLDER = '.\\EA1\\'
    EXPERIMENT2_FOLDER = '.\\EA2\\'
    FILE_NAME_SEPARATOR = '\\ID'
    DATA_FILE_EXTENSION = '.csv'
    VIDEO_FILE_EXTENSION = '.MP4'
    VIDEO_APPENDIX = '_vid'
    AUDIO_EXTENSION = '.wav'
    LOG_FILE_NAME = '_MovieLog'
    CELLS_DELIMITER = "\t"
    ROW_DELIMITER = "\r"

    # gender titles
    MALE = "Male"
    FEMALE = "Female"

    # languages titles
    HEBREW = "Hebrew"
    AR_HE = "Arabic-Hebrew"
    HE_AR = "Hebrew-Arabic"

    # OTHER
    VIDEO_X = CENTER_X
    VIDEO_Y = CENTER_Y + 50

    WIN_RIGHT_ALIGN = 'right'
    WIN_LEFT_ALIGN = 'left'
    WIN_CENTER_ALIGN = 'center'

    INSTRUCTION_WIDTH = 1100

    USER_INPUT_X = 150
    RIGHT_ALIGN_X = 450

    VIDEOS_BREAK_DURATION = 30

    QUIT_KEY_MARK = 'ESCAPE'


#########################################


class Trial:
    def __init__(self):
        """
        Initializes the win (window) object and the mouse object
        """
        if isMindWareConnected:
            # Open parallel port and some other stuff for MindWare
            self.p_port = parallel.ParallelPort(LPTAddress)  # Opening parallel port.
            self.p_port.setData(0)  # Setting initial value to 0
            time.sleep(outDuration / 1000)  # Wait for trigger to 'catch on'

        # Creates trial objects
        self.win = psychopy.visual.Window(size=[WIN_WIDTH, WIN_HEIGHT], units="pix", fullscr=True, color=[-1, -1, -1],
                                          monitor='testMonitor', winType='pyglet')
        self.mouse = psychopy.event.Mouse(visible=False, newPos=[0, -200], win=self.win)
        self.output_file = self.create_data_file()

    @staticmethod
    def check_path(path):
        """
        Checks if the path is valid: not exists or the user wishes to override
        :return: True if the folder does not exist or the user has chosen to delete it.
        False if the folder is already exists and the user canceled.
        """
        if os.path.exists(path):
            # alerts the experimenter that the sub_id already exists
            dialog = psychopy.gui.Dlg()
            dialog.addText(OVERRIDE_SUBJECT_Q)
            dialog.show()

            if dialog.OK:
                if os.path.isdir(path):
                    shutil.rmtree(path)  # removes a directory (and all its content)
                else:
                    os.remove(path)  # removes a file
            else:
                return False  # User wish to retry

        return True  # Path is valid

    @staticmethod
    def check_sub_id(sub_id):
        """
        Checks the validity of the given subject id.
        Subject id has to be bigger than 31 so when saving the videos in the excel in the format of
        <SUB_ID>-<VIDEO_NUMBER> it won't be converted to a date format
        :param sub_id: the subject id to be checked
        :return: True if the subject id is valid. False otherwise
        """
        if not sub_id.isdigit() or int(sub_id) < 99:
            # subject id with less than 3 digit will damage the format in the excel
            dialog = psychopy.gui.Dlg()
            dialog.addText("subject id is no valid. Please enter number that is bigger than 100")
            dialog.show()

            if not dialog.OK:
                core.quit()  # User canceled
            return False

        return True

    @staticmethod
    def create_file(path, header):
        """
        Creates a file and opens it for writing with a given header.
        :param path: The path of the new file
        :param header: The first line in the file
        :return: A file object
        """
        new_file = open(path, 'w')
        new_file.write(header)
        return new_file

    def create_data_file(self):
        """
        Creates data output file
        :return: The output file object
        """
        pass

    def draw_text(self, text, align=Constants.WIN_CENTER_ALIGN, x_pos=CENTER_X, y_pos=CENTER_Y, height=30,
                  wrap_width=None, to_draw=True, bold=False, italic=False):
        """
        Draws a text to the screen using psychopy.visual.TextStim function.
        Sets some default parameters regarding to this program:
          # The global window variable of the program
          # color=[1, 1, 1] (the default parameters of the TextStim function)
        After calling this function to draw all the wanted texts of the next screen, the command: win.flip()
        should be called
        :param align: The align of the text (regarding to the x+y pos), should be one of the relevant constants.
        :param text: The text to draw to the screen
        :param x_pos: The x position of the text on the screen. The default value is 0 (in the center)
        :param y_pos: The y position of the text on the screen. The default value is 0 (in the center)
        :param height: The height of the text- sets the size of the text. The function resets the default height
        to 30 (instead of None as in the TextStim function)
        :param wrap_width: The width of the texts (length of the line). The default parameter is the same as the
        TextStim function default value (None)
        :param to_draw: set to False for not drawing the text after creating the object. The default value is to True
        (to draw)
        :param bold: default=False
        :param italic: default=False
        :return the TextStim object if necessary
        """
        text = text.decode('UTF-8')[::-1]
        text_stim = psychopy.visual.TextStim(win=self.win, alignHoriz=align, text=text, height=height,
                                             pos=[x_pos, y_pos], wrapWidth=wrap_width, bold=bold, italic=italic)
        if to_draw:
            text_stim.draw()
        return text_stim

    def draw_advance(self):
        """
        Draws advance message - the message with the information how to continue in the trial to the next screen.
        The function draws the text and execute it- meaning it calls win.flip() to draw everything in the buffer.
        Then it waits for a key.
        """
        self.draw_text(ADVANCE, y_pos=ADVANCE_Y, wrap_width=Constants.INSTRUCTION_WIDTH)
        self.win.flip()
        self.wait_for_input()

    def load_video(self, video_file):
        """
        Load a video using the trial default parameters
        :param video_file: path of the movie
        :return: the movie object
        """
        if not os.path.exists(video_file):
            # video file is not exists. Exit with a message
            print "Wrong parameters - video file is not found"
            print "missing file - " + video_file
            return None
        try:  # may crash in case the video file is broken
            mov = visual.MovieStim3(self.win, video_file, size=(640, 360), flipVert=False, flipHoriz=False,
                                    pos=[Constants.VIDEO_X, Constants.VIDEO_Y], loop=False)
        except KeyError:
            return None
        return mov

    @staticmethod
    def load_audio(audio_file):
        """
        Load an audio using the trial default parameters
        :param audio_file: path of the audio
        :return: the audio object
        """
        if not os.path.exists(audio_file):
            # video file is not exists. Exit with a message
            print "Wrong parameters - audio file is not found"
            print "missing file - " + audio_file
            return None
        try:  # may crash in case the video file is broken
            aud = sound.Sound(audio_file, sampleRate=48000)
        except KeyError:
            return None
        return aud

    @staticmethod
    def wait_for_input(keyList=None):
        """
        :param keyList: list of keys to wait for (escape, space, letters, etc.)
        """
        return psychopy.event.waitKeys(keyList=keyList)

    def initialize_trial(self, versions=0):
        """
        Initialize the trial basic parameters using a dialog box.
        Set the subject-id, the version (if exists) and the gender of the subject to choose the screen messages
        :param versions a boolean parameter to set if the trial's version needs to be set in the dialog options.
        Default value is False
        :return: the sub-id and the partner-id (if exists)
        """
        # Ensure that relative paths start from the same directory as this script
        _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
        os.chdir(_thisDir)

        while True:
            # input subject and partner ID; store values for later
            dialog = psychopy.gui.Dlg()
            dialog.addField(SUBJECT_TITLE)
            dialog.addField(GENDER_TITLE, choices=[Constants.MALE, Constants.FEMALE])
            if versions:
                dialog.addField(VERSION_TITLE, choices=range(1, versions + 1))
            dialog.show()

            if not dialog.OK:
                core.quit()  # User canceled

            sub_id = dialog.data[0]
            self.set_gender(dialog.data[1])

            if Trial.check_sub_id(sub_id):
                # the sub_id is valid so continue on and exit the loop
                break

        if versions:
            versions = dialog.data[2]
            return sub_id, versions  # returns the sub_id as well as the version

        return sub_id

    def set_gender(self, gender):
        """
        Sets the gender of the screen messages to fit the sub's gender
        :param gender: The gender of the sub
        """
        if gender == Constants.MALE:
            self.__baseline_msg1 = BASELINE_MSG1_M
            self.__baseline_msg2 = BASELINE_MSG2_M
            self.__baseline_msg3 = BASELINE_MSG3_M
            self.__baseline_msg4 = BASELINE_MSG4_M
            self.__baseline_msg5 = BASELINE_MSG5_M
            self.__baseline_end_msg = BASELINE_END_MSG_M
        else:
            self.__baseline_msg1 = BASELINE_MSG1_F
            self.__baseline_msg2 = BASELINE_MSG2_F
            self.__baseline_msg3 = BASELINE_MSG3_F
            self.__baseline_msg4 = BASELINE_MSG4_F
            self.__baseline_msg5 = BASELINE_MSG5_F
            self.__baseline_end_msg = BASELINE_END_MSG_F
        self.__baseline_msg6 = BASELINE_MSG6

    def get_user_input(self, text_message=''):
        """
        Gets an input from the user. Screen the given question and than gets the input in hebrew and screen each note
        :param text_message: The question to the user to get the input. The default value is an empty string
        :return: The user input as a string. If the user canceled using the ESCAPE key, an "ESCAPE" string
        will be return
        """
        message = self.draw_text(text_message, y_pos=100,
                                 wrap_width=Constants.INSTRUCTION_WIDTH)
        message.setAutoDraw(True)  # keeps the question on the screen for the entire time
        if text_message != '':  # flips only when the message is not empty
            self.win.flip()

        user_input = ''
        event.getKeys()  # clears the previous keys if existed
        keys = event.getKeys()
        while 'return' not in keys:
            if len(keys) > 0:  # at least one key was pressed
                if keys[0] == 'escape':
                    message.setAutoDraw(False)
                    return Constants.QUIT_KEY_MARK
                # elif keys[0] == 'space':
                #     user_input += ' '  # storing the key as ' '
                elif keys[0] == 'backspace':  # removes last key
                    # must be decoded before removing for the Hebrew unicode and then encoded back
                    user_input = user_input.decode('UTF-8')[:-1].encode('UTF-8')
                elif keys[0][:-1] == 'num_':  # for the num-keys
                    user_input += keys[0][-1]  # storing the number itself
                # elif len(keys[0]) > 1:
                #     keys = event.getKeys()
                #     continue
                else:
                    key = Trial.__keyboard_trans(keys[0])
                    if len(key.decode('UTF-8')) > 1:  # must be decoded so the Hebrew note will be decoded as 1 note
                        keys = event.getKeys()  # not a printable note (a key-name instead of note)
                        continue
                    user_input += key  # Adds the key (1 note)
                self.draw_text(user_input, x_pos=Constants.USER_INPUT_X)
                self.win.flip()
            keys = event.getKeys()

        message.setAutoDraw(False)  # removes the question
        return user_input

    def baseline(self):
        """
        Shows instructions and sending baseline triggers
        """
        # shows instructions
        self.draw_text(self.__baseline_msg1, y_pos=250, wrap_width=Constants.INSTRUCTION_WIDTH)
        self.draw_text(self.__baseline_msg2, y_pos=150, wrap_width=Constants.INSTRUCTION_WIDTH)
        self.draw_text(self.__baseline_msg3, y_pos=50, wrap_width=Constants.INSTRUCTION_WIDTH)
        self.draw_text(self.__baseline_msg4, y_pos=-50, wrap_width=Constants.INSTRUCTION_WIDTH)
        self.draw_text(self.__baseline_msg5, y_pos=-150, wrap_width=Constants.INSTRUCTION_WIDTH)
        self.draw_text(self.__baseline_msg6, y_pos=-250, wrap_width=Constants.INSTRUCTION_WIDTH)
        self.win.flip()
        psychopy.event.waitKeys()

        # shows the baseline message
        self.draw_text(BASELINE_SCREEN, height=100)
        self.win.flip()
        start_baseline_time = time.time()
        curr_time = time.time()
        self.sending_mindware_triggers(trigValStartBaseline)  # sending triggers
        while curr_time - start_baseline_time <= BASELINE_DURATION and not event.getKeys(['escape']):
            # waits for 2 minutes
            curr_time = time.time()
        self.sending_mindware_triggers(trigValEndBaseline)  # sending end triggers

        # shows end message
        self.draw_text(self.__baseline_end_msg, wrap_width=Constants.INSTRUCTION_WIDTH)
        self.win.flip()
        event.waitKeys()

    def break_time_sleep(self, message, message2=None):
        """
        Sleeps for 30 seconds for break time
        :param message: The instructions before the sleeping
        :param message2: Additional instructions before the sleeping
        """
        self.draw_text(message, wrap_width=Constants.INSTRUCTION_WIDTH)
        if message2:
            self.draw_text(message2, y_pos=-60, wrap_width=Constants.INSTRUCTION_WIDTH)
        self.win.flip()
        start_time = time.time()
        curr_time = time.time()
        while curr_time - start_time <= Constants.VIDEOS_BREAK_DURATION and not event.getKeys(['escape']):
            curr_time = time.time()

    @staticmethod
    def __keyboard_trans(key):
        """
        Convert each input in an English keyboard into the correct key in the Hebrew keyboard
        :param key: The input from the English keyboard
        :return: The concurrent key in the Hebrew keyboard
        """
        hebrew_dict = {'q': '/', 'w': '\'', 'e': 'ק', 'r': 'ר', 't': 'א', 'y': 'ט', 'u': 'ו', 'i': 'ן', 'o': 'ם',
                       'p': 'פ', 'a': 'ש', 's': 'ד', 'd': 'ג', 'f': 'כ', 'g': 'ע', 'h': 'י', 'j': 'ח', 'k': 'ל',
                       'l': 'ך', 'semicolon': 'ף', 'apostrophe': ',', 'z': 'ז', 'x': 'ס', 'c': 'ב', 'v': 'ה', 'b': 'נ',
                       'n': 'מ', 'm': 'צ', 'comma': 'ת', 'period': 'ץ', 'slash': '.', 'space': ' '}
        if key not in hebrew_dict:
            return key  # key not in the dictionary - keeps the original key
        else:
            return hebrew_dict[key]

    def sending_mindware_triggers(self, trigger):
        """
        Sending triggers to a parallel port
        :param trigger: the trigger's value
        """
        if isMindWareConnected:
            # Open parallel port and some other stuff
            self.p_port.setData(trigger)  # Send trigger (START / END)
            time.sleep(outDuration / 1000)  # Wait for trigger to 'catch on'
            self.p_port.setData(0)  # Reset port to 0
            time.sleep(outDuration / 1000)  # Wait for trigger to 'catch on'

    def start_experiment(self):
        """
        Main method of the experiment. Runs the whole experiment
        """
        pass

    def close(self):
        """
        Ends the experiment. Should be called at the end to close any open steam
        """
        self.output_file.close()
        self.win.close()
        time.sleep(5)
        core.quit()
