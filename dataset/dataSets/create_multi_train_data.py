import math
from datetime import datetime,timedelta
import numpy as np


file_suffix = '.csv'
route_dict = {'B-3': 165.0, 'B-1': 241.0, 'A-3': 276.66, 'A-2': 111.33, 'C-3': 260.66, 'C-1': 336.66}


def create(in_file, num_window):

    in_file_name = in_file + file_suffix
    # Step 1: Load trajectories
    fr = open(in_file_name, 'r')
    fr.readline()  # skip the header
    traj_data = fr.readlines()
    fr.close()

    six_time = []
    temp_time = datetime.now()
    temp_travel_time = 0
    count = 0
    fid = open('train_{}_id.txt'.format(num_window-1), 'w')
    for i in range(len(traj_data)):
        # print traj_data[i]
        each_traj = traj_data[i].replace('"', '').split(',')
        intersection_id = each_traj[0]
        tollgate_id = each_traj[1]
        interval_left = each_traj[2][1:]
        travel_time = each_traj[4][:-1]
        start_time = datetime.strptime(interval_left, "%Y-%m-%d %H:%M:%S")
        start_time_window = datetime(start_time.year, start_time.month, start_time.day, start_time.hour, start_time.minute, 0)
        if len(six_time) == 0:
            six_time.append(temp_travel_time)
        if (start_time_window - temp_time).seconds == 1200:
            six_time.append(travel_time)
            if len(six_time) == num_window:
                # print six_time
                with open('multi_train_data/travel_{}_{}.txt'.format(num_window-1, count), 'w') as fw:
                    route_id = route_dict[intersection_id+'-'+tollgate_id]
                    obj_time = start_time_window.hour * 60 + start_time_window.minute
                    fw.write(str(route_id))
                    for tt in six_time:
                        fw.write(' ' + tt)
                    fw.write(' ' + str(obj_time/4.0))
                    weekday = start_time_window.weekday() * 30 + 100
                    fw.write(' ' + str(weekday))
                
                del six_time[0]
                fid.write(str(count) + '\n')
                count += 1
        else:
            six_time = []

        temp_time = start_time_window
        temp_travel_time = travel_time
        # print start_time_window, travel_time, six_time
        # wait = raw_input()
    fid.close()


def main():

    in_file = 'training/training_20min_avg_travel_time'
    for i in xrange(6):
        create(in_file, i+2)

if __name__ == '__main__':
    main()

