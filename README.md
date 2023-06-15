# Recording 

This repository has been made to allow the recording of two different webcams and a Kinect camera simultaneously.

# Requirements
To install requirements simply run the following command in the main folder

```
pip install -r requirements.txt
```

# How to use
Your Kinect Studio application must already be running. <br> 
If your desired outputs directory is _path/to/outputs_ then you must specify it by replacing the **output_dir** variable in _capture.py_ and create three folders : 
* path/to/outputs/Camera1
* path/to/outputs/Camera2
* path/to/outputs/Kinect

Then, set your Kinect Studio's output directory as _path/to/outputs/Kinect_ in the application.

You can then run the command 

```
python capture.py
```

When clicking on the 'Start Recording' button the script also clicks at the **(kinect_x, kinect_y)** coordinates which should point to the Kinect Studio's recording button, you may have to change these variables to fit your configuration.

When clicking on the 'Stop Recording' button one file per webcam is created in its corresponding directory. 
This file has the form 'u$USER_$EX_t$TARGET_$CAM.mp4' where $USER is the user ID specified in the GUI, $EX the selected exercise and difficulty level, $TARGET the specified target and $CAM the webcam used to record it.

However, when the recording is over in Kinect Studio, the created file is automaticaly named after its beginning timestamp like as 'YYYYMMDD_hhmmss_00.xef'. Since it cannot be immediately renamed after recording as it is still opened in Kinect Studio, a line is written in _rename_files.txt_ with this file's name and how it should be renamed. After closing Kinect Studio, you can then run 
```
python rename_kinect_records.py
```
which will rename every kinect files to the form 'u$USER_$EX_t$TARGET_kinect.xef'