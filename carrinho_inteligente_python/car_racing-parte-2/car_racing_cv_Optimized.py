import datetime
import math
import random

import gym
import cv2
import imutils

show_cv = True
show_cv = False

if show_cv:
    env = gym.make("CarRacing-v2", render_mode="human", new_step_api=True)
else:
    env = gym.make("CarRacing-v2", new_step_api=True)

seed = 42
env.action_space.seed(seed)
observation, info = env.reset(seed=seed, return_info=True)

#print("action", env.action_space)

last_steering = 0.0

done = False

gameplay = 0
gameplays = 100

actual_frame = 0
frames_max_per_play = 1500

def rand_speed():
    return random.randrange(1,100,1)/100

def rand_steering():
    return random.randrange(1,100,1)/100

def rand_car_distance_x():
    return random.randrange(1,40,1)

def rand_car_distance_y():
    return random.randrange(1,40,1)

speed = rand_speed()
steering_control = rand_steering()

car_distance_pixel_x = rand_car_distance_x()
car_distance_pixel_y = rand_car_distance_y()

total_reward = 0

best_score = -math.inf
best_score_second = -math.inf
best_score_third = -math.inf

gameplay_best = 0
gameplay_best_second = 0
gameplay_best_third = 0

best_speed = 0
best_steering = 0
best_x = 0
best_y = 0


start_time = datetime.datetime.now()

print("Starting!!")
print("Jogando primeira partida - Aguarde")

while not gameplay == gameplays:
    action = env.action_space.sample()

    action[0] = 0.0  # steering
    action[1] = speed # 0.08  # speed / gas
    action[2] = 0.0  # brake

    y_player = 75
    y = y_player - car_distance_pixel_y#45
    y_far = 40

    x_player = 48
    x_left = x_player - car_distance_pixel_x # 42
    x_right = x_player + car_distance_pixel_x #54

    x_far_left = 22
    x_far_right = 74

    player_left_pixel = observation[y, x_left]
    player_right_pixel = observation[y, x_right]

    player_far_left_pixel = observation[y_far, x_far_left]
    player_far_right_pixel = observation[y_far, x_far_right]

    if player_left_pixel[1] > 200 and player_right_pixel[1] > 200:
        action[0] = last_steering
    elif player_left_pixel[1] > 200:
        action[0] = steering_control
    elif player_right_pixel[1] > 200:
        action[0] = -steering_control
    elif player_far_left_pixel[1] < 200:
        action[0] = -0.1
    elif player_far_right_pixel[1] < 200:
        action[0] = 0.1
    else:
        action[0] = 0.0

    last_steering = action[0]

    observation, reward, done, truncated, info = env.step(action)

    if show_cv:
        image_cp = observation.copy()
        cv2.circle(image_cp, (x_left, y), 4, (0, 0, 255))
        cv2.circle(image_cp, (x_right, y), 4, (0, 0, 255))

        cv2.circle(image_cp, (x_far_left, y_far), 4, (0, 0, 255))
        cv2.circle(image_cp, (x_far_right, y_far), 4, (0, 0, 255))

        cv2.circle(image_cp, (x_player, y_player), 4, (255, 0, 0))

        cv2.cvtColor(image_cp, cv2.COLOR_RGB2BGR, image_cp)
        image_cp = imutils.resize(image_cp, 500)
        cv2.imshow("Player", image_cp)

    actual_frame += 1

    total_reward = total_reward + reward

    if done or actual_frame == frames_max_per_play:
        actual_frame = 0
        gameplay += 1

        if total_reward > best_score:

            best_score_third = best_score_second
            best_score_second = best_score
            best_score = total_reward

            gameplay_best_third = gameplay_best_second
            gameplay_best_second = gameplay_best
            gameplay_best = gameplay

            best_speed = speed
            best_steering = steering_control
            best_x = car_distance_pixel_x
            best_y = car_distance_pixel_y

        timeElapsed = datetime.datetime.now() - start_time
        start_time = datetime.datetime.now()

        print("##############")
        print(gameplay, "of", gameplays, "Total reward", total_reward, "elapsed", timeElapsed)
        print("Parameters", "Speed", speed, "steering_control", steering_control, "pixel_x", car_distance_pixel_x, "pixel_y", car_distance_pixel_y)

        print("Third place index", gameplay_best_third, best_score_third)
        print("Second place index", gameplay_best_second, best_score_second)

        print("First place index", gameplay_best, best_score)
        print("Partial best Parameters")
        print('{"speed":', best_speed, ',"steering_control":', best_steering, ',"pixel_x":', best_x,
              ',"pixel_y":', best_y, ',"range":', frames_max_per_play, ',"seed":', seed, ',"score":', best_score, "}")

        speed = rand_speed()
        steering_control = rand_steering()
        car_distance_pixel_x = rand_car_distance_x()
        car_distance_pixel_y = rand_car_distance_y()

        total_reward = 0

        observation, info = env.reset(seed=seed, return_info=True)

print("Final Record", best_score, "gameplay", gameplay_best)
env.close()
