import os
import cv2
import PySimpleGUI as sg
import pyautogui

# get latest file's name in kinect outputs directory
def find_file_name(directory):
    max = 0
    max_name = ''
    for filename in os.listdir(directory):
        try:
            filetime = int(filename[:-4].replace('_', ''))
        except:
            pass
        if filetime > max:
            max = filetime
            max_name = filename
    return max_name


if __name__ == "__main__":
    # output directory
    output_dir = 'D:/Recordings'

    # Kinect Studio's recording button position
    kinect_x = 180 
    kinect_y = 140

    # define a video capture object
    cam1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # frame per second
    fps = 30 # 30 MAX
    cam1.set(cv2.CAP_PROP_FPS, fps)
    cam2.set(cv2.CAP_PROP_FPS, fps)

    # increasing width/height may decrease fps
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    width = int(cam1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam1.get(cv2.CAP_PROP_FRAME_HEIGHT))

    exercises = {
        'Cache Tête': 'SECT',
        'Arc Arrière': 'SEAA',
        'Étirement latéral assis': 'SLFA',
        'Étirement latéral debout': 'SLFD',
        'Étirement rotation assis': 'SR',
        'Équilibre assis': 'QA',
        'Équilibre assis rotations': 'QR',
        'Équilibre assis pivot': 'QP',
        'Équilibre assis mouvements latéraux': 'QML',
        'Équilibre assis pied levé': 'QPL',
        'Équilibre assis pied levé rotations': 'QPLR'
    }

    # GUI
    layout = [
        [sg.Text('Exercice :')],
        [sg.Combo(list(exercises.keys()), default_value='Cache Tête', key='exercise')],
        [sg.Text('Niveau de difficulté :')],
        [sg.Combo(['Niveau 1', 'Niveau 2', 'Niveau 3'], default_value='Niveau 1', key='level')],
        [sg.Text('User ID :'), sg.Input(key='user')],
        [sg.Text('Target :'), sg.Input(key='target')],
        [sg.Button('Start Recording', key='record', size=(15, 1))]
    ]

    window = sg.Window('Recording App', layout)
    
    is_recording = False
    while True:
        event, values = window.read(timeout=0)

        if event == sg.WINDOW_CLOSED:
            break
        
        if event == 'record':
            # Start recording
            if not is_recording:
                pyautogui.click(kinect_x, kinect_y) # Click on Kinect Studio's record button
                filename =  'u' + values['user'] + '_' + exercises[values['exercise']] + values['level'][-1] + '_t' + values['target']
                writer1 = cv2.VideoWriter(output_dir + '/Camera1/' + filename + '_cam1.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
                writer2 = cv2.VideoWriter(output_dir + '/Camera2/' + filename + '_cam2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
                window['record'].update(text='Stop Recording')
            # Stop recording
            else:
                pyautogui.click(kinect_x, kinect_y) # Click on Kinect Studio's record button
                writer1.release()
                writer2.release()

                # append desired filename to a txt
                kinect_file = find_file_name(output_dir + '/Kinect')
                with open('./rename_files.txt', 'a') as f:
                    f.write(output_dir + '/Kinect/' + kinect_file +','+ output_dir + '/Kinect/' + filename + '_kinect.xef\n')

                window['record'].update(text='Start Recording')
                
            is_recording = not is_recording
        

        ret1, frame1 = cam1.read()
        ret2, frame2 = cam2.read()

        if ret1 and ret2:
            # Display the resulting frame
            cv2.imshow('Camera 1', frame1)
            cv2.imshow('Camera 2', frame2)
            if is_recording:
                writer1.write(frame1)
                writer2.write(frame2)

            
    window.close()

    # After the loop release the cap object
    cam1.release()
    cam2.release()

    # Destroy all the windows
    cv2.destroyAllWindows()
