import os
import glob
import time
import subprocess
from PIL import Image
import numpy as np
from rembg import remove, new_session

def extract_frames_from_video(video_path, output_dir, step=2):
    os.makedirs(output_dir, exist_ok=True)
    for f in glob.glob(os.path.join(output_dir, "*.png")):
        try:
            os.remove(f)
        except:
            pass

    # Extract frames using ffmpeg at 24fps base, sampled by step=2 -> 12fps
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        os.path.join(output_dir, "frame_%03d.png")
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    all_frames = sorted(glob.glob(os.path.join(output_dir, "frame_*.png")))
    selected = all_frames[::step]
    return selected

def extract_frames_from_gif(gif_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for f in glob.glob(os.path.join(output_dir, "*.png")):
        try:
            os.remove(f)
        except:
            pass

    im = Image.open(gif_path)
    frames = []
    idx = 0
    try:
        while True:
            im.seek(idx)
            frame_path = os.path.join(output_dir, f"frame_{idx:03d}.png")
            im.convert("RGBA").save(frame_path)
            frames.append(frame_path)
            idx += 1
    except EOFError:
        pass
    return frames

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

    # Scan for both MP4 and GIF files
    raw_files = sorted(glob.glob(os.path.join(raw_dir, "*.mp4")) + glob.glob(os.path.join(raw_dir, "*.gif")))
    if not raw_files:
        print(f"No .mp4 or .gif files found in {raw_dir}")
        print("Please place the Doubao generated files in 01_raw_doubao/ first.")
        return

    print(f"Found {len(raw_files)} animation files in {raw_dir}")

    # Use isnet-anime or u2net
    session = new_session("isnet-anime")
    frame_duration_ms = int(1000 / 12)  # 12 FPS (~83ms)

    total_start = time.time()

    for v_idx, file_path in enumerate(raw_files):
        state_name = os.path.splitext(os.path.basename(file_path))[0]
        v_t0 = time.time()
        print(f"\n[{v_idx + 1}/{len(raw_files)}] Processing state: {state_name} ({file_path})")

        temp_dir = os.path.join(temp_frames_root, state_name)
        if file_path.lower().endswith(".mp4"):
            selected_frames = extract_frames_from_video(file_path, temp_dir, step=2)
        else:
            selected_frames = extract_frames_from_gif(file_path, temp_dir)

        print(f"  Extracted {len(selected_frames)} frames.")
        if not selected_frames:
            print(f"  Warning: No frames extracted for {file_path}, skipping.")
            continue

        processed_images = []
        for f_idx, fpath in enumerate(selected_frames):
            img = Image.open(fpath)
            nobg = remove(img, session=session)

            # Alpha noise thresholding
            arr = np.array(nobg)
            alpha = arr[:, :, 3]
            arr[alpha < 20, 3] = 0
            cleaned = Image.fromarray(arr)

            # Resize to standard 256x256 view
            resized = cleaned.resize((256, 256), Image.Resampling.LANCZOS)
            processed_images.append(resized)

            if (f_idx + 1) % 15 == 0 or (f_idx + 1) == len(selected_frames):
                print(f"  Processed {f_idx + 1}/{len(selected_frames)} frames ({time.time() - v_t0:.1f}s)...")

        # Save APNG to theme/assets/
        theme_apng_path = os.path.join(theme_assets_dir, f"{state_name}.apng")
        processed_images[0].save(
            theme_apng_path,
            format="PNG",
            save_all=True,
            append_images=processed_images[1:],
            duration=frame_duration_ms,
            loop=0
        )
        print(f"  Saved Theme APNG: {theme_apng_path} ({os.path.getsize(theme_apng_path) / 1024:.1f} KB)")

        # Save APNG to 03_export/
        export_apng_path = os.path.join(export_dir, f"{state_name}.apng")
        processed_images[0].save(
            export_apng_path,
            format="PNG",
            save_all=True,
            append_images=processed_images[1:],
            duration=frame_duration_ms,
            loop=0
        )

        # Save preview GIF to 02_forge/
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

        print(f"  Finished {state_name} in {time.time() - v_t0:.1f}s")

    print(f"\nAll {len(raw_files)} animations successfully processed in {time.time() - total_start:.1f}s!")

if __name__ == "__main__":
    main()
