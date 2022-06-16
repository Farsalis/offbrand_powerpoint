from presentation_queue import *


def assemble_presentation(*args):
    """
    Convert presentation to DLL
    """
    arg_list = args

    unpack_list = [list_obj for super_list_obj in list(arg_list) for list_obj in super_list_obj]
    # Weird list comprehension

    linked_list = DoubleLinkedList()
    for list_ in unpack_list:
        linked_list.append(list_)
    print(linked_list.__repr__())
    return linked_list
