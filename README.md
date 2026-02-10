https://huggingface.co/spaces/pavellakov/video-compressor

# 🎬 Video Compressor (ffmpeg + Gradio)

This project is a **simple video compression tool** built with [Gradio](https://gradio.app) for the user interface and [FFmpeg](https://ffmpeg.org/) for the actual compression.  
It allows you to upload a video, set the **CRF (Constant Rate Factor)** value for compression quality, and download the compressed video.  
A real-time progress bar shows the compression progress.

---

## 🚀 Features
- Upload common video formats: `.mp4`, `.avi`, `.mov`, `.mkv`
- Compress videos using **H.265 (HEVC)** codec (`libx265`)
- Adjust **CRF** (23 = high quality, 32 = lower quality but smaller file size)
- Real-time progress updates during compression
- Automatic file size comparison after compression
- Download compressed video directly
- Built with **Gradio UI** → lightweight and easy to run

---

## 🛠 Requirements

- Python 3.9+ recommended
- Install dependencies:
  ```bash
  pip install gradio
  ```

- Install **FFmpeg** (required for video compression).  
  - On macOS (Homebrew):  
    ```bash
    brew install ffmpeg
    ```
  - On Ubuntu/Debian:  
    ```bash
    sudo apt update && sudo apt install ffmpeg
    ```
  - On Windows: [Download FFmpeg](https://ffmpeg.org/download.html) and add it to your PATH.

---

## 📂 Project Structure

```
video-compressor/
│── app.py            # Main Python script (the Gradio app)
│── README.md         # Documentation
```

---

## ▶️ Usage

Run the app locally with:

```bash
python app.py
```

Then open your browser at: [http://127.0.0.1:7860](http://127.0.0.1:7860)

1. **Upload a video file**  
2. **Choose compression level (CRF)**  
   - Lower CRF = higher quality, larger file size  
   - Higher CRF = lower quality, smaller file size  
   - Default: 28 (balanced)  
3. **Click "Compress Video"**  
4. Wait for the **progress bar** to reach 100%  
5. **Download your compressed video**

---

## ⚙️ How It Works

1. The app calls **`ffprobe`** to read the video duration.  
2. It runs **`ffmpeg`** with `libx265` codec and user-specified CRF.  
3. While running, stderr output from ffmpeg is parsed (`time=HH:MM:SS.xx`) to update progress.  
4. After finishing, the app calculates:  
   - Original size (MB)  
   - New size (MB)  
   - Reduction percentage  
5. Displays results + download link for the compressed file.

---

## 📊 Example Results

- Original: 100 MB  
- Compressed: 35 MB  
- Reduced by: **65%** 🎉  

---

## 🧩 Code Highlights

- **Helper functions** keep the code clean:  
  - `get_video_duration()` → fetch video length with ffprobe  
  - `build_ffmpeg_command()` → builds ffmpeg CLI command  
  - `summarize_compression()` → calculates file size reduction  
- **Unified exception handling** with `safe_none_on_error()`  
- **Progress tracking** uses regex on ffmpeg stderr

---

## 🔮 Future Improvements

- Option to **downscale resolution** (1080p → 720p, 480p)  
- Add support for different codecs (VP9, AV1)  
- Cloud deployment with Hugging Face Spaces or Docker  

---

## 📜 License

MIT License. Free to use and modify.  

---

## 👨‍💻 Author

Developed by **Pavel Lakov**  
🔗 [GitHub](https://github.com/PavelLakov)

