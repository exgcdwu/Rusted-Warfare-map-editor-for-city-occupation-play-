import time
import sys

from command._util._core import *

PROGRESS_TIME = 0
PROGRESS_TIME_LIST = []
PROGRESS_PREVIOUS_FLASH = 0
PROGRESS_PREVIOUS_NUM = None
PROGRESS_PREVIOUS_LEN = UNDERLINE_EVEN_NUM

def init_progress():
    global PROGRESS_TIME
    global PROGRESS_TIME_LIST
    global PROGRESS_PREVIOUS_FLASH
    global PROGRESS_PREVIOUS_NUM
    global PROGRESS_PREVIOUS_LEN
    PROGRESS_TIME = time.time()
    PROGRESS_TIME_LIST = []
    PROGRESS_PREVIOUS_FLASH = 0
    PROGRESS_PREVIOUS_NUM = None
    PROGRESS_PREVIOUS_LEN = UNDERLINE_EVEN_NUM

TIME_ITERATION = 5
TIME_FLASH = 1

def print_progress(iteration, total, time_iteration=TIME_ITERATION, hms_l = ['Est. ', 'h ', 'm ', 's '], prefix='', suffix='', decimals=1, length_p=UNDERLINE_EVEN_NUM, fill='=', isenter = False):

    global PROGRESS_TIME
    global PROGRESS_TIME_LIST
    global PROGRESS_PREVIOUS_FLASH
    global PROGRESS_PREVIOUS_NUM
    global PROGRESS_PREVIOUS_LEN

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))

    time_now = time.time() - PROGRESS_TIME

    if len(PROGRESS_TIME_LIST) < time_iteration:
        PROGRESS_TIME_LIST.append((time_now, total))
        ftime = ""
    else:
        if (time_now - PROGRESS_PREVIOUS_FLASH) < TIME_FLASH:
            decimal_time = PROGRESS_PREVIOUS_NUM
        else:
            tt = (time_iteration - (total - PROGRESS_TIME_LIST[0][1]))
            if tt <= 0:
                decimal_time = None
            else:
                decimal_time = (time_now - PROGRESS_TIME_LIST[0][0]) / \
                tt * (total - iteration)

            PROGRESS_PREVIOUS_NUM = decimal_time
            PROGRESS_PREVIOUS_FLASH = time_now

        PROGRESS_TIME_LIST.append((time_now, total))
        PROGRESS_TIME_LIST = PROGRESS_TIME_LIST[1:]
        
        if decimal_time == None:
            ftime = "| " + hms_l[3] + "N/A"
        else:
            decimal_sec = decimal_time % 60
            decimal_min = (decimal_time // 60) % 60
            decimal_hour = (decimal_time // 3600) % 60

            fhour = (("{0:.0f}").format((decimal_hour)) + " " + hms_l[0]) if decimal_hour > 0 else ""
            fmin = (("{0:.0f}").format((decimal_min)) + " " + hms_l[1]) if decimal_min > 0 else ""
            fsec = (("{0:.0f}").format((decimal_sec)) + " " + hms_l[2])

            ftime = "| " + hms_l[3] + fhour + fmin + fsec

    length = length_p - len(prefix) - len(suffix) - 20 - sum([len(i) for i in hms_l])
    filledLength = int(length * iteration // total)
    if filledLength == 0:
        filledLength = 1
    bar = fill * (filledLength - 1) + '>' + '-' * (length - filledLength)
    progress = f"\r{prefix} |{bar}| {percent}% {suffix} {ftime}"
    
    lp = len(progress)
    if lp < PROGRESS_PREVIOUS_LEN:
        clear_progress = '\r' + ' ' * (PROGRESS_PREVIOUS_LEN + 20) + '\r'
        sys.stdout.write(clear_progress)

    PROGRESS_PREVIOUS_LEN = lp
    sys.stdout.write(progress)
    sys.stdout.flush()
    if isenter and iteration == total:
        print("")

def print_progress_o(language, isverbose, iteration, total, time_iteration=TIME_ITERATION, length=UNDERLINE_EVEN_NUM, hms = ["h |时 ", "m |分 ", "s |秒 ", "Est. |估计 "], prefix='progress: |进度: ', suffix='finish|完成', decimals=1, fill='=', isenter = False):
    if isverbose:
        prefix_l = str_lang(language, prefix)
        suffix_l = str_lang(language, suffix)
        hms_l = [str_lang(language, i) for i in hms]
        print_progress(iteration, total, time_iteration, hms_l, prefix_l, suffix_l, decimals, length, fill, isenter)