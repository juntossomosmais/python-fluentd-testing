import copy
import os


def absolute_path_fluentd_output_file(test_file):
    my_current_directory = os.path.dirname(os.path.realpath(__file__))
    folder = f"{my_current_directory}/fluentd-setup/result"
    abs_path = f"{folder}/{test_file}"
    return folder, abs_path


def try_to_remove_key_otherwise_return_it(your_dict, *keys):
    your_dict = copy.deepcopy(your_dict)
    for key in keys:
        your_dict.pop(key, None)
    return your_dict
