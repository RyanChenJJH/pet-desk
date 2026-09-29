import os
import glob
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
from rembg import remove, new_session

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DIR = os.path.join(BASE_DIR, "01_raw_doubao")
THEME_ASSETS_DIR = os.path.join(BASE_DIR, "theme", "assets")
EXPORT_DIR = os.path.join(BASE_DIR, "03_export")
FORGE_DIR = os.path.join(BASE_DIR, "02_forge")
TEMP_FRAMES_ROOT = os.path.join(FORGE_DIR, "temp_frames")

TARGET_SIZE = 256
EXTRACT_FPS = 10


def extract_frames_from_video(video_path, output_dir, fps=EXTRACT_FPS):
    os.makedirs(output_dir, exist_ok=True)
    for f in glob.glob(os.path.join(output_dir, "*.png")):
        os.remove(f)

    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", f"fps={fps}",
        os.path.join(output_dir, "frame_%03d.png")
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    return sorted(glob.glob(os.path.join(output_dir, "frame_*.png")))


def process_single_frame(fpath, session):
    img = Image.open(fpath)
    nobg = remove(img, session=session)

    arr = np.array(nobg)
    h, w = arr.shape[:2]

    # Clean bottom-right "豆包AI生成" watermark area
    arr[int(h * 0.93):, int(w * 0.82):, 3] = 0

    # Alpha noise thresholding
    alpha = arr[:, :, 3]
    arr[alpha < 25, 3] = 0
    cleaned = Image.fromarray(arr)

    resized = cleaned.resize((TARGET_SIZE, TARGET_SIZE), Image.Resampling.LANCZOS)
    return resized


def process_state(file_path, session):
    state_name = os.path.splitext(os.path.basename(file_path))[0]
    v_t0 = time.time()
    print(f"\nProcessing state: {state_name} ({file_path})", flush=True)

    temp_dir = os.path.join(TEMP_FRAMES_ROOT, state_name)
    frames = extract_frames_from_video(file_path, temp_dir)
    print(f"  Extracted {len(frames)} frames at {EXTRACT_FPS} FPS.", flush=True)

    frame_duration_ms = int(1000 / EXTRACT_FPS)

    processed_images = [None] * len(frames)

    def worker(idx):
        processed_images[idx] = process_single_frame(frames[idx], session)

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(worker, range(len(frames))))

    for out_path in (
        os.path.join(THEME_ASSETS_DIR, f"{state_name}.apng"),
        os.path.join(EXPORT_DIR, f"{state_name}.apng"),
    ):
        processed_images[0].save(
            out_path,
            format="PNG",
            save_all=True,
            append_images=processed_images[1:],
            duration=frame_duration_ms,
            loop=0,
        )
        print(f"  [APNG] {out_path} ({os.path.getsize(out_path) / 1024:.1f} KB)", flush=True)

    forge_gif_path = os.path.join(FORGE_DIR, f"{state_name}_preview.gif")
    processed_images[0].save(
        forge_gif_path,
        format="GIF",
        save_all=True,
        append_images=processed_images[1:],
        duration=frame_duration_ms,
        loop=0,
        transparency=0,
        disposal=2,
    )

    print(f"  Completed {state_name} in {time.time() - v_t0:.1f}s", flush=True)
    return state_name


def main():
    for d in (RAW_DIR, THEME_ASSETS_DIR, EXPORT_DIR, FORGE_DIR):
        os.makedirs(d, exist_ok=True)

    raw_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.mp4")))
    if not raw_files:
        print(f"No .mp4 files found in {RAW_DIR}")
        return

    print(f"Found {len(raw_files)} videos to process.", flush=True)

    session = new_session("isnet-anime")
    total_start = time.time()

    for idx, fpath in enumerate(raw_files):
        print(f"\n==========================================")
        print(f"Progress: [{idx + 1}/{len(raw_files)}]", flush=True)
        process_state(fpath, session)

    print(f"\n==========================================")
    print(f"SUCCESS: All {len(raw_files)} animations processed in {(time.time() - total_start) / 60:.1f} minutes!")


if __name__ == "__main__":
    main()
