# Emphatic Accuracy Experiment
Python files for an emphatic accuracy experiment. The experiment consists of 2 parts: in the first one, the subject (target) records stories and rates her emotions during the recording. In the second part other subjects watch videos and rate their emotions

# Requirements
- Psychopy

# How to run?
## First part
Consists of several steps
1. Create EA1 folder in the same repository. The folder must consist an example video file with name: "practice_video.mp4"
2. Run: recording_videos_trial.py
    Recording step will be executed.
    You should follow the instructions and start recording in the exact time you press the spacebar key when the instructions instruct to do so.
2. Put the video in the same dir as the subject auto-created dir (EA1/<subject_id>).
3. Run: split_videos.py
    The video will be split to short stories
4. Run: rating_trial_part_a.py
    The subject will watch her own stories and rate her feelings.

## Second part
1. Create EA2 folder in the same repository. The folder must consist an example video file with name: "practice_video.mp4"
2. Create 3 folders in the same repository: "part_b_videos1", "part_b_videos2", "part_b_videos3", and put there the videos for the experiment.
2. Run: rating_trial_part_b.py
