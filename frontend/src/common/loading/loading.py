import customtkinter as ctk
import tkinter as tk
import threading
from PIL import Image
import time

class LoadingFrame(ctk.CTkFrame):
    def __init__(self, master, fg_color, image_path = "assets/images/loading.gif", size = (100,100), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.fg_color = fg_color
        self.size = size
        self.loading_image_path = image_path
        self.create_widgets()

    def create_widgets(self):
        self.loading_label = ctk.CTkLabel(self, fg_color=None, text='')
        self.loading_label.pack(expand=True, fill='both')

        self.gif_frames = self._get_frames(self.loading_image_path)
        self._play_gif(self.loading_label, self.gif_frames)

    def _get_frames(self, img):
        with Image.open(img) as gif:
            index = 0
            frames = []

            while True:
                try:
                    gif.seek(index)
                    frame = gif.convert('RGBA')
                    background = Image.new('RGBA', frame.size, self.fg_color)
                    combined_frame = Image.alpha_composite(background, frame)
                    ctk_frame = ctk.CTkImage(combined_frame, size=self.size)
                    frames.append(ctk_frame)
                except EOFError:
                    break
                except Exception as e:
                    print(f"Error processing frame {index}: {e}")
                    break
                index += 1

            return frames

    def _play_gif(self, label, frames):

        total_delay = 50
        delay_frames = 25 # delay between frames

        for frame in frames:
            self.master.after(total_delay, self._next_frame, frame, label)
            total_delay += delay_frames
        self.master.after(total_delay, self._next_frame, frames, label, True)

    def _next_frame(self, frame, label, restart=False):
        if restart:
            try:
                label.configure()
            except:
                return
            self.after(1, self._play_gif, label, frame)
            return

        try:
            label.configure(image=frame)
        except tk.TclError:
            return

if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Loading Frame")
    app.geometry("500x500")
    app.configure()

    loading_frame = LoadingFrame(app, fg_color='#222B36')
    loading_frame.pack()

    app.mainloop()