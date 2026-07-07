import tkinter as tk
from datetime import datetime, timedelta
from network_final import GitCommitEngine

# --- CONFIGURATION ---
# ⛔️ Change the place holder, Please !!
GITHUB_USERNAME = "<Enter your own GitHub UserName>"
REFRESH_DELAY = 600000 # 10 minutes
WIDGET_POSITION = "180x100+1200+60"

class GitDesktopWidget:
    def __init__(self):
        # Instantiate the brains
        self.engine = GitCommitEngine(username=GITHUB_USERNAME)

        self.root = tk.Tk()

        # UI Setup (macOS Frameless)
        self.root.overrideredirect(True)
        self.root.geometry(WIDGET_POSITION)
        self.root.configure(bg='#1c1c1e')
        self.root.wm_attributes("-topmost", True)

        # UI Elements
        self.title_label = tk.Label(self.root, text="30-DAY COMMITS", font=("Helvetica", 10, "bold"), fg="#8e8e93", bg="#1c1c1e")
        self.title_label.pack(pady=(12, 0))

        self.count_label = tk.Label(self.root, text="--", font=("Helvetica", 36, "bold"), fg="#ff9f0a", bg="#1c1c1e")
        self.count_label.pack()

        self.sub_label = tk.Label(self.root, text="synchronizing...", font=("Helvetica", 11), fg="#ffffff", bg="#1c1c1e")
        self.sub_label.pack(pady=(0, 10))

        # Start the loop
        self.update_data()
        self.root.mainloop()

    def update_data(self):
        """Asks the engine for data, then updates the UI pixels."""
        result = self.engine.fetch_30_day_commits()

        if result["error"] == "offline":
            self.count_label.config(text="--", fg="#ff453a")
            self.sub_label.config(text="offline")
        else:
            count = result["count"]
            self.count_label.config(text=str(count))
            self.sub_label.config(text=f"since {(datetime.now() - timedelta(days=30)).strftime('%b %d')}")

            if count > 0:
                self.count_label.config(fg="#30d158")
            else:
                self.count_label.config(fg="#ff9f0a")

        self.root.after(REFRESH_DELAY, self.update_data)

if __name__ == "__main__":
    GitDesktopWidget()