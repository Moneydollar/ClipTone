import tkinter as tk
from tkinter import ttk as tkk
import yt_dlp
from os import path, remove
import ffmpeg
from subprocess import run
from threading import Thread  # For multithreading


# TODO: ADD STYlING TO THE GUI
class videoDownloader:
    def __init__(self, height, width, title):
        self.root = tk.Tk()
        self.isLossy = None
        self.isLossless = None
        self.isDownloading = False
        self.loop_times = 0
        self.height = height
        self.width = width
        self.title = title
        self.icon16 = tk.PhotoImage(file="assets/icon16.png")
        self.icon24 = tk.PhotoImage(file="assets/icon24.png")
        self.icon32 = tk.PhotoImage(file="assets/icon32.png")
        self.root.iconphoto(False, self.icon24, self.icon32)
        tk.Tk.iconbitmap(self.root, default="assets/icon64.ico")
        self.root.configure(background="#f3f3f3")
        self.root.title("ClipTone")
        self.root.geometry(f"{self.height}x{self.width}")

        # Create a entry box
        self.entry_box = tk.Entry(self.root, background="#ebe694", font="Helvetica 12")
        self.entry_box.pack(pady=10)
        # Create a context menu for the entry box
        self.entry_context_menu = tk.Menu(self.root, tearoff=0)
        self.entry_context_menu.add_command(label="Cut", command=self.cut_text)
        self.entry_context_menu.add_command(label="Copy", command=self.copy_text)
        self.entry_context_menu.add_command(label="Paste", command=self.paste_text)

        # Bind the context menu to the entry box
        self.entry_box.bind("<Button-3>", self.show_entry_context_menu)

        # ... existing code ...

        # Create a frame to hold the radio buttons and pack it to the top
        radio_frame = tk.Frame(self.root)
        radio_frame.pack(pady=10)
        radio_frame.configure(background="#f3f3f3")

        # Radio button for selecting Lossy downloads
        dummy_radio_button = tk.Radiobutton(radio_frame, text="", value="dummy")
        dummy_radio_button.select()  # Select the dummy button by default
        self.lossyButton = tk.Radiobutton(
            radio_frame, text="Lossy", value=1, command=self.onLossySelect
        )
        self.lossyButton.pack(side=tk.LEFT, padx=5)  # Place on the left side
        self.lossyButton.configure(background="#f3f3f3")

        # Radio button for selecting Lossless downloads.
        self.losslessButton = tk.Radiobutton(
            radio_frame, text="Lossless", value=2, command=self.onLosslessSelect
        )
        self.losslessButton.pack(
            side=tk.LEFT, padx=5
        )  # Place on the left side on previous button
        self.losslessButton.configure(background="#f3f3f3")

        # Create a label
        self.label = tk.Label(
            self.root, text="Enter the video link to the audio you want to download"
        )
        self.label.pack(pady=10)
        self.label.configure(background="#f3f3f3")
        self.open_button = tk.Button(
            text="View Downloaded Audio", command=self.open_directory
        )
        self.open_button.pack(pady=10)
        self.entry_box.bind("<Return>", self.on_enter_pressed)

        # Create a Exit Button

        # self.exit_button = tk.Button(self.root, text="Exit", command=self.on_closing)
        # self.exit_button.pack(pady=10)

        downloadProgressFrame = tk.Frame(self.root, width=300)
        downloadProgressFrame.configure(background="#f3f3f3")
        downloadProgressFrame.pack(pady=15, padx=10)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = tkk.Progressbar(
            downloadProgressFrame,
            mode="determinate",
            variable=self.progress_var,
            style="TProgressbar",
        )

        self.progress_bar.pack(
            fill=tk.X,
            padx=10,
            pady=5,
        )
        self.download_label = tk.Label(downloadProgressFrame, text="Ready to Download")
        self.download_label.configure(background="#f3f3f3")
        self.download_label.pack(pady=10)

    def show_entry_context_menu(self, event):
        try:
            self.entry_context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.entry_context_menu.grab_release()

    def cut_text(self):
        self.entry_box.event_generate("<<Cut>>")

    def copy_text(self):
        self.entry_box.event_generate("<<Copy>>")

    def paste_text(self):
        self.entry_box.event_generate("<<Paste>>")

    def get_song(self):
        song = self.entry_box.get()
        return song

    def open_directory(self):
        home = path.expanduser("~")
        new_directory = path.join(home, "ffmpeg_downloads")
        run(f"explorer {new_directory}")
        pass

    # NOTE:: 'event' paramerer is required for this function to work. The bind method returens an event object, which is passed to this function.

    def on_enter_pressed(self, event):
        self.isDownloading = True

        if self.isDownloading and self.loop_times == 0:
            if self.isLossy == True and self.isLossless == False:
                try:
                    self.download_label.configure(text="Downloading... Please Wait")
                    Thread(target=self.getLossyAudio).start()
                except yt_dlp.utils.DownloadError:
                    self.download_label.configure(
                        text="Download Failed, Link is Invalid"
                    )
                self.loop_times += 1
            elif self.isLossy == False and self.isLossless == True:
                try:
                    self.download_label.configure(text="Downloading... Please Wait")
                    Thread(target=self.getLosslessAudio).start()
                except yt_dlp.utils.DownloadError:
                    self.download_label.configure(
                        text="Download Failed, Link is Invalid"
                    )
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

    def update_progress_bar(self, data):
        if data["status"] == "downloading":
            total_bytes = data.get("total_bytes")
            downloaded_bytes = data.get("downloaded_bytes")
            if total_bytes and downloaded_bytes:
                progress = downloaded_bytes / total_bytes * 100.0
                self.progress_var.set(progress)

    def on_closing(self):
        if self.isDownloading:
            # If downloading is in progress, cancel closing and wait for the download to complete
            print("Cannot quit. Download in progress.")
        else:
            self.root.destroy()

    # def refresh(self):
    #     self.root.update()

    def getLossyAudio(self):
        home = path.expanduser("~")
        new_directory = path.join(home, "ffmpeg_downloads")
        ydl_opts = {"outtmpl": path.join(new_directory, "%(title)s.%(ext)s")}
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        videoLink = self.get_song()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.add_progress_hook(
                self.update_progress_bar
            )  # Register the progress hook
            ydl.download([videoLink])

        videoInfo = ydl.extract_info(videoLink, download=False)
        videoTitle = videoInfo.get("title")
        videoTitle = videoTitle.replace("/", "\\")
        videoExt = videoInfo.get("ext")

        video_file_path = path.join(new_directory, f"{videoTitle}.{videoExt}")
        output_audio = path.join(new_directory, f"{videoTitle}.mp3")
        processed_Audio = None

        try:
            ffmpeg.input(video_file_path).output(
                output_audio, codec="mp3", ac="2", ar="44100"
            ).run()
        except ffmpeg._run.Error as e:
            self.loop_times = 0
            print("FFmpeg error:")
            print(e.stderr)

        if path.isfile(video_file_path):
            self.download_label.config(text="Download Complete")
        self.entry_box.delete(0, tk.END)
        self.download_label.config(
            text="Download Complete, Ready to Process another Video"
        )  # Update the label
        remove(video_file_path)
        self.isDownloading = False
        self.loop_times = 0
        self.progress_var.set(0)
        return processed_Audio

    def getLosslessAudio(self):
        home = path.expanduser("~")
        new_directory = path.join(home, "ffmpeg_downloads")
        ydl_opts = {"outtmpl": path.join(new_directory, "%(title)s.%(ext)s")}
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        videoLink = self.get_song()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.add_progress_hook(
                self.update_progress_bar
            )  # Register the progress hook
            ydl.download([videoLink])

        videoInfo = ydl.extract_info(videoLink, download=False)
        videoTitle = videoInfo.get("title")
        videoTitle = videoTitle.replace("/", "\\")
        videoExt = videoInfo.get("ext")

        video_file_path = path.join(new_directory, f"{videoTitle}.{videoExt}")
        output_audio = path.join(new_directory, f"{videoTitle}.wav")
        processed_Audio = None

        try:
            ffmpeg.input(video_file_path).output(output_audio, ac="2", ar="44100").run()

        except ffmpeg._run.Error as e:
            self.loop_times = 0
            print("FFmpeg error:")
            print(e.stderr)

        if path.isfile(video_file_path):
            self.download_label.config(text="Download Complete")
        self.entry_box.delete(0, tk.END)
        self.download_label.config(
            text="Download Complete, Ready to Process another Video"
        )  # Update the label
        remove(video_file_path)
        self.isDownloading = False
        self.loop_times = 0
        self.progress_var.set(0)
        return processed_Audio

    def run(self):
        try:
            tk.mainloop()
            self.isDownloading = False

        except tk.TclError:
            pass


app = videoDownloader(400, 270, "YouTube Downloader")
app.run()
