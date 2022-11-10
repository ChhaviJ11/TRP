import cv2
import time
import numpy as np

#xml cascade file
sony_logo_cascade = cv2.CascadeClassifier('E:\\TRP Code\\sony_cascade.xml')
star_logo_cascade = cv2.CascadeClassifier('E:\\TRP Code\\star_cascade.xml')
mtv_logo_cascade = cv2.CascadeClassifier('E:\\TRP Code\\mtv_cascade.xml')
zee_logo_cascade = cv2.CascadeClassifier('E:\\TRP Code\\zee_cascade.xml')

# To capture video from existing video.
cap = cv2.VideoCapture('E:\\TRP Code\\dd.mp4')

#variables used in sony logo detection
sony_logoCaptureStarted = False
sony_start_epoch_time = 0  # Initialize variable
sony_loop_start_epoch_time = int(time.time_ns())
no_sony_logo_detected = True
sony_time_intervals = []
sony_list = []

#variables used in star logo detection
star_logoCaptureStarted = False
star_start_epoch_time = 0  # Initialize variable
star_loop_start_epoch_time = int(time.time_ns())
no_star_logo_detected = True
star_time_intervals = []
star_list = []

#variables used in mtv logo detection
mtv_logoCaptureStarted = False
mtv_start_epoch_time = 0  # Initialize variable
mtv_loop_start_epoch_time = int(time.time_ns())
no_mtv_logo_detected = True
mtv_time_intervals = []
mtv_list = []

#variables used in zee logo detection
zee_logoCaptureStarted = False
zee_start_epoch_time = 0  # Initialize variable
zee_loop_start_epoch_time = int(time.time_ns())
no_zee_logo_detected = True
zee_time_intervals = []
zee_list = []

#variables used in ad detection
ad_time_intervals = []
no_logo_loop_start_epoch_time = int(time.time_ns())
no_logo_capture_start_time = 0
no_logo_detected_capture_start = False
ad_list = []

#variables used in blank screen
bsCalculatedTimesList = []
bsTimeIntervalsList =[]
bsTimesDict = {}
bsStartEpochTime = 0
bsTime = 0

def calculateTimeDuration(start_epoch_time, end_epoch_time):
    start_sec = int(start_epoch_time / 1000000000)
    epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    start_time = epoch_start_time

    end_sec = int(end_epoch_time / 1000000000)
    epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(end_sec))
    end_time = epoch_end_time

    time_detect = end_epoch_time - start_epoch_time
    return [time_detect, start_time, end_time]

def printData(channel_data_list):
    channel_dict={}

    channel_dict['start_time']= channel_data_list[1]

    channel_dict['end_time'] = channel_data_list[2]
    channel_dict['time_duration'] = channel_data_list[0]
    return channel_dict



while True:
    _, img = cap.read()
    if (_ == False):
        break;
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # if star logo detected
    if star_logo_cascade:
        roi_gray = gray[29:29 + 156, 1075:1075 + 156]
        roi_color = img[29:29 + 156, 1075:1075 + 156]

        # Detect the logo
        logo = star_logo_cascade.detectMultiScale(roi_gray, 1.1, 4)
        star_logoDetected = False
        if len(logo) == 0:
            no_star_logo_detected = True

        for (x, y, w, h) in logo:
            no_star_logo_detected = False
            if star_logoCaptureStarted == False:
                star_logoCaptureStarted = True
                star_start_epoch_time = int(time.time_ns())
            cv2.rectangle(roi_color, (x, y), (x + w, y + h), (255, 0, 0), 2)
            star_logoDetected = True

        cv2.imshow('Video', img)
        star_dict = {}
        if (star_logoCaptureStarted and star_logoDetected == False):
            star_end_epoch_time = int(time.time_ns())

            star_time = calculateTimeDuration(star_start_epoch_time, star_end_epoch_time)

            star_list.append(printData(star_time))

            star_logoCaptureStarted = False
            star_time_intervals.append(star_time[0])
            # Restart New Timer
            star_start_epoch_time = int(time.time_ns())

    # if mtv logo detected
    if mtv_logo_cascade:
        roi_gray = gray[17:17 + 120, 1090:1090 + 120]
        roi_color = img[17:17 + 120, 1090:1090 + 120]

        # Detect the logo
        logo = mtv_logo_cascade.detectMultiScale(roi_gray, 1.2, 4)
        mtv_logoDetected = False
        if len(logo) == 0:
            no_mtv_logo_detected = True

        for (x, y, w, h) in logo:
            no_mtv_logo_detected = False
            if mtv_logoCaptureStarted == False:
                mtv_logoCaptureStarted = True
                mtv_start_epoch_time = int(time.time_ns())
            cv2.rectangle(roi_color, (x, y), (x + w, y + h), (255, 255, 255), 2)
            mtv_logoDetected = True

        cv2.imshow('Video', img)
        mtv_dict = {}
        if (mtv_logoCaptureStarted and mtv_logoDetected == False):
            mtv_end_epoch_time = int(time.time_ns())

            mtv_time = calculateTimeDuration(mtv_start_epoch_time, mtv_end_epoch_time)

            mtv_list.append(printData(mtv_time))

            mtv_logoCaptureStarted = False
            mtv_time_intervals.append(mtv_time[0])
            # Restart New Timer
            mtv_start_epoch_time = int(time.time_ns())

    # if zee logo detected
    if zee_logo_cascade:
        roi_gray = gray[11:11 + 181, 965:965 + 181]
        roi_color = img[11:11 + 181, 965:965 + 181]

        # Detect the logo
        logo = zee_logo_cascade.detectMultiScale(roi_gray, 1.2, 4)
        zee_logoDetected = False
        if len(logo) == 0:
            no_zee_logo_detected = True

        for (x, y, w, h) in logo:
            no_zee_logo_detected = False
            if zee_logoCaptureStarted == False:
                zee_logoCaptureStarted = True
                zee_start_epoch_time = int(time.time_ns())
            cv2.rectangle(roi_color, (x, y), (x + w, y + h), (255, 255, 0), 2)
            zee_logoDetected = True

        cv2.imshow('Video', img)
        zee_dict = {}
        if (zee_logoCaptureStarted and zee_logoDetected == False):
            zee_end_epoch_time = int(time.time_ns())

            zee_time = calculateTimeDuration(zee_start_epoch_time, zee_end_epoch_time)

            zee_list.append(printData(zee_time))

            zee_logoCaptureStarted = False
            zee_time_intervals.append(zee_time[0])
            # Restart New Timer
            zee_start_epoch_time = int(time.time_ns())

    # if sony logo detected
    if sony_logo_cascade:

        roi_gray = gray[57:57 + 123, 1054:1054 + 123]
        roi_color = img[57:57 + 123, 1054:1054 + 123]

        # Detect the logo
        logo = sony_logo_cascade.detectMultiScale(roi_gray, 1.2, 4)
        sony_logoDetected = False
        if len(logo) == 0:
            no_sony_logo_detected = True

        for (x, y, w, h) in logo:
            no_sony_logo_detected = False
            if sony_logoCaptureStarted == False:
                sony_logoCaptureStarted = True
                sony_start_epoch_time = int(time.time_ns())
            cv2.rectangle(roi_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
            sony_logoDetected = True

        cv2.imshow('Video', img)
        sony_dict = {}
        if (sony_logoCaptureStarted and sony_logoDetected == False):
            sony_end_epoch_time = int(time.time_ns())

            sony_time = calculateTimeDuration(sony_start_epoch_time, sony_end_epoch_time)

            sony_list.append(printData(sony_time))

            sony_logoCaptureStarted = False
            sony_time_intervals.append(sony_time[0])
            # Restart New Timer
            sony_start_epoch_time = int(time.time_ns())

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

#star logo
if (star_logoCaptureStarted):
    star_end_epoch_time = int(time.time_ns())

    star_time = calculateTimeDuration(star_start_epoch_time, star_end_epoch_time)

    star_list.append(printData(star_time))

    star_logoCaptureStarted = False
    star_time_intervals.append(star_time[0])

star_loop_end_epoch_time = int(time.time_ns())
star_loop_logo_time = star_loop_end_epoch_time - star_loop_start_epoch_time

#mtv logo
if (mtv_logoCaptureStarted):
    mtv_end_epoch_time = int(time.time_ns())

    mtv_time = calculateTimeDuration(mtv_start_epoch_time, mtv_end_epoch_time)

    mtv_list.append(printData(mtv_time))

    mtv_logoCaptureStarted = False
    mtv_time_intervals.append(star_time[0])

mtv_loop_end_epoch_time = int(time.time_ns())
mtv_loop_logo_time = mtv_loop_end_epoch_time - mtv_loop_start_epoch_time

#zee logo
if (zee_logoCaptureStarted):
    zee_end_epoch_time = int(time.time_ns())

    zee_time = calculateTimeDuration(zee_start_epoch_time, zee_end_epoch_time)

    zee_list.append(printData(zee_time))

    zee_logoCaptureStarted = False
    zee_time_intervals.append(zee_time[0])

zee_loop_end_epoch_time = int(time.time_ns())
zee_loop_logo_time = zee_loop_end_epoch_time - zee_loop_start_epoch_time

#sony logo
if (sony_logoCaptureStarted):
    sony_end_epoch_time = int(time.time_ns())

    sony_time = calculateTimeDuration(sony_start_epoch_time, sony_end_epoch_time)

    sony_list.append(printData(sony_time))

    sony_logoCaptureStarted = False
    sony_time_intervals.append(sony_time[0])

sony_loop_end_epoch_time = int(time.time_ns())
sony_loop_logo_time = sony_loop_end_epoch_time - sony_loop_start_epoch_time


#star logo
star_time_intervals_seconds =[]
star_time = 0
for i in star_time_intervals:
    sec = i / 1000000000
    star_time = star_time+ sec
    star_time_intervals_seconds.append(sec)
star_final_data ={}
star_final_data['data'] = star_list
star_final_data['total_time'] = round(star_time,6)
print('Star Time ')
print(star_final_data)
print('STAR Time Intervals seconds')
print(star_time_intervals_seconds)
print('')

#mtv logo
mtv_time_intervals_seconds =[]
mtv_time = 0
for i in mtv_time_intervals:
    sec = i / 1000000000
    mtv_time = mtv_time+ sec
    mtv_time_intervals_seconds.append(sec)
mtv_final_data ={}
mtv_final_data['data'] = mtv_list
mtv_final_data['total_time'] = round(mtv_time,6)
print('mtv Time ')
print(mtv_final_data)
print('mtv Time Intervals seconds')
print(mtv_time_intervals_seconds)
print('')

#zee logo
zee_time_intervals_seconds =[]
zee_time = 0
for i in zee_time_intervals:
    sec = i / 1000000000
    zee_time = zee_time+ sec
    zee_time_intervals_seconds.append(sec)
zee_final_data ={}
zee_final_data['data'] = zee_list
zee_final_data['total_time'] = round(zee_time,6)
print('zee Time ')
print(zee_final_data)
print('zee Time Intervals seconds')
print(zee_time_intervals_seconds)
print('')

#sony logo
sony_time_intervals_seconds =[]
sony_time = 0
for i in sony_time_intervals:
    sec = i / 1000000000
    sony_time = sony_time+ sec
    sony_time_intervals_seconds.append(sec)
sony_final_data ={}
sony_final_data['data'] = sony_list
sony_final_data['total_time'] = round(sony_time,6)
print('sony Time ')
print(sony_final_data)
print('sony Time Intervals seconds')
print(sony_time_intervals_seconds)
print('')

print('')
print('End Program')
print('')



