import numpy as np
width = 0.57
height = 0.7
epsilon = 1e-3
rotate_times = 0

def Calculate_steering_angle(pt1, pt2, pt3):     # Calculate steering angle
    # Calculate method: Law of cosines
    a = Calculate_distance_between_two_points(pt1, pt2)
    b = Calculate_distance_between_two_points(pt2, pt3)
    c = Calculate_distance_between_two_points(pt1, pt3)
    cosine = (a**2+b**2-c**2)/(2*a*b)
    return np.pi - np.arccos(cosine)

def Calculate_distance_between_two_points(x1, x2):
    return np.sqrt((x1[0]-x2[0])**2+(x1[1]-x2[1])**2)

def Times_to_fine_tuning(angle): # Fine Tuning Times
    if angle < epsilon:
        return 0
    else:
        angle = np.abs(angle)
        return int(angle / (0.2 * np.pi)) + 1

def What_Angle_To_Rotate_to_clean_the_rubbish(rubbish, pt0, pt1): # Principle: Only rotate less than pi/2
    # Step1: If the rubbish is inside the robot, do nothing. To judge, we need an angle and a length
    angle_of_rubbish_and_robot_direction = Calculate_steering_angle(pt0, pt1, rubbish)
    angle_of_robot = np.arctan(width / height)
    if angle_of_rubbish_and_robot_direction > angle_of_robot and angle_of_rubbish_and_robot_direction < np.pi - angle_of_robot:
        max_length_of_inside_robot = width / 2 / np.sin(angle_of_rubbish_and_robot_direction)
        type = 1
    else:
        max_length_of_inside_robot = height / 2 / np.abs(np.cos(angle_of_rubbish_and_robot_direction))
        type = 2
    dist_between_rubbish_and_robot = Calculate_distance_between_two_points(rubbish, pt1)
    if dist_between_rubbish_and_robot <= max_length_of_inside_robot:
        return 0
    else:
        if type == 1:
            return min(angle_of_rubbish_and_robot_direction, np.pi - angle_of_rubbish_and_robot_direction) - np.arcsin(width / 2 / dist_between_rubbish_and_robot)
        else:
            return np.arccos(height / 2 / dist_between_rubbish_and_robot) - min(angle_of_rubbish_and_robot_direction, np.pi - angle_of_rubbish_and_robot_direction)

def start_rotate(x, y):
    print("#####Angle And Rotate Times Calculation")
    print("From Start to 1st Rotate")
    angle = np.arctan(x[0] - width / 2 / y[0] - height / 2)
    global rotate_times
    rotate_times = rotate_times + Times_to_fine_tuning(angle)
    print("Angle = {}, times = {}".format(angle, Times_to_fine_tuning(angle)))

def clean_rubbish(rubbish, sequence, x, y, i, coordinate_index):
    print("#####Rubbish " + str(i))
    if i == 1: # NO NEED TO MINUS 1
        pt0 = (width / 2, height / 2)
    else:
        pt0 = (x[coordinate_index - 1], y[coordinate_index - 1])
    pt1 = (x[coordinate_index], y[coordinate_index])
    if i != 14:
        pt2 = (x[coordinate_index + 1], y[coordinate_index + 1])

    print("rubbish coordinate: ({}, {})".format(rubbish[sequence[i - 1] - 1][0], rubbish[sequence[i - 1] - 1][1]))
    print("pt0 coordinate: ({}, {})".format(pt0[0], pt0[1]))
    print("pt1 coordinate: ({}, {})".format(pt1[0], pt1[1]))
    if i != 14:
        print("pt2 coordinate: ({}, {})".format(pt2[0], pt2[1]))
    angle_clean_rubbish = What_Angle_To_Rotate_to_clean_the_rubbish(rubbish[sequence[i - 1] - 1], pt0, pt1)
    global rotate_times
    rotate_times = rotate_times + Times_to_fine_tuning(angle_clean_rubbish)
    print("clean rubbish {}, angle = {}, times = {}".format(i, angle_clean_rubbish,
                                                           Times_to_fine_tuning(angle_clean_rubbish)))

    if i != 14:
        print("move to next direction")
        angel_to_move = Calculate_steering_angle(pt0, pt1, pt2) + angle_clean_rubbish
        rotate_times = rotate_times + Times_to_fine_tuning(angel_to_move)
        print("Angle = {}, times = {}".format(angel_to_move, Times_to_fine_tuning(angel_to_move)))

def transfer_rotate(x, y, coordinate_index):
    pt0 = (x[coordinate_index - 1], y[coordinate_index - 1])
    pt1 = (x[coordinate_index], y[coordinate_index])
    pt2 = (x[coordinate_index + 1], y[coordinate_index + 1])
    angle_rotate = What_Angle_To_Rotate_to_clean_the_rubbish(pt0, pt1, pt2)
    print("#####Transfer Rotate")
    global rotate_times
    rotate_times = rotate_times + Times_to_fine_tuning(angle_rotate)
    print("Angle = {}, times = {}".format(angle_rotate, Times_to_fine_tuning(angle_rotate)))


def calculate_critical_point_angle(x, y):
    print("#########Calculate critical point angle")
    Start_point = (width/2, height/2)
    for i in range(len(x)):
        if i == 0:
            pt0 = Start_point
        else:
            pt0 = (x[i-1], y[i-1])
        pt1 = (x[i], y[i])
        vector = (pt1[0] - pt0[0], pt1[1] - pt0[1])
        angle = np.arccos( abs(vector[0]) / Calculate_distance_between_two_points(pt0, pt1))
        if vector[0] < 0 and vector[1] >= 0:
            angle = np.pi - angle
        if vector[0] < 0 and vector[1] < 0:
            angle = np.pi + angle
        if vector[0] >= 0 and vector[1] < 0:
            angle = 2 * np.pi - angle
        print("Critical Point = {}, angle_to_x_positive = {}, degree = {}".format(i+1, angle, angle*180/np.pi))


def run(rubbish, sequence, x, y):
    start_rotate(x, y)
    # Rubbish 1
    clean_rubbish(rubbish, sequence, x, y, 1, 0)
    transfer_rotate(x, y, 1)
    clean_rubbish(rubbish, sequence, x, y, 2, 2)
    clean_rubbish(rubbish, sequence, x, y, 3, 3)
    clean_rubbish(rubbish, sequence, x, y, 4, 4)
    # Rubbish 5
    clean_rubbish(rubbish, sequence, x, y, 5, 5)
    transfer_rotate(x, y, 6)
    clean_rubbish(rubbish, sequence, x, y, 6, 7)
    clean_rubbish(rubbish, sequence, x, y, 7, 8)
    clean_rubbish(rubbish, sequence, x, y, 8, 9)
    clean_rubbish(rubbish, sequence, x, y, 9, 10)
    clean_rubbish(rubbish, sequence, x, y, 10, 11)
    clean_rubbish(rubbish, sequence, x, y, 11, 12)
    clean_rubbish(rubbish, sequence, x, y, 12, 13)
    clean_rubbish(rubbish, sequence, x, y, 13, 14)
    clean_rubbish(rubbish, sequence, x, y, 14, 15)

    print("Total Rotate Times: " + str(rotate_times))

    calculate_critical_point_angle(x, y)


