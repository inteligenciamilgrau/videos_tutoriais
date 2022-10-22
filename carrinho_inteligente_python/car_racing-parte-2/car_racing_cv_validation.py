import gym
import cv2
import imutils

env = gym.make("CarRacing-v2", render_mode="human", new_step_api=True)

last_steering = 0.0

done = False

# coloque aqui a sua melhor jogada
dict_params = {"speed": 0.15 ,"steering_control": 0.18 ,"pixel_x": 8 ,"pixel_y": 20 ,"range": 1500 ,"seed": 42 ,"score": 93.81625441696866 }

env.action_space.seed(dict_params["seed"])
observation, info = env.reset(seed=dict_params["seed"], return_info=True)

speed = dict_params["speed"] #rand_speed()
steering_control = dict_params["steering_control"] #rand_steering()

car_distance_pixel_x = dict_params["pixel_x"] #rand_car_distance_x()
car_distance_pixel_y = dict_params["pixel_y"] #rand_car_distance_y()

total_reward = 0

for i in range(dict_params["range"]):
    action = env.action_space.sample()

    action[0] = 0.0  # steering
    action[1] = speed #0.08  # speed / gas
    action[2] = 0.0  # brake

    y_player = 75
    y = y_player - car_distance_pixel_y #45
    y_far = 40

    x_player = 48
    x_left = x_player - car_distance_pixel_x # 42
    x_right = x_player + car_distance_pixel_x # 54

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

    print(i, "of", dict_params["range"], "reward", reward, "steering", action[0])

    total_reward = total_reward + reward

    image_cp = observation.copy()
    cv2.circle(image_cp, (x_left, y), 4, (0, 0, 255))
    cv2.circle(image_cp, (x_right, y), 4, (0, 0, 255))

    cv2.circle(image_cp, (x_far_left, y_far), 4, (0, 0, 255))
    cv2.circle(image_cp, (x_far_right, y_far), 4, (0, 0, 255))

    cv2.circle(image_cp, (x_player, y_player), 4, (255, 0, 0))

    cv2.cvtColor(image_cp, cv2.COLOR_RGB2BGR, image_cp)
    image_cp = imutils.resize(image_cp, 500)
    cv2.imshow("Player", image_cp)

    if done:
        observation, info = env.reset(return_info=True)

print("orginal score", dict_params["score"])
print("total reward", total_reward)
env.close()
