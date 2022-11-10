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

#variables used in blank screen detection
blank_screen_captureStarted = False
blank_screen_start_epoch_time = 0  # Initialize variable
blank_screen_loop_start_epoch_time = int(time.time_ns())
no_blank_screen_logo_detected = True
blank_screen_time_intervals = []
blank_screen_list = []


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

while True:
    _, img = cap.read()
    if (_ == False):
        break;
    frameSum = np.sum(img)
    # print('framesum',frameSum)
    frameSumStr = str(frameSum)
    if frameSum == 0 and len(frameSumStr) < 8:
        bsStartEpochTime = int(time.time_ns())

        bsEndEpochTime = int(time.time_ns())
        timesList = calculateTimeDuration(bsStartEpochTime, bsEndEpochTime)
        bsCalculatedTimesList.append(timesList)
        bsCalculatedTimesListLen = len(bsCalculatedTimesList)
        bsStartEpochTime = int(time.time_ns())

        bsSec = timesList[0] / 1000000000
        bsTime = bsTime + bsSec
        bsTimesDict = {
            'start_time': bsCalculatedTimesList[0][1],
            'endt_time': bsCalculatedTimesList[bsCalculatedTimesListLen - 1][2],
            'duration': round(bsTime,6)
        }
        # print("if part", bsTimesDict)
    else:
        if (len(bsTimesDict)):
            bsTimeIntervalsList.append(bsTimesDict)
            bsTimesDict = {}
        # print("else part",bsTimeIntervalsList)

        bsStartEpochTime = int(time.time_ns())
        bsTime = 0

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

            start_sec = int(star_start_epoch_time / 1000000000)
            epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
            star_dict['start_time'] = epoch_start_time

            start_sec = int(star_end_epoch_time / 1000000000)
            epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
            star_dict['end_time'] = epoch_end_time

            time_detect = star_end_epoch_time - star_start_epoch_time
            star_dict['time_duration'] = time_detect

            star_list.append(star_dict)
            star_logo_time = star_end_epoch_time - star_start_epoch_time
            star_logoCaptureStarted = False
            star_time_intervals.append(star_logo_time)
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
        mtv_dict={}
        if (mtv_logoCaptureStarted and mtv_logoDetected == False):
            mtv_end_epoch_time = int(time.time_ns())

            start_sec = int(mtv_start_epoch_time / 1000000000)
            epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
            mtv_dict['start_time'] = epoch_start_time

            start_sec = int(mtv_end_epoch_time / 1000000000)
            epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
            mtv_dict['end_time'] = epoch_end_time

            time_detect = mtv_end_epoch_time - mtv_start_epoch_time
            mtv_dict['time_duration'] = time_detect

            mtv_list.append(mtv_dict)
            mtv_logo_time = mtv_end_epoch_time - mtv_start_epoch_time
            mtv_logoCaptureStarted = False
            mtv_time_intervals.append(mtv_logo_time)
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

            start_sec = int(zee_start_epoch_time / 1000000000)
            epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
            zee_dict['start_time'] = epoch_start_time
            start_sec = int(zee_end_epoch_time / 1000000000)
            epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
            zee_dict['end_time'] = epoch_end_time

            time_detect = zee_end_epoch_time - zee_start_epoch_time
            zee_dict['time_duration'] = time_detect

            zee_list.append(zee_dict)

            zee_logo_time = zee_end_epoch_time - zee_start_epoch_time
            zee_logoCaptureStarted = False
            zee_time_intervals.append(zee_logo_time)

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

            start_sec = int(sony_start_epoch_time / 1000000000)
            epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
            sony_dict['start_time'] = epoch_start_time

            start_sec = int(sony_end_epoch_time / 1000000000)
            epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
            sony_dict['end_time'] = epoch_end_time

            time_detect = sony_end_epoch_time - sony_start_epoch_time
            sony_dict['time_duration'] = time_detect

            sony_list.append(sony_dict)

            sony_logo_time = sony_end_epoch_time - sony_start_epoch_time
            sony_logoCaptureStarted = False
            sony_time_intervals.append(sony_logo_time)

            # Restart New Timer
            sony_start_epoch_time = int(time.time_ns())

    if (no_sony_logo_detected and no_star_logo_detected and no_mtv_logo_detected and no_zee_logo_detected):
        ad_dict = {}
        if no_logo_detected_capture_start == False:


            no_logo_capture_start_time = int(time.time_ns())
            no_logo_detected_capture_start = True
            print('ad start time')
            print(no_logo_capture_start_time)

            if (no_logo_detected_capture_start == True):
            # if (sony_logoCaptureStarted == False and star_logoCaptureStarted == False and zee_logoCaptureStarted == False and mtv_logoCaptureStarted == False):

                if (sony_logoCaptureStarted == True):
                    no_logo_capture_end_time = int(time.time_ns())
                if(star_logoCaptureStarted ==True):
                    no_logo_capture_end_time = int(time.time_ns())
                if(zee_logoCaptureStarted == True):
                    no_logo_capture_end_time = int(time.time_ns())
                if(mtv_logoCaptureStarted == True):
                # if (no_logo_detected_capture_start == True):
                    no_logo_capture_end_time =int(time.time_ns())


                    start_sec = int(no_logo_capture_start_time / 1000000000)
                    epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
                    ad_dict['start_time'] = epoch_start_time

                    start_sec = int(no_logo_capture_end_time / 1000000000)
                    epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
                    ad_dict['end_time'] = epoch_end_time

                    time_detect = no_logo_capture_end_time - no_logo_capture_start_time
                    ad_dict['time_duration'] = time_detect



                no_logo_detected_capture_start = False
                ad_list.append(ad_dict)
                ad_time_intervals.append(time_detect)
                if no_logo_detected_capture_start == False:
                    no_logo_detected_capture_start = True
                    no_logo_capture_start_time = int(time.time_ns())
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

#star logo
if (star_logoCaptureStarted):
    star_end_epoch_time = int(time.time_ns())

    start_sec = int(star_start_epoch_time / 1000000000)
    epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    star_dict['start_time'] = epoch_start_time

    start_sec = int(star_end_epoch_time / 1000000000)
    epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    star_dict['end_time'] = epoch_end_time

    time_detect = star_end_epoch_time - star_start_epoch_time
    star_dict['time_duration'] = time_detect

    star_list.append(star_dict)

    star_logo_time = star_end_epoch_time - star_start_epoch_time
    star_logoCaptureStarted = False
    star_time_intervals.append(star_logo_time)

star_loop_end_epoch_time = int(time.time_ns())
star_loop_logo_time = star_loop_end_epoch_time - star_loop_start_epoch_time

#mtv logo
if (mtv_logoCaptureStarted):
    mtv_end_epoch_time = int(time.time_ns())

    start_sec = int(mtv_start_epoch_time / 1000000000)
    epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    mtv_dict['start_time'] = epoch_start_time

    start_sec = int(mtv_end_epoch_time / 1000000000)
    epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    mtv_dict['end_time'] = epoch_end_time

    time_detect = mtv_end_epoch_time - mtv_start_epoch_time
    mtv_dict['time_duration'] = time_detect

    mtv_list.append(mtv_dict)

    mtv_logo_time = mtv_end_epoch_time - mtv_start_epoch_time
    mtv_logoCaptureStarted = False
    mtv_time_intervals.append(mtv_logo_time)

mtv_loop_end_epoch_time = int(time.time_ns())
mtv_loop_logo_time = mtv_loop_end_epoch_time - mtv_loop_start_epoch_time

# zee logo
if (zee_logoCaptureStarted):
    zee_end_epoch_time = int(time.time_ns())
    start_sec = int(zee_start_epoch_time / 1000000000)
    epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    zee_dict['start_time'] = epoch_start_time
    start_sec = int(zee_end_epoch_time / 1000000000)
    epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    zee_dict['end_time'] = epoch_end_time

    time_detect = zee_end_epoch_time - zee_start_epoch_time
    zee_dict['time_duration'] = time_detect

    zee_list.append(zee_dict)

    zee_logo_time = zee_end_epoch_time - zee_start_epoch_time
    zee_logoCaptureStarted = False
    zee_time_intervals.append(zee_logo_time)

zee_loop_end_epoch_time = int(time.time_ns())
zee_loop_logo_time = zee_loop_end_epoch_time - zee_loop_start_epoch_time

#sony logo
if (sony_logoCaptureStarted):
    sony_end_epoch_time = int(time.time_ns())

    start_sec = int(sony_start_epoch_time / 1000000000)
    epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    sony_dict['start_time'] = epoch_start_time

    start_sec = int(sony_end_epoch_time / 1000000000)
    epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
    sony_dict['end_time'] = epoch_end_time

    time_detect = sony_end_epoch_time -sony_start_epoch_time
    sony_dict['time_duration'] = time_detect

    sony_list.append(sony_dict)

    sony_logo_time = sony_end_epoch_time - sony_start_epoch_time
    sony_logoCaptureStarted = False
    sony_time_intervals.append(sony_logo_time)

sony_loop_end_epoch_time = int(time.time_ns())
sony_loop_logo_time = sony_loop_end_epoch_time - sony_loop_start_epoch_time

#
if (no_logo_detected_capture_start == True):
    # if (sony_logoCaptureStarted == False or star_logoCaptureStarted == False or zee_logoCaptureStarted == False or mtv_logoCaptureStarted == False):
    if (sony_logoCaptureStarted == False):
        no_logo_capture_end_time = sony_start_epoch_time
    if (star_logoCaptureStarted == False):
        no_logo_capture_end_time = star_start_epoch_time
    if (zee_logoCaptureStarted == False):
        no_logo_capture_end_time = zee_start_epoch_time
    if (mtv_logoCaptureStarted == False):
        # if (no_logo_detected_capture_start == True):
        no_logo_capture_end_time = mtv_start_epoch_time
        print('ad time')
        print(no_logo_capture_end_time)
        start_sec = int(no_logo_capture_start_time / 1000000000)
        epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
        ad_dict['start_time'] = epoch_start_time
                # print('epoch_start_time')
                # print(epoch_start_time)

        start_sec = int(no_logo_capture_end_time / 1000000000)
        epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
        ad_dict['end_time'] = epoch_end_time

        time_detect = no_logo_capture_end_time - no_logo_capture_start_time
        ad_dict['time_duration'] = time_detect


    ad_time_intervals.append(time_detect)
    ad_list.append(ad_dict)


        # no_logo_detected_capture_start = False

no_logo_loop_end_epoch_time = int(time.time_ns())
no_logo_loop_logo_time = no_logo_loop_end_epoch_time - no_logo_loop_start_epoch_time

#
# #blank_screen
# if (blank_screen_captureStarted and no_logo_detected_capture_start==False):
#     blank_screen_end_epoch_time = zee_start_epoch_time
#
#     start_sec = int(blank_screen_start_epoch_time / 1000000000)
#     epoch_start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
#     blank_screen_dict['start_time'] = epoch_start_time
#
#     start_sec = int(blank_screen_end_epoch_time / 1000000000)
#     epoch_end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(start_sec))
#     blank_screen_dict['end_time'] = epoch_end_time
#
#     time_detect = blank_screen_end_epoch_time - blank_screen_start_epoch_time
#     blank_screen_dict['time_duration'] = time_detect
#
#     blank_screen_list.append(blank_screen_dict)
#
#     blank_screen_logo_time = blank_screen_end_epoch_time - blank_screen_start_epoch_time
#     blank_screen_logoCaptureStarted = False
#     blank_screen_time_intervals.append(blank_screen_logo_time)
#
# blank_screen_loop_end_epoch_time = int(time.time_ns())
# blank_screen_loop_logo_time = blank_screen_loop_end_epoch_time - blank_screen_loop_start_epoch_time


# Release the VideoCapture object
cap.release()

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

# mtv logo
mtv_time_intervals_seconds =[]
mtv_time = 0
for i in mtv_time_intervals:
    sec = i / 1000000000
    mtv_time = mtv_time+ sec
    mtv_time_intervals_seconds.append(sec)
mtv_final_data ={}
mtv_final_data['data'] = mtv_list
mtv_final_data['total_time'] = round(mtv_time,6)
print('MTV Time ')
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
print('')
zee_final_data ={}
zee_final_data['data'] = zee_list
zee_final_data['total_time'] = round(zee_time,6)
print('Zee Time ')
print(zee_final_data)
print('zee Time Intervals seconds')
print(zee_time_intervals_seconds)
print('')

# sony logo
sony_time = 0
sony_time_intervals_seconds =[]
for i in sony_time_intervals:
    sec = i / 1000000000
    sony_time = sony_time+sec
    sony_time_intervals_seconds.append(sec)
sony_final_data ={}
sony_final_data['data'] = sony_list
sony_final_data['total_time'] = round(sony_time,6)
print('SONY Time ')
print(sony_final_data)
print('SONY Time Intervals seconds')
print(sony_time_intervals_seconds)
print('')

print('')
ad_time_intervals_seconds =[]
ad_time = 0
for i in ad_time_intervals:
    sec = i / 1000000000
    ad_time = ad_time + sec
    ad_time_intervals_seconds.append(sec)
ad_final_data ={}
ad_final_data['data'] = ad_list
ad_final_data['total_time'] = round(ad_time,5)
print('AD Time ')
print(ad_final_data)
print('AD Time Intervals seconds')
print(ad_time_intervals_seconds)
print('')
#
# #blank_screen
# blank_screen_time_intervals_seconds =[]
# blank_screen_time = 0
# for i in blank_screen_time_intervals:
#     sec = i / 1000000000
#     blank_screen_time = blank_screen_time+ sec
#     blank_screen_time_intervals_seconds.append(sec)
# print('')
# blank_screen_final_data ={}
# blank_screen_final_data['data'] = blank_screen_list
# blank_screen_final_data['total_time'] = round(blank_screen_time,6)
# print('blank_screen Time ')
# print(blank_screen_final_data)
# print('blank_screen Time Intervals seconds')
# print(blank_screen_time_intervals_seconds)
# print('')
print("bsTimeIntervalsList")
print(bsTimeIntervalsList)
print('')
print('End Program')
print('')






