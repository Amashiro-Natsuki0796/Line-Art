import cv2
import numpy as np
import random
import colorsys
from tqdm import tqdm

def random_vibrant_color():
    h = random.random()  # Hue: 色相（0~1）
    s = random.uniform(0.8, 1.0)  # Saturation: 高饱和度
    v = random.uniform(0.8, 1.0)  # Value (Brightness): 高亮度
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return (int(b * 255), int(g * 255), int(r * 255))  # OpenCV 是 BGR 顺序

def process_frame(img, line_count=1500):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    canvas = np.ones_like(img)  # 黑色画布

    contour_points = []
    for cnt in contours:
        for pt in cnt:
            contour_points.append(pt[0])
    contour_points = np.array(contour_points)

    if len(contour_points) < 2:
        return canvas  # 没轮廓就返回空白帧

    for _ in range(line_count):
        idx1 = random.randint(0, len(contour_points)-1)
        idx2 = random.randint(0, len(contour_points)-1)
        pt1 = tuple(contour_points[idx1])
        pt2 = tuple(contour_points[idx2])

        color = random_vibrant_color()
        cv2.line(canvas, pt1, pt2, color, thickness=1)

    return canvas


def video_abstract_lines(input_video="/Users/ayin/Downloads/input.mp4", output_video="1output.mp4", line_count=200):
    cap = cv2.VideoCapture(input_video)
    if not cap.isOpened():
        print("无法打开视频文件")
        return

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (w, h))

    # 使用tqdm创建进度条
    with tqdm(total=total, desc="处理视频帧", unit="帧") as pbar:
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = process_frame(frame, line_count=line_count)
            out.write(processed_frame)

            frame_idx += 1
            pbar.update(1)  # 更新进度条

    cap.release()
    out.release()
    print(f"完成，已保存为：{output_video}")


if __name__ == "__main__":
    video_abstract_lines(input_video="input/input.mp4", output_video="output/output.mp4", line_count=200)