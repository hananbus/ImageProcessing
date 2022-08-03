import cv2


def get_frames_and_fps(path):
    vid_obj = cv2.VideoCapture(path)
    frames_ls = []
    success = 1
    while success:
        try:
            success, image = vid_obj.read()
            frames_ls.append(image)
        except:
            break

    fps = vid_obj.get(cv2.CAP_PROP_FPS)

    return frames_ls[:-1], fps  # there's a None frame in the end


def write_video(name, frames, fps):
    height, width, _ = frames[0].shape
    output_name = f'{name}.mp4'
    nframes = len(frames)

    video_writer = cv2.VideoWriter(output_name, 0x7634706d, fps, (width, height))

    for frame in frames:
        video_writer.write(frame)

    cv2.destroyAllWindows()
    video_writer.release()

    print(f"Created video {output_name} with {nframes} frames")