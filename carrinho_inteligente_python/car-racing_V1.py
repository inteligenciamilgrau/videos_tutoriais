import gym
import cv2
import imutils

env = gym.make("CarRacing-v2", render_mode="human", new_step_api=True)

seed = 42
env.action_space.seed(seed)
observation, info = env.reset(seed=seed, return_info=True)

#print("action", env.action_space)

last_steering = 0.0

done = False

total_reward = 0

for i in range(1500):
#while not done:
    action = env.action_space.sample()

    action[0] = 0.0  # steering
    action[1] = 0.08  # speed / gas
    action[2] = 0.0  # brake

    y_player = 75
    y = 45
    y_far = 40

    x_player = 48
    x_left = 42
    x_right = 54

    x_far_left = 22
    x_far_right = 74

    player_left_pixel = observation[y, x_left]
    player_right_pixel = observation[y, x_right]

    player_far_left_pixel = observation[y_far, x_far_left]
    player_far_right_pixel = observation[y_far, x_far_right]

    if player_left_pixel[1] > 200 and player_right_pixel[1] > 200:
        action[0] = last_steering
    elif player_left_pixel[1] > 200:
        action[0] = 0.5
    elif player_right_pixel[1] > 200:
        action[0] = -0.5
    elif player_far_left_pixel[1] < 200:
        action[0] = -0.1
    elif player_far_right_pixel[1] < 200:
        action[0] = 0.1
    else:
        action[0] = 0.0

    last_steering = action[0]

    observation, reward, done, truncated, info = env.step(action)

    print(i, "reward", reward, "steering", action[0])

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
        observation, info = env.reset(seed=seed, return_info=True)

print("Total reward", total_reward)
env.close()
