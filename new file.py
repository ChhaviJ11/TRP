import cv2
import time
import numpy as np


#xml cascade file
sony_logo_cascade = cv2.CascadeClassifier('E:\\TRP Code\\sony_cascade.xml')
star_logo_cascade = cv2.CascadeClassifier('E:\\TRP Code\\star_cascade.xml')
mtv_logo_cascade = cv2.CascadeClassifier('E:\\TRP Code\\mtv_cascade.xml')
zee_logo_cascade = cv2.CascadeClassifier('E:\\TRP Code\\zee_cascade.xml')
blank_screen_cascade = cv2.CascadeClassifier('E:\\TRP Code\\blank_screen_cascade.xml')


# To capture video from existing video.
cap = cv2.VideoCapture('E:\\TRP Code\\new ad.mp4')

detect_types = {
    'star_logo': 'star_logo',
    'sony_logo': 'sony_logo',
    'mtv_logo': 'mtv_logo',
    'zee_logo': 'zee_logo',
    'black_screen': 'black_screen',
    'ad_screen': 'ad_screen',
}
cascade_captured_dict = {
    detect_types['star_logo']: False,
    detect_types['sony_logo']: False,
    detect_types['mtv_logo']: False,
    detect_types['zee_logo']: False,
    detect_types['black_screen']: False,
    detect_types['ad_screen']: False
}
intervals_dict = {
    detect_types['star_logo']: [],
    detect_types['sony_logo']: [],
    detect_types['mtv_logo']: [],
    detect_types['zee_logo']: [],
    detect_types['black_screen']: [],
    detect_types['ad_screen']: []
}
calculated_times_dict = {
    detect_types['star_logo']: [],
    detect_types['sony_logo']: [],
    detect_types['mtv_logo']: [],
    detect_types['zee_logo']: [],
    detect_types['black_screen']: [],
    detect_types['ad_screen']: []
}
capture_time_dict = {
    detect_types['star_logo']: 0,
    detect_types['sony_logo']: 0,
    detect_types['mtv_logo']: 0,
    detect_types['zee_logo']: 0,
    detect_types['black_screen']: 0,
    detect_types['ad_screen']: 0
}
times_dict = {
    detect_types['star_logo']: {},
    detect_types['sony_logo']: {},
    detect_types['mtv_logo']: {},
    detect_types['zee_logo']: {},
    detect_types['black_screen']: {},
    detect_types['ad_screen']: {}
}
timestamp_dict = {
    # detect_types['star_logo']: {'start': 0, 'end': 0},
    # detect_types['sony_logo']: {'start': 0, 'end': 0},
    # detect_types['mtv_logo']: {'start': 0, 'end': 0},
    # detect_types['zee_logo']: {'start': 0, 'end': 0},
    # detect_types['black_screen']: {'start': 0, 'end': 0},
    # detect_types['ad_screen']: {'start': 0, 'end': 0},
    'common': {'start': 0, 'end': 0},
}

def resetVars():
    global cascade_captured_dict
    global intervals_dict
    global times_dict
    global capture_time_dict
    global calculated_times_dict

    cascade_captured_dict = {
        detect_types['star_logo']: False,
        detect_types['sony_logo']: False,
        detect_types['mtv_logo']: False,
        detect_types['zee_logo']: False,
        detect_types['black_screen']: False
    }

def calculateTimeDuration(start_epoch_time, end_epoch_time):
    start_sec = int(start_epoch_time / 1000000000)
    epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    start_time = epoch_start_time

    end_sec = int(end_epoch_time / 1000000000)
    epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(end_sec))
    end_time = epoch_end_time

    time_detect = end_epoch_time - start_epoch_time
    return [time_detect, start_time, end_time,start_sec,end_sec]

def detectCascade(type, img, gray):

    if type == 'star_logo' and star_logo_cascade:
        roi_gray = gray[29:29 + 156, 1075:1075 + 156]
        roi_color = img[29:29 + 156, 1075:1075 + 156]
        logo = star_logo_cascade.detectMultiScale(roi_gray, 1.1, 4)

        setDetectionIntervals(type, logo)
        cv2ImShow(type, logo, roi_color)

    elif type == 'sony_logo' and sony_logo_cascade:
        roi_gray = gray[57:57 + 123, 1054:1054 + 123]
        roi_color = img[57:57 + 123, 1054:1054 + 123]
        logo = sony_logo_cascade.detectMultiScale(roi_gray, 1.1, 4)

        setDetectionIntervals(type, logo)
        cv2ImShow(type, logo, roi_color)

    elif type == 'mtv_logo' and mtv_logo_cascade:
        roi_gray = gray[17:17 + 120, 1090:1090 + 120]
        roi_color = img[17:17 + 120, 1090:1090 + 120]
        logo = mtv_logo_cascade.detectMultiScale(roi_gray, 1.2, 4)

        setDetectionIntervals(type, logo)
        cv2ImShow(type, logo, roi_color)

    elif type == 'zee_logo' and zee_logo_cascade:
        roi_gray = gray[11:11 + 181, 965:965 + 181]
        roi_color = img[11:11 + 181, 965:965 + 181]
        logo = zee_logo_cascade.detectMultiScale(roi_gray, 1.1, 4)

        setDetectionIntervals(type, logo)
        cv2ImShow(type, logo, roi_color)

    elif type == 'black_screen':
        setDetectionIntervals(type, img)

    elif type == 'ad_screen':
        setDetectionIntervals(type, img)

    return ''

def setDetectionIntervals(type, cascade):
    global cascade_captured_dict
    global intervals_dict
    global times_dict
    global capture_time_dict
    global calculated_times_dict


    cascadeLen = len(cascade)
    if(type == 'black_screen'):
        cascadeLen = 0
        frame_sum = np.sum(cascade)
        frame_sum_str = str(frame_sum)
        if frame_sum == 0 or len(frame_sum_str) < 8:
            cascadeLen = len(frame_sum_str)

    if(type == 'ad_screen'):
        cascadeLen = 0
        # number of times True exists in list
        listTmp = list(cascade_captured_dict.values());
        listTmp.pop()
        exist_count = listTmp.count(True)
        if exist_count == 0:
            cascadeLen = len(cascade)

    if cascadeLen > 0:
        if (timestamp_dict['common']['start'] == 0):
            timestamp_dict['common']['start'] = int(time.time_ns())

        cascade_captured_dict[type] = True
        timestamp_dict['common']['end'] = int(time.time_ns())

        times_list = calculateTimeDuration(timestamp_dict['common']['start'], timestamp_dict['common']['end'])

        calculated_times_dict[type].append(times_list)
        calculated_times_listLen = len(calculated_times_dict[type])
        timestamp_dict['common']['start'] = int(time.time_ns())

        sec = times_list[0] / 1000000000
        capture_time_dict[type] = capture_time_dict[type] + sec

        times_dict[type] = {
            'start_time': calculated_times_dict[type][0][1],
            'end_time': calculated_times_dict[type][calculated_times_listLen - 1][2],
            'duration': round(capture_time_dict[type], 5),
            'start_time_epoch': calculated_times_dict[type][0][3],
            'end_time_epoch': calculated_times_dict[type][calculated_times_listLen - 1][4],
        }
    else:
        cascade_captured_dict[type] = False
        capture_time_dict[type] = 0
        timestamp_dict['common']['start'] = int(time.time_ns())

        if (len(times_dict[type])):
            intervals_dict[type].append(times_dict[type])
            times_dict[type] = {}

def cv2ImShow(type, logo, roi_color):
    for (x, y, w, h) in logo:
        cv2.rectangle(roi_color, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow('Video', img)

while True:
    _, img = cap.read()
    if (_ == False):
        break;

    # Set Defaults Vars
    resetVars()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Black Screen Detection
    detectCascade(detect_types['black_screen'], img, gray)

    # Star Logo Detect
    detectCascade(detect_types['star_logo'], img, gray)

    # Sony Logo Detect
    detectCascade(detect_types['sony_logo'], img, gray)

    # Mtv Logo Detect
    detectCascade(detect_types['mtv_logo'], img, gray)

    # Zee Logo Detect
    detectCascade(detect_types['zee_logo'], img, gray)

    # Ad Screen Detection
    detectCascade(detect_types['ad_screen'], img, gray)


    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

for times_k in times_dict:
    if(len(times_dict[times_k]) > 0):
        intervals_dict[times_k].append(times_dict[times_k])
        times_dict[times_k] = {}
    if (len(times_dict[times_k]) > 0):
        intervals_dict[times_k].append(times_dict[times_k])
        times_dict[times_k] = {}

final_intervals_list = []
final_api_intervals_list = []
total_duration = 0
view_data = {}
view_data['device_id'] = 12345
view_data['creation_timestamp'] = int(time.time_ns())
api_record =[]
for k in intervals_dict:
    total_duration = 0
    intervalsLen = len(intervals_dict[k])
    api_record =[]
    if(intervalsLen):
        for key in intervals_dict[k]:
            total_duration = total_duration + key['duration']
            
    final_intervals_list.append({
        'name': k,
        'count': intervalsLen,
        'total_duration': round(total_duration, 5),
        'channelsTimesList': intervals_dict[k]
    })
    view_data['channels'] = final_intervals_list
print("viewData:",view_data)

print('')
print("intervals_dict")
for val in final_intervals_list:
    print(val)

print('End Program')
print('')




