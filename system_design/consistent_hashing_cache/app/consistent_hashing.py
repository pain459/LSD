import tkinter as tk
from tkinter import ttk, messagebox
import time

class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("400x250")
        
        self.time_left = 0
        self.running = False

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10)
        style.configure("TLabel", font=("Helvetica", 48))

        self.label = ttk.Label(root, text="00:00:00", style="TLabel")
        self.label.pack(pady=20)

        self.entry = ttk.Entry(root, width=10, font=("Helvetica", 18), justify="center")
        self.entry.pack(pady=10)
        self.entry.insert(0, "60")  # default 60 seconds

        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(pady=10)

        self.start_button = ttk.Button(self.button_frame, text="Start", command=self.start)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = ttk.Button(self.button_frame, text="Pause", command=self.pause)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        self.reset_button = ttk.Button(self.button_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=2, padx=5, pady=5)

    def start(self):
        if not self.running:
            try:
                self.time_left = int(self.entry.get())
                self.entry.config(state=tk.DISABLED)
                self.running = True
                self.update_timer()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def pause(self):
        if self.running:
            self.running = False
            self.entry.config(state=tk.NORMAL)

    def reset(self):
        self.running = False
        self.time_left = 0
        self.label.config(text="00:00:00")
        self.entry.config(state=tk.NORMAL)

    def update_timer(self):
        if self.running:
            if self.time_left > 0:
                self.label.config(text=self.format_time(self.time_left))
                self.time_left -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.running = False
                messagebox.showinfo("Time's up", "The countdown has finished!")
                self.entry.config(state=tk.NORMAL)

    def format_time(self, seconds):
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02}"

if __name__ == "__main__":
    root = tk.Tk()
    timer = CountdownTimer(root)
    root.mainloop()
