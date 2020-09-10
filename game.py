import random

import requests

from sense_hat import SenseHat
from time import sleep

# Initialise SenseHat 
sense = SenseHat()

# Keep the score!
score = 0

API_ENDPOINT = "https://gyrododge.herokuapp.com/api/v1/score/new/"

# The player's X position
pixel_x = 4

# Colours!
white = (255, 255, 255)
red = (255, 0, 0)


sense.clear()

# Initialise three obstacles on random positions. Obstacles are reused.
obstacles = [
    [random.randint(0, 7), 8],
    [random.randint(0, 7), 10],
    [random.randint(0, 7), 14],
]
 
# Obstacles should fall down
obstacle_velocity = [0, 1]


def draw_pixel():
    """Draws the player pixel."""
    sense.set_pixel(pixel_x, 0, white)
 
def move_left():
    """Move the player pixel left."""
    global pixel_x
    pixel_x += 1
 
def move_right():
    """Move the player pixel right."""
    global pixel_x
    pixel_x -= 1

def submit_score():
    
    sense.set_rotation(180)
    sense.show_message('ENTER NAME')
    sense.set_rotation(0)
    sense.clear()
    name = ""
    name = input("Enter your name (max 3 letters):")
    while name == "" or len(name) > 3:
        if name != "":
            print("That name is too long!")
        name = input("Enter your name (max 3 letters):")
    
    payload = {
        "points": score,
        "name": name.upper(),
    }
    
    try:
        res = requests.post(API_ENDPOINT, json=payload)
    except:
        return None
    print("Status:", res.status_code)
    print("Response:", res.text)
    return res.json()["position"]
    
def reset_game():
    global score
    global obstacles
    global pixel_x
    score = 0
    obstacles = [
        [random.randint(0, 7), 8],
        [random.randint(0, 7), 10],
        [random.randint(0, 7), 14],
    ]
    pixel_x = 4

def detect_collisions():
    """Used to detect collisions with obstacles."""

    for obstacle in obstacles:
        if obstacle[0] == pixel_x and obstacle[1] <= 0:
            sense.set_rotation(180)
            sense.show_message('GAME OVER')
            sense.show_message('SCORE')
            sense.show_message(str(score))

            position = submit_score()           
            
            sense.set_rotation(180)
            if position:
                sense.show_message('POS')
                sense.show_message(str(position))
            else:
                sense.show_message('NO INTERNET!')
            sense.set_rotation(0)
            
            reset_game()
 
def move_obstacles():
    """Moves all obstacles to their next position."""

    # For every obstacle we have
    for obstacle in obstacles:
        # If the obstacle is now at the bottom, place it at the top again
        if obstacle[1] < 0:
            # Place at a random position on the x-axis
            obstacle[0] = random.randint(0, 7)
            # Place on a random position on the y-axis outside the screen.
            obstacle[1] = random.randint(8, 15)
            
            global score
            # The player survived this obstacle, increase their score.
            score += 1
            print("Score:", score)
        
        # Move the obstacle down
        obstacle[1] -= obstacle_velocity[1]
 
def draw_obstacles():
    """Draws all obstacles."""
    
    # For every obstacle we have
    for obstacle in obstacles:
        # Draw the obstacle if on screen
        if obstacle[1] < 8 and obstacle[1] >= 0:
            sense.set_pixel(obstacle[0], obstacle[1], red)

def detect_movement():
    """Detect accelerometer input and move the player accordingly."""

    # Read acceleration
    acceleration = sense.get_accelerometer_raw()
    x = round(acceleration['x'], 1)
    y = round(acceleration['y'], 0)
    z = round(acceleration['z'], 0)

    # Move if over threshold and don't move off the screen
    if x >= 0.3 and pixel_x != 7:
        move_left()
    # Move if over threshold and don't move off the screen
    if x <= -0.3 and pixel_x != 0:
        move_right()

# frame counter. Used to only move obstacles on even frames
frame = 0

# Game loop
while True:
    draw_obstacles()
    draw_pixel()
    frame += 1

    # Only move obstacles if even frame
    if frame % 2 == 0:
        move_obstacles()
        detect_collisions()
        # Reset frame counter
        frame = 0
    # Detect accelerometer movement
    detect_movement()

    # Wait before next frame
    sleep(0.25)
    sense.clear()
