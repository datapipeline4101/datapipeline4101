from random import randint

def flight_path(position_x, frame_distance):
    new_position_x = position_x + frame_distance[0] #pow function isn't working
    new_position_y = 0.01 * position_x**2
    new_position_z = 0.01 * position_x**2
    new_position = (new_position_x, new_position_y, new_position_z)
    return new_position

def main():
    positions = [[0,0,1],[1,6,1]]
    start_position = positions[0]
    end_position = positions[1]
    start_to_finish = tuple(map(lambda i, j: j-i, start_position, end_position))
    video_length = 30 #User input in seconds. Usually input but it's a set number for testing purposes
    position_amount = video_length * 24
    frame_distance = tuple(map(lambda i: i/position_amount, start_to_finish))
    print("start position", start_position)
    for i in range(position_amount):
        start_position = flight_path(start_position[0], frame_distance)
        print("new position", start_position)
main()

#video length * framerate (always 24 FPS) = ammount of positions necessary
#divide length by frames
#LET'S TRY:  distance between start and finish divided by (ammount of positions necessary)