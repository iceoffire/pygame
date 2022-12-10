# Personal Projects using Pygame

This repo was previously used by me in order to save developed projets created while studying Digital Games at FATEC Antônio Russo.

Pygame is a really fun library to develop games, and I'm happy to contribute with the community by sharing my code here.

# How To Use

## Installing Python

You need to install Python and Pip in order to use this repository. The supported version is `python 3+`, and you can download it from the [official](https://www.python.org) website.

You also can download it using the command line, in a [Linux](https://docs.python-guide.org/starting/install3/linux/) or [Mac](https://docs.python-guide.org/starting/install3/osx/) machine. Follow the guide for your Operational System.


## Installing Pygame

Each project in the **Project** Folder is gonna have a `requirements.txt` file with all the required libraries to download.

You don't need to open the file in order to use it, you can run it by the command line, like below.

```
$ pip install -r requirements.txt
```

Most projects are gonna have only `pygame` as a requirement, so you are good to play the projects by only having `pygame` installed.


# Projects

You can access all the projects by entering in the **Project** folder.

The list of projects is bellow, and the current status for those projects you can also find here.

## How to Run

Every project has it own `main.py` file, that's responsible for beeing the major file, and the first one to be executed.

You can run by following the bellow command in your specific OS.

### Windows + Mac
```
$ python main.py
```

### Linux
```
$ python3 main.py
```

## Ball Toward Mouse

Code exploring the physics behind a Angry Birds game. The code is not complete since it doesn't explore collisions. You can find `oblique throw` simulation in this project.

## Block Breaker

As its name suggest, this project is about a block breaker game. It uses only native shapes draw of pygame.

## Ninja Platform Style

This game is a POC of creating dynamic maps. You can manipulate the map creation by updating the `/assets/image/map/map1.png` image file.

Follow this color schema:

| Color | Description |
| ----- | ----------- |
| ⬛ | dirt |
| 🟦 | spawn |
| 🟥 | objective |
| ⬜ | nothing |

The structure tries to match the best construction style in order to create the map.

You can also access this project in the pygame forum [here](https://www.pygame.org/project/3530).

![image](https://user-images.githubusercontent.com/36308052/206822181-a90bce15-e524-47d4-81be-0534f04ac48e.png)


## OpenGL3D

A POC to test the creation of 3D renders using OpenGL and showing it  in the pygame draw.

## POC Surface

Simplified POC of the Ninja Platform Style.

## Paint

A Paint implementation using pygame.

## Particle System

Creation of a Particle System that runs in the CPU.
You can also access this project in the pygame forum [here](https://www.pygame.org/project/3529)

![image](https://user-images.githubusercontent.com/36308052/206822198-96ea1cd0-7f84-4f1d-81ab-a78f05c760f8.png)


## Space Invaders

A Space Invaders implementation in pygame. This game was created trying to show the powers of pygame.

![image](https://user-images.githubusercontent.com/36308052/206822288-e90ad759-f9c9-4525-b1e9-dc2b5da979d9.png)
