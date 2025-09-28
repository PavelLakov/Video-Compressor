import subprocess
import os
import re
import gradio as gr


def safe_none_on_error(_msg="error"):
    """Helper for unified exception handling (returns None)."""
    return None


def get_video_duration(input_path):
    try:
        result = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", input_path
        ]).decode().strip()
        return float(result)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return safe_none_on_error("ffprobe error")


def build_ffmpeg_command(input_path, output_path, crf_value):
    return [
        "ffmpeg", "-y", "-i", input_path,
        "-c:v", "libx265", "-crf", str(int(crf_value)),
        "-c:a", "aac", output_path
    ]


def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)


def summarize_compression(input_path, output_path):
    """Return human-readable stats after compression."""
    orig_size = get_file_size_mb(input_path)
    new_size = get_file_size_mb(output_path)
    reduction = (1 - new_size / orig_size) * 100 if orig_size > 0 else 0

    msg = (f"Compression complete!\n"
           f"Original: {orig_size:.1f} MB\n"
           f"New: {new_size:.1f} MB\n"
           f"Reduced by: {reduction:.1f}%")
    return msg


def compress_video(input_file_path, crf_value, progress=gr.Progress()):
    if input_file_path is not None:
        input_path = input_file_path.name
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_compressed{ext}"

        duration = get_video_duration(input_path)
        if duration is None:
            return None, "Could not determine video duration. Ensure ffprobe is installed."

        cmd = build_ffmpeg_command(input_path, output_path, crf_value)

        process = subprocess.Popen(
            cmd, stderr=subprocess.PIPE, universal_newlines=True
        )

        time_pattern = re.compile(r"time=(\d+):(\d+):(\d+)\.?\d*")

        for line in iter(process.stderr.readline, ""):
            match = time_pattern.search(line)
            if match and duration > 0:
                h, m, s = map(int, match.groups())
                current_time = h * 3600 + m * 60 + s
                percent = min(int((current_time / duration) * 100), 100)
                progress(percent / 100, desc=f"Compressing... {percent}%")

        process.wait()

        if process.returncode != 0:
            return None, "Compression failed. Ensure ffmpeg is installed."

        try:
            msg = summarize_compression(input_path, output_path)
            return output_path, msg
        except (FileNotFoundError, OSError):
            return None, "Compression finished but error getting file size."

    return None, "No input file provided."


with gr.Blocks(title="Video Compressor") as demo:
    gr.Markdown("# 🎬 Video Compressor (ffmpeg + Gradio)")
    gr.Markdown("Upload a video, choose compression level (CRF), and download the smaller file.")

    with gr.Row():
        with gr.Column():
            input_file_ui = gr.File(label="Upload Video", file_types=[".mp4", ".avi", ".mov", ".mkv"])
            crf_slider = gr.Slider(23, 32, value=28, step=1, label="Compression Level (CRF)")
            compress_btn = gr.Button("Compress Video")
        with gr.Column():
            output_file = gr.File(label="Download Compressed Video")
            status_box = gr.Textbox(label="Status / Log")

    compress_btn.click(
        fn=compress_video,
        inputs=[input_file_ui, crf_slider],
        outputs=[output_file, status_box]
    )

if __name__ == "__main__":
    demo.launch(share=True)
