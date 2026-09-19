import os
import glob
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import numpy as np
from rembg import remove, new_session

def extract_frames_from_video(video_path, output_dir, fps=10):
    os.makedirs(output_dir, exist_ok=True)
    for f in glob.glob(os.path.join(output_dir, "*.png")):
        try:
            os.remove(f)
        except:
            pass

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

    # Clean bottom-right watermark area (豆包AI生成 watermark)
    arr[int(h * 0.93):, int(w * 0.82):, 3] = 0

    # Alpha noise thresholding
    alpha = arr[:, :, 3]
    arr[alpha < 25, 3] = 0
    cleaned = Image.fromarray(arr)

    # Standard 256x256 resizing
    resized = cleaned.resize((256, 256), Image.Resampling.LANCZOS)
    return resized

def process_state(file_path, session, output_dirs, fps=10):
    state_name = os.path.splitext(os.path.basename(file_path))[0]
    theme_assets_dir, export_dir, forge_dir, temp_frames_root = output_dirs
    v_t0 = time.time()
    print(f"\nProcessing state: {state_name} ({file_path})")

    temp_dir = os.path.join(temp_frames_root, state_name)
    frames = extract_frames_from_video(file_path, temp_dir, fps=fps)
    print(f"  Extracted {len(frames)} frames at {fps} FPS.")

    frame_duration_ms = int(1000 / fps)

    # Multi-threaded rembg processing
    processed_images = [None] * len(frames)
    def worker(idx):
        processed_images[idx] = process_single_frame(frames[idx], session)

    with ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(worker, range(len(frames))))

    # 1. Save APNG to theme/assets/
    theme_apng_path = os.path.join(theme_assets_dir, f"{state_name}.apng")
    processed_images[0].save(
        theme_apng_path,
        format="PNG",
        save_all=True,
        append_images=processed_images[1:],
        duration=frame_duration_ms,
        loop=0
    )
    theme_kb = os.path.getsize(theme_apng_path) / 1024
    print(f"  [APNG] Saved Theme Asset: {theme_apng_path} ({theme_kb:.1f} KB)")

    # 2. Save APNG to 03_export/
    export_apng_path = os.path.join(export_dir, f"{state_name}.apng")
    processed_images[0].save(
        export_apng_path,
        format="PNG",
        save_all=True,
        append_images=processed_images[1:],
        duration=frame_duration_ms,
        loop=0
    )

    # 3. Save preview GIF to 02_forge/
    forge_gif_path = os.path.join(forge_dir, f"{state_name}_preview.gif")
    processed_images[0].save(
        forge_gif_path,
        format="GIF",
        save_all=True,
        append_images=processed_images[1:],
        duration=frame_duration_ms,
        loop=0,
        transparency=0,
        disposal=2
    )

    elapsed = time.time() - v_t0
    print(f"  Completed {state_name} in {elapsed:.1f}s")
    return state_name

def main():
    base_dir = r"e:\Work2\AI_Work\tool\clawd-on-desk\pet-forge\work_space\R7_dashuiniu"
    raw_dir = os.path.join(base_dir, "01_raw_doubao")
    theme_assets_dir = os.path.join(base_dir, "theme", "assets")
    export_dir = os.path.join(base_dir, "03_export")
    forge_dir = os.path.join(base_dir, "02_forge")
    temp_frames_root = os.path.join(forge_dir, "temp_frames")

    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(theme_assets_dir, exist_ok=True)
    os.makedirs(export_dir, exist_ok=True)
    os.makedirs(forge_dir, exist_ok=True)

    output_dirs = (theme_assets_dir, export_dir, forge_dir, temp_frames_root)

    raw_files = sorted(glob.glob(os.path.join(raw_dir, "*.mp4")))
    if not raw_files:
        print(f"No .mp4 files found in {raw_dir}")
        return

    print(f"Found {len(raw_files)} videos in {raw_dir} to process.")

    session = new_session("isnet-anime")
    total_start = time.time()

    for idx, fpath in enumerate(raw_files):
        print(f"\n==========================================")
        print(f"Progress: [{idx + 1}/{len(raw_files)}]")
        process_state(fpath, session, output_dirs, fps=10)

    total_elapsed = time.time() - total_start
    print(f"\n==========================================")
    print(f"SUCCESS: All {len(raw_files)} animations processed in {total_elapsed / 60:.1f} minutes!")

if __name__ == "__main__":
    main()
