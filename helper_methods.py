import os

import pygame
import pygame.image
from PIL import Image

general_path = 'C:\\Users\\scfre\\PycharmProjects\\powerpoint_presentation\\all_photos'

const_sleep_seconds = 2
ms_dilation = 1000
color = (0, 0, 0)

bool_val = True


def loop_pictures(endpoint, screen):
    """
    Loop through pictures available in a given directory
    """
    path = os.path.join(general_path, endpoint)
    os.chdir(path)

    for picture in os.listdir():
        if bool_val:
            print(picture)
            image = pygame.image.load(picture)
            image_key_fade(image,
                           screen, (abs(screen.get_width() - image.get_width()) / 2, abs((screen.get_height() -
                                                                                          image.get_height()) / 2)))

            pygame.time.delay(const_sleep_seconds * ms_dilation)  # Interval between pictures

            screen.fill(color)

            pygame.display.update()
        else:
            return None


def keep_picture(picture_path, screen):
    """
    Display one picture for indefinite amount of time,
    until main thread goes to next picture
    """
    path = os.path.join(general_path, picture_path)
    image = pygame.image.load(path)
    image_key_fade(image, screen, (abs(screen.get_width() - image.get_width()) / 2, abs((screen.get_height() -
                                                                                         image.get_height()) / 2)))


def image_key_fade(image, screen, position):
    """
    Place image, then fill screen x amount of times for "breath" effect.
    Cancel effect if main thread detects a switch to next slide.
    """
    for i in range(0, 256, 1):
        if bool_val:
            image.set_alpha(i)
            new_blit = screen.blit(image, position)
            pygame.display.update(new_blit)
            screen.fill(color)
        else:
            screen.fill(color)
            pygame.display.update()
            return


def check_if(dir_name, endpoint, screen):
    """
    Do not duplicate already changed image directories.
    Image conversion handles any directories if an override to a changed directory occurs.
    """
    path = os.path.join(general_path)
    os.chdir(path)

    for dir_ in os.listdir():
        if dir_ == dir_name:
            return False, False

    directory, dir_list = image_conversion(endpoint, screen)
    return directory, dir_list


def mass_conversion(screen):
    """
    Convert directory of directories
    """
    path = os.path.join(general_path)
    os.chdir(path)

    new_directories = []

    for item in os.listdir():
        directory, dir_list = check_if(f'{item}_changed', item, screen)
        new_directories.append(directory)
    return new_directories


def end_section():
    global bool_val
    bool_val = False


def start_section():
    global bool_val
    bool_val = True


def new_section(endpoint, screen, loop=False):
    """
    Intermediary function, display either picture or directory pictures
    for next slide (info comes from DLL)
    """
    if loop:
        while bool_val:
            loop_pictures(endpoint, screen)
    else:
        keep_picture(endpoint, screen)


def strip_name(string):
    """
    Strip path string to last file or directory name
    """
    for i in range(string.count('\\')):
        tup_str = string.partition('\\')
        string = tup_str[-1]
    return string


def image_conversion(endpoint_path, screen_=None):
    """
    Converts entire directory images for proper display (dependent on screen height)
    """
    path = os.path.join(general_path, endpoint_path)

    new_dir_name = f'{strip_name(path)}_changed'
    new_dir_path = os.path.join(general_path, new_dir_name)

    image_project_name = []

    os.chdir(path)

    try:
        os.mkdir(new_dir_path)
    except WindowsError:
        os.remove(new_dir_path)
        os.mkdir(new_dir_path)

    for file in os.listdir():
        if file.endswith(('jpg', 'png')):
            image = Image.open(file)
            print(file, new_dir_name)

            div = image.height / screen_.get_height()
            width = int(image.width / div)
            height = screen_.get_height()

            image_name = f'{new_dir_name}_pic_{file}'
            new_image = image.resize((width, height))
            new_image.save(f'{new_dir_path}\\{image_name}')

            image_project_name.append(f'{new_dir_name}_pic_{file}')

    return new_dir_name, image_project_name
