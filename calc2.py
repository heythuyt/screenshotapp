import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import datetime
from PIL import Image, ImageTk, ImageOps
import os


class ScreenshotViewer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screenshot Viewer")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
        self.root.bind("<Left>", self.show_previous_screenshot)
        self.root.bind("<Right>", self.show_next_screenshot)
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        self.root.bind("<MouseWheel>", self.zoom)
        

        self.screenshots = []
        self.current_screenshot_index = 0

        self.image_frame = tk.Frame(self.root, bg="white")
        self.image_frame.pack(expand=True, fill=tk.BOTH)

        self.screenshot_label = tk.Label(self.image_frame, bg="white")
        self.screenshot_label.pack(expand=True, fill=tk.BOTH)

        self.button_frame = tk.Frame(self.image_frame, bg="white")
        self.button_frame.place(relx=0, rely=0, anchor="nw")

        choose_dir_button = tk.Button(self.button_frame, text="Choose Directory", command=self.load_screenshots)
        choose_dir_button.pack(side=tk.LEFT, padx=5)

        screenshot_button = tk.Button(self.button_frame, text="Take Screenshot", command=self.take_screenshot)
        screenshot_button.pack(side=tk.LEFT, padx=5)

        self.zoom_in_button = tk.Button(self.button_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=5)

        self.zoom_out_button = tk.Button(self.button_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=5)

        self.zoom_level = 1.0

        self.root.mainloop()

    def load_screenshots(self):
        screenshots_dir = filedialog.askdirectory(title="Select Screenshots Directory")
        if screenshots_dir:
            self.screenshots = [
                os.path.join(screenshots_dir, file)
                for file in os.listdir(screenshots_dir)
                if file.endswith(".png")
            ]
            if not self.screenshots:
                messagebox.showinfo("No Screenshots", "No screenshots found in the selected directory.")
            else:
                self.current_screenshot_index = 0
                self.show_screenshot()

    def show_screenshot(self):
        if self.screenshots:
            image = Image.open(self.screenshots[self.current_screenshot_index])
            self.resize_image(image)
            tk_image = ImageTk.PhotoImage(image)
            self.screenshot_label.config(image=tk_image)
            self.screenshot_label.image = tk_image

    def show_previous_screenshot(self, event=None):
        if self.screenshots:
            self.current_screenshot_index = (
                self.current_screenshot_index - 1
            ) % len(self.screenshots)
            self.show_screenshot()

    def show_next_screenshot(self, event=None):
        if self.screenshots:
            self.current_screenshot_index = (
                self.current_screenshot_index + 1
            ) % len(self.screenshots)
            self.show_screenshot()

    def toggle_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))
        self.show_screenshot()

    def exit_fullscreen(self, event=None):
        self.root.attributes("-fullscreen", False)
        self.root.geometry("800x600")
        self.show_screenshot()

    def zoom_in(self):
        self.zoom_level *= 1.1
        self.update_zoomed_image()

    def zoom_out(self):
        self.zoom_level /= 1.1
        self.update_zoomed_image()

    def update_zoomed_image(self):
        if self.screenshots:
            image = Image.open(self.screenshots[self.current_screenshot_index])
            width, height = image.size
            scaled_width = int(width * self.zoom_level)
            scaled_height = int(height * self.zoom_level)
            image = image.resize((scaled_width, scaled_height), Image.LANCZOS)
            tk_image = ImageTk.PhotoImage(image)
            self.screenshot_label.config(image=tk_image)
            self.screenshot_label.image = tk_image

    def resize_image(self, image):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        image = image.resize((screen_width, screen_height), Image.LANCZOS)
        return image

    def take_screenshot(self):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        screenshot = pyautogui.screenshot()
        if self.screenshots:
            screenshots_dir = os.path.dirname(self.screenshots[0])
        else:
            screenshots_dir = filedialog.askdirectory(title="Select Directory to Save Screenshots")
        if screenshots_dir:
            screenshot_path = os.path.join(screenshots_dir, f"screenshot_{timestamp}.png")
            screenshot.save(screenshot_path)
            self.screenshots.append(screenshot_path)
            self.current_screenshot_index = len(self.screenshots) - 1
            self.show_screenshot()

    def zoom(self, event):
        if event.delta > 0:
            self.zoom_in()
        else:
            self.zoom_out()


ScreenshotViewer()
