import tkinter as tk
import yt_dlp
import os
import ffmpeg
import threading  # For multithreading


class videoDownloader:
    def __init__(self, height, width, title):
        self.root = tk.Tk()
        self.isDownloading = False
        self.height = height
        self.icon = "assets/icon.ico"
        tk.Tk.iconbitmap(self.root, default=self.icon)
        self.width = width
        self.title = title
        self.root.title("Video to Audio Downloader")
        self.root.geometry(f"{self.height}x{self.width}")
        # Create a entry box
        self.entry_box = tk.Entry(self.root, background="#ebe694", font="Helvetica 12")
        self.entry_box.pack(pady=10)

        # Create a label
        self.label = tk.Label(
            self.root, text="Enter the video link to the audio you want to download"
        )
        self.label.pack(pady=10)
        self.entry_box.bind("<Return>", self.on_enter_pressed)

        # Create a Exit Button

        self.exit_button = tk.Button(self.root, text="Exit", command=self.on_closing)
        self.exit_button.pack(pady=10)

    def get_song(self):
        try:
            song = self.entry_box.get()
            return song
        except Exception:
            song = "Invalid Link, Please Try Again"
        song = self.entry_box.get()
        return song

    def on_enter_pressed(self, event):
        self.isDownloading = True
        song = self.entry_box.get()
        if self.isDownloading:
            self.download_label = tk.Label(self.root)
            self.download_label.config(text="Downloading... Please Wait")
            self.download_label.pack(pady=10)
            threading.Thread(target=self.get_audio).start()

    # def refresh(self):
    #     self.root.update()

    def get_audio(self):
        home = os.path.expanduser("~")
        new_directory = os.path.join(home, "ffmpeg_downloads")
        ydl_opts = {"outtmpl": os.path.join(new_directory, "%(title)s.%(ext)s")}
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        videoLink = self.get_song()
        ydl.download(
            [videoLink]
        )  # Download the video directly, no need to store the result

        videoInfo = ydl.extract_info(videoLink, download=False)
        videoTitle = videoInfo.get("title")
        videoTitle = videoTitle.replace("/", "\\")
        videoExt = videoInfo.get("ext")

        video_file_path = os.path.join(new_directory, f"{videoTitle}.{videoExt}")
        output_audio = os.path.join(new_directory, f"{videoTitle}.mp3")
        processed_Audio = None

        try:
            ffmpeg.input(video_file_path).output(
                output_audio, codec="mp3", ac="2", ar="44100"
            ).run()
        except ffmpeg._run.Error as e:
            print("FFmpeg error:")
            print(e.stderr)

        if os.path.isfile(video_file_path):
            self.download_label.config(text="Download Complete")
        self.entry_box.delete(0, tk.END)
        self.download_label.pack_forget()
        os.remove(video_file_path)
        self.isDownloading = False
        return processed_Audio

    def run(self):
        try:
            tk.mainloop()
            self.isDownloading = False

        except tk.TclError:
            pass

    def on_closing(self):
        if self.isDownloading:
            # If downloading is in progress, cancel closing and wait for the download to complete
            print("Cannot quit. Download in progress.")
        else:
            self.root.destroy()


# root.mainloop()
app = videoDownloader(400, 170, "YouTube Downloader")
app.run()
