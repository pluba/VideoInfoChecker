import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import cv2
import os

def toggle_fullscreen(event=None):
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

def get_video_info():
    filename = filedialog.askopenfilename(title="Select a video file", filetypes=[("Video files", "*.mp4;*.mov;*.mkv;*.avi;*.flv;*.webm")])
    if filename:
        cap = cv2.VideoCapture(filename)
        if not cap.isOpened():
            print("Error: Unable to open video file.")
            return

        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
        duration_seconds = num_frames / frame_rate
        duration_hours = int(duration_seconds / 3600)
        duration_minutes = int((duration_seconds % 3600) / 60)
        duration_seconds = int(duration_seconds % 60)
        resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        codec = cap.get(cv2.CAP_PROP_FOURCC)
        codec_str = decode_fourcc(codec)
        file_size = os.path.getsize(filename) / (1024 * 1024)  # Convert bytes to megabytes

        format_str = os.path.splitext(filename)[1].replace(".", "").upper()
        file_name = os.path.basename(filename)

        duration_str = ""
        if duration_hours > 0:
            duration_str += f"{duration_hours} hour{'s' if duration_hours > 1 else ''}"
        if duration_minutes > 0:
            duration_str += f" {duration_minutes} minute{'s' if duration_minutes > 1 else ''}"
        if duration_seconds > 0 or (duration_hours == 0 and duration_minutes == 0):
            duration_str += f" {duration_seconds} second{'s' if duration_seconds > 1 else ''}"

        info_label.config(text=f"Format: {format_str}\nFrames: {num_frames}\nFPS: {frame_rate}\nResolution: {resolution[0]}x{resolution[1]}\nDuration: {duration_str}\nFile Size: {file_size:.2f} MB\nCodec: {codec_str}")
        file_label.config(text=file_name, font=("Helvetica", 20, "bold"))

        cap.release()
        info_button.config(text="Next Video", state=tk.NORMAL)

def decode_fourcc(fourcc):
    fourcc = int(fourcc)
    return "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])

root = tk.Tk()
root.title("Video Info")
root.configure(bg="#2e73db")

# Remove the default icon
root.iconbitmap(default=None)

# Start the application in maximized screen
root.state("zoomed")

# Bind F11 to toggle fullscreen
root.bind("<F11>", toggle_fullscreen)

# Define a custom button style
style = ttk.Style()
style.configure('RoundedButton.TButton', background='#2e73db', foreground='#000000', borderwidth=0, relief="flat", font=("Helvetica", 12, "bold"))

info_frame = tk.Frame(root, bg="#2e73db")
info_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

file_label = tk.Label(info_frame, text="", bg="#2e73db", fg="#ffffff", font=("Helvetica", 20, "bold"))
file_label.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.CENTER)

info_label = tk.Label(info_frame, text="", justify=tk.CENTER, bg="#2e73db", fg="#ffffff", font=("Helvetica", 12, "bold"))
info_label.pack(side=tk.TOP, padx=20, pady=10, anchor=tk.CENTER)

# Create a button using the custom style
info_button = ttk.Button(info_frame, text="Video Info", style='RoundedButton.TButton', command=get_video_info)
info_button.pack(side=tk.BOTTOM, pady=20)

root.mainloop()
