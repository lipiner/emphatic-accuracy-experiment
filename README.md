# emphatic-accuracy-experiment
Python files for an emphatic accuracy experiment. The experiment consists of 2 parts: in the first one, the subject is recording her stories, and in the second she rates her emotions during the recording

# requirements
- Psychopy

# How to run?
1. Create EA1 folder in the same repository. The folder must consist an example video file with name: "practice_video.mp4"
2. Run: recording_videos_trial.py
    First part will be executed.
    You should follow the instructions and start recording in the exact time you press the spacebar key when the instructions instruct to do so.
2. Put the video in the same dir as the subject auto-created dir (EA1/<subject_id>).
3. Run: split_videos.py
    The video will be split to short stories
4. Run: rating_trial_part_a.py
    Second part will be executed.
    
