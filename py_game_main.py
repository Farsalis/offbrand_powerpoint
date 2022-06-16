# import the pygame module, so you can use it
import threading

from pygame.constants import K_ESCAPE, K_s, K_t, K_RIGHT, K_LEFT

import shared_variables
from helper_methods import *
from presentation_creator import *


current_thread = threading.Thread()


def new_thread(presentation_state, screen, ll):
    """
    Create new thread to be joined later.
    """
    list_ = ll.get(presentation_state).data
    t_ = threading.Thread(target=new_section, args=(list_[0], screen, list_[1]))
    threads.append(t_)
    t_.start()

    global current_thread
    current_thread = t_


def slide_next(presentation_state, screen, ll):
    """
    Continue to next slide and join current thread.
    """
    end_section()

    try:
        current_thread.join()
    except AttributeError:
        raise AttributeError('No Current Thread')

    screen.fill(color)
    pygame.display.update()

    start_section()

    new_thread(presentation_state, screen, ll)


def main():
    """
    Start pygame application, execute presentation assembly,
    and analyze input to determine correct slide display.
    """
    pygame.init()
    pygame.display.set_caption("Presentation")

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    pygame.display.update(screen.fill(color))

    pygame.mouse.set_visible(False)

    running = True
    start_uninitialized = True

    linked_list = assemble_presentation(shared_variables.presentation_)

    presentation_state = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    end_section()
                    current_thread.join()
                    pygame.quit()
                elif event.key == K_s and start_uninitialized:
                    #  return_dict = mass_conversion(screen)
                    #  print(return_dict)

                    new_thread(presentation_state, screen, linked_list)
                    start_uninitialized = False
                elif event.key == K_t and not start_uninitialized:
                    end_section()
                    current_thread.join()
                elif event.key == K_RIGHT and not start_uninitialized:
                    if presentation_state == linked_list.size() - 1:
                        presentation_state = 0
                    else:
                        presentation_state += 1

                    slide_next(presentation_state, screen, linked_list)

                elif event.key == K_LEFT and not start_uninitialized:
                    if presentation_state <= 0:
                        presentation_state = linked_list.size() - 1
                    else:
                        presentation_state -= 1

                    slide_next(presentation_state, screen, linked_list)


if __name__ == "__main__":

    threads = []
    t_1 = threading.Thread(target=main, args=())
    threads.append(t_1)
    t_1.start()

    for thread in threads:
        thread.join()

    print('Successful Execution of All Threads')
