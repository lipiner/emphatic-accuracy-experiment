# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
# http://stackoverflow.com/questions/4580576/python-library-for-splitting-video

import sys  # to point to homebrew installed location
from trial import Constants as C

import os
import subprocess  # for running ffmpeg
import time

START_TIME_COL = 4
END_TIME_COL = 5
OUTPUT_FOLDER = '.\\'


def process_video_file(video_filename, logfile, output):
    """
    Split the given video file based on the log file into the output dir
    :param video_filename: the video filename
    :param logfile: the logfile with instructions how to split the video file
    :param output: the output dir for all the split videos
    """
    start_times = []
    end_times = []
    with open(logfile, 'rU') as this_file:  # 'U' is for universal support for '\r' newline chars put in by Matlab
        while len(this_file.readline()) < END_TIME_COL:  # reads the first line (to skip on the headers)
            continue  # the line was invalid (may happen when editing the file manually) so skip another line
        while len(this_file.readline()) < END_TIME_COL:  # reads the first data line (to skip on the DEMO line)
            continue  # the line was invalid (may happen when editing the file manually) so skip another line
        for line in this_file:
            split_line = line.split(C.CELLS_DELIMITER)
            if len(split_line) < START_TIME_COL:
                continue  # ignores any extra lines that do not contain all parameters for any reason
            # The UTF-16 adds extra char every 2 chars, so removing them when reading the times
            start_times.append(split_line[START_TIME_COL][1::2])
            end_times.append(split_line[END_TIME_COL][1::2])
    for idx in xrange(len(start_times)):
        # ffmpeg -i input.mp4 -ss FROMTIME_IN_SECONDS -c copy -to TO_TIME_IN_SECONDS output.mp4
        # -ss before -i is much faster, but less accurate

        # creates the output file to be the original name with an appendix in the output file
        output_file = video_filename[:-4] + C.VIDEO_APPENDIX + str(idx + 1) + C.VIDEO_FILE_EXTENSION
        # takes only the file name into the output folder
        output_file = os.path.join(output, output_file.split(os.path.sep)[-1])
        # for some reason, if I use "-c copy" the video doesn't cut well
        # -y flag for always overwrite existed files
        command = "C:\\ffmpeg\\bin\\ffmpeg.exe -y -i " + video_filename + " -ss " + str(start_times[idx]) + \
                  " -to " + str(end_times[idx]) + " " + output_file
        print "Starting cutting " + video_filename + " from time " + str(start_times[idx]) + " to time " + \
              str(end_times[idx])
        subprocess.call(command, shell=True)

    print "Done process file"


def check_input(video, log):
    """
    Checks the format of the input files (a video and a csv log file)
    :param video: The supposed to be video file
    :param log: The supposed to be csv file
    :return: True iff all the input is valid
    """
    if os.path.splitext(video)[1].upper() != C.VIDEO_FILE_EXTENSION or \
       os.path.splitext(log)[1] != C.DATA_FILE_EXTENSION:
        return False
    return True


def print_usage():
    """
    Print the usage of the script
    """
    print "Usage:"
    print "python split_videos.py <dir_path_with_mp4_and_log_file>"
    print "or:"
    print "python split_videos.py <path_to_video.mp4> <path_to_log.csv>"
    if len(sys.argv) == 1:
        time.sleep(5)  # for running not from the command line - waits before closes the window with the messages
    sys.exit()


def process_dir(path):
    """
    Gets a directory and returns the video file and the log file in the directory
    :param path: The directory
    :return: a tuple: video_file, log_file
    """
    video = None
    log = None
    if not os.path.isdir(path):
        print_usage()
    else:
        files_list = []
        # get a list of all the files' name in the subject directory and in the sub-dirs
        for sub_dir, _, _ in os.walk(path):
            sub_dir_files = os.listdir(sub_dir)
            for sub_file in sub_dir_files:
                files_list.append(os.path.join(sub_dir, sub_file))
        # searches for the video file and the log file
        for my_file in files_list:
            if my_file.upper().endswith(C.VIDEO_FILE_EXTENSION):
                video = my_file
            if C.LOG_FILE_NAME in my_file:
                log = my_file

    if video is None:
        print "No video file in the directory"
        if len(sys.argv) == 1:
            time.sleep(5)  # for running not from the command line - waits before closes the window with the messages
        sys.exit()
    if log is None:
        print "No log file in the directory"
        if len(sys.argv) == 1:
            time.sleep(5)  # for running not from the command line - waits before closes the window with the messages
        sys.exit()

    return video, log


if __name__ == "__main__":
    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
    os.chdir(_thisDir)
    output_dir = OUTPUT_FOLDER

    # defines the video file and the log file
    if len(sys.argv) == 1:
        # Runs without any parameter
        sub_id = raw_input("Enter the subject id: ")
        output_dir = C.EXPERIMENT1_FOLDER + sub_id  # set the output folder to be the given one instead of the default
        video_file, log_file = process_dir(output_dir)
    elif len(sys.argv) == 2:
        # Should be a directory
        video_file, log_file = process_dir(sys.argv[1])
    elif len(sys.argv) == 3:
        # Should be the files to process
        video_file = sys.argv[1]
        log_file = sys.argv[2]
        if not check_input(sys.argv[1], sys.argv[2]):
            print 'Wrong input files format (not a video file or not a correct log file'
            print_usage()
    else:
        print_usage()
        sys.exit()

    print 'You wish to process video filename: ', str(video_file), ' with logfile ', str(log_file), ', correct?'
    is_correct = raw_input("[Y]es / [N]o : ")
    if not (is_correct == "y" or is_correct == "Y"):
        print 'ok, try again'
        sys.exit()

    print 'ok!'
    process_video_file(str(video_file), str(log_file), output_dir)
