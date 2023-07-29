import tkinter as tk
import yt_dlp
import os
import ffmpeg
import subprocess
import threading  # For multithreading


class videoDownloader:
    def __init__(self, height, width, title):
        self.root = tk.Tk()
        self.isLossy = None
        self.isLossless = None
        self.isDownloading = False
        self.loop_times = 0
        self.height = height
        self.icon = "assets/icon.ico"
        tk.Tk.iconbitmap(self.root, default=self.icon)
        self.width = width
        self.title = title
        self.root.title("ClipTone")
        self.root.geometry(f"{self.height}x{self.width}")

        # Create a entry box
        self.entry_box = tk.Entry(self.root, background="#ebe694", font="Helvetica 12")
        self.entry_box.pack(pady=10)

        # Create a frame to hold the radio buttons and pack it to the top
        radio_frame = tk.Frame(self.root)
        radio_frame.pack(pady=10)

        # Radio button for selecting Lossy downloads
        dummy_radio_button = tk.Radiobutton(radio_frame, text="", value="dummy")
        dummy_radio_button.select()  # Select the dummy button by default
        self.lossyButton = tk.Radiobutton(
            radio_frame, text="Lossy", value=1, command=self.onLossySelect
        )
        self.lossyButton.pack(side=tk.LEFT, padx=5)  # Place on the left side

        # Radio button for selecting Lossless downloads.
        self.losslessButton = tk.Radiobutton(
            radio_frame, text="Lossless", value=2, command=self.onLosslessSelect
        )
        self.losslessButton.pack(side=tk.LEFT, padx=5)  # Place on the left side

        # Create a label
        self.label = tk.Label(
            self.root, text="Enter the video link to the audio you want to download"
        )
        self.label.pack(pady=10)
        self.open_button = tk.Button(
            text="View Downloaded Audio", command=self.open_directory
        )
        self.open_button.pack(pady=10)
        self.entry_box.bind("<Return>", self.on_enter_pressed)

        # Create a Exit Button

        self.exit_button = tk.Button(self.root, text="Exit", command=self.on_closing)
        self.exit_button.pack(pady=10)
        self.download_label = tk.Label(self.root, text="Ready to Download")
        self.download_label.pack(pady=10)

    def get_song(self):
        song = self.entry_box.get()
        return song

    def open_directory(self):
        home = os.path.expanduser("~")
        new_directory = os.path.join(home, "ffmpeg_downloads")
        subprocess.run(f"explorer {new_directory}")
        pass

    # NOTE:: 'event' paramerer is required for this function to work. The bind method returens an event object, which is passed to this function.

    def on_enter_pressed(self, event):
        self.isDownloading = True

        if self.isDownloading and self.loop_times == 0:
            if self.isLossy == True and self.isLossless == False:
                try:
                    self.download_label.config(text="Downloading... Please Wait")
                    threading.Thread(target=self.getLossyAudio).start()
                except yt_dlp.utils.DownloadError:
                    self.download_label.config(text="Download Failed, Link is Invalid")
                self.loop_times += 1
            elif self.isLossy == False and self.isLossless == True:
                try:
                    self.download_label.config(text="Downloading... Please Wait")
                    threading.Thread(target=self.getLosslessAudio).start()
                except yt_dlp.utils.DownloadError:
                    self.download_label.config(text="Download Failed, Link is Invalid")
                self.loop_times += 1
        elif self.isLossy == None and self.isLossless == None:
            self.label.config(text="Please select either Lossy or Lossless")

        else:
            return False

    def onLosslessSelect(self):
        self.isLossy = False
        self.isLossless = True
        pass

    def onLossySelect(self):
        self.isLossless = False
        self.isLossy = True
        pass

    def on_closing(self):
        if self.isDownloading:
            # If downloading is in progress, cancel closing and wait for the download to complete
            print("Cannot quit. Download in progress.")
        else:
            self.root.destroy()

    # def refresh(self):
    #     self.root.update()

    def getLossyAudio(self):
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
            self.loop_times = 0
            print("FFmpeg error:")
            print(e.stderr)

        if os.path.isfile(video_file_path):
            self.download_label.config(text="Download Complete")
        self.entry_box.delete(0, tk.END)
        self.download_label.config(
            text="Download Complete, Ready to Process another Video"
        )  # Update the label
        os.remove(video_file_path)
        self.isDownloading = False
        self.loop_times = 0
        return processed_Audio

    def getLosslessAudio(self):
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
        output_audio = os.path.join(new_directory, f"{videoTitle}.wav")
        processed_Audio = None

        try:
            ffmpeg.input(video_file_path).output(output_audio, ac="2", ar="44100").run()

        except ffmpeg._run.Error as e:
            self.loop_times = 0
            print("FFmpeg error:")
            print(e.stderr)

        if os.path.isfile(video_file_path):
            self.download_label.config(text="Download Complete")
        self.entry_box.delete(0, tk.END)
        self.download_label.config(
            text="Download Complete, Ready to Process another Video"
        )  # Update the label
        os.remove(video_file_path)
        self.isDownloading = False
        self.loop_times = 0
        return processed_Audio

    def run(self):
        try:
            tk.mainloop()
            self.isDownloading = False

        except tk.TclError:
            pass


app = videoDownloader(400, 270, "YouTube Downloader")
app.run()
