import numpy as np
from inspect import getmembers, isfunction

import distfunctions
import videoadapter
from framestree import build_frames_tree


def find_closet_key(keys, val):
    keys_arr = np.asarray(keys)
    idx = (np.abs(keys_arr - int(val))).argmin()
    return keys_arr[idx]


def main():
    dist_functions = [tup[1] for tup in getmembers(distfunctions, isfunction)]

    video_path = input("Please enter video path: ")
    num_of_levels = int(input("Please enter wanted number of levels for the frames tree: "))
    print("Please enter the number of the wanted distance function:")
    num_of_func = int(input("\n".join(f'{i} - {f.__name__}' for i, f in enumerate(dist_functions, 1)) + "\n")) - 1
    dist_function = dist_functions[num_of_func]

    print("Loading video...")
    frames, fps = videoadapter.get_frames_and_fps(video_path)

    print("Building frames tree...")
    tree = build_frames_tree(num_of_levels, frames, dist_function)
    levels = list(tree.keys())

    print(f"Available frame levels: {levels}")
    while True:
        video_name = input("Please enter the name for the output video, or 'q' to quit: ")
        if video_name.lower() == 'q':
            break
        wanted_frames = input("Please enter the number of wanted frames: ")

        closet_key = find_closet_key(levels, wanted_frames)
        frames_from_tree = tree[closet_key]
        videoadapter.write_video(video_name, frames_from_tree, fps)


if __name__ == '__main__':
    main()