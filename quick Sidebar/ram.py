import tkinter as tk
import psutil
import os
import subprocess
import win32com.client

class SidebarApp:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.config(bg='pink')
        self.root.wm_attributes("-transparentcolor", 'pink')

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.sidebar_width = 300
        self.sidebar_open = False
        self.sidebar = None

        self.recent_labels = []
        self.memory_widgets = []

        self.root.geometry(f"60x60+{self.screen_width - 70}+{self.screen_height // 2 - 30}")
        self.canvas = tk.Canvas(self.root, width=60, height=60, highlightthickness=0, bg='pink')
        self.canvas.pack()
        self.canvas.create_oval(5, 5, 55, 55, fill='gray60', outline='gray')
        self.canvas.bind("<Button-1>", self.toggle_sidebar)

    def toggle_sidebar(self, event=None):
        if self.sidebar_open:
            self.animate_close()
        else:
            self.create_sidebar()
            self.animate_open()

    def create_sidebar(self):
        self.sidebar = tk.Toplevel()
        self.sidebar.overrideredirect(True)
        self.sidebar.geometry(f"{self.sidebar_width}x{self.screen_height}+{self.screen_width}+0")
        self.sidebar.configure(bg='#2b2b2b')
        self.sidebar.wm_attributes("-topmost", True)
        self.sidebar.wm_attributes("-alpha", 0.7)

        self.sidebar_canvas = tk.Canvas(self.sidebar, width=self.sidebar_width, height=self.screen_height,
                                        bg='#2b2b2b', highlightthickness=0)
        self.sidebar_canvas.pack(fill="both", expand=True)

        close_btn = tk.Button(self.sidebar_canvas, text="→", font=("Arial", 12, "bold"),
                              bg="gray20", fg="white", command=self.animate_close,
                              bd=0, relief="flat", cursor="hand2")
        close_btn.place(x=self.sidebar_width - 40, y=10, width=30, height=30)

        ram_label = tk.Label(self.sidebar_canvas, text="RAM Usage", bg='#2b2b2b', fg='white', font=('Arial', 12))
        ram_label.place(x=20, y=60)

        ram_percent = psutil.virtual_memory().percent
        ram_bar = tk.Canvas(self.sidebar_canvas, width=260, height=20, bg='gray25', bd=0, highlightthickness=0)
        ram_bar.place(x=20, y=90)
        ram_bar.create_rectangle(0, 0, ram_percent * 2.6, 20, fill='lime')

        ram_text = tk.Label(self.sidebar_canvas, text=f"{ram_percent:.1f}% used", bg='#2b2b2b', fg='white')
        ram_text.place(x=20, y=115)

        self.update_recent_items()
        self.schedule_recent_update()

    def update_recent_items(self):
        for label in self.recent_labels:
            label.destroy()
        self.recent_labels.clear()

        items = self.get_recent_items(limit=30)
        images, docs, dirs = [], [], []

        for path in items:
            if os.path.isdir(path):
                dirs.append(path)
            else:
                ext = os.path.splitext(path)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                    images.append(path)
                elif ext in ['.pdf', '.docx', '.xlsx', '.txt', '.py', '.js', '.cpp', '.c', '.html', '.css']:
                    docs.append(path)

        y = 150
        def section(title, files):
            nonlocal y
            if files:
                lbl = tk.Label(self.sidebar_canvas, text=title, bg='#2b2b2b', fg='lightblue',
                               font=('Arial', 10, 'bold'))
                lbl.place(x=20, y=y)
                self.recent_labels.append(lbl)
                y += 25
                for file in files[:5]:
                    name = os.path.basename(file)
                    l = tk.Label(self.sidebar_canvas, text=name[:35], bg='#2b2b2b',
                                 fg='white', anchor='w', font=('Arial', 9), cursor="hand2")
                    l.place(x=30, y=y)
                    l.bind("<Button-1>", lambda e, p=file: self.open_file(p))
                    self.recent_labels.append(l)
                    y += 22
                y += 10

        section("🖼️ Images", images)
        section("📄 Files", docs)
        section("🗂️ Apps / Folders", dirs)

        self.memory_start_y = y + 20
        self.display_memory_details()

    def schedule_recent_update(self):
        if self.sidebar_open:
            self.update_recent_items()
            self.sidebar.after(10000, self.schedule_recent_update)

    def display_memory_details(self):
        vm = psutil.virtual_memory()
        swap = psutil.swap_memory()

        cached = getattr(vm, 'cached', vm.available) / (1024 ** 3)
        paged_pool = swap.used / (1024 ** 3)
        non_paged_pool = getattr(vm, 'shared', vm.used) / (1024 ** 3)

        for w in self.memory_widgets:
            w.destroy()
        self.memory_widgets = []

        y = self.memory_start_y
        header = tk.Label(self.sidebar_canvas, text="📊 Memory Info", bg='#2b2b2b',
                          fg='orange', font=("Arial", 12, "bold"))
        header.place(x=20, y=y)
        self.memory_widgets.append(header)
        y += 30

        def mem_row(label, value):
            nonlocal y
            text = f"{label}: {value:.2f} GB"
            lbl = tk.Label(self.sidebar_canvas, text=text, bg='#2b2b2b', fg='lightgreen',
                           font=("Arial", 10, 'bold'))
            lbl.place(x=30, y=y)
            self.memory_widgets.append(lbl)
            y += 25

        mem_row("Cached Memory", cached)
        mem_row("Paged Pool", paged_pool)
        mem_row("Non-Paged Pool", non_paged_pool)

    def animate_open(self):
        def slide():
            x = self.sidebar.winfo_x()
            if x > self.screen_width - self.sidebar_width:
                x -= 20
                self.sidebar.geometry(f"{self.sidebar_width}x{self.screen_height}+{x}+0")
                self.sidebar.after(10, slide)
            else:
                self.sidebar.geometry(f"{self.sidebar_width}x{self.screen_height}+{self.screen_width - self.sidebar_width}+0")
                self.sidebar_open = True
                self.schedule_recent_update()
        slide()

    def animate_close(self):
        def slide():
            x = self.sidebar.winfo_x()
            if x < self.screen_width:
                x += 20
                self.sidebar.geometry(f"{self.sidebar_width}x{self.screen_height}+{x}+0")
                self.sidebar.after(10, slide)
            else:
                self.sidebar.destroy()
                self.sidebar = None
                self.sidebar_open = False
        slide()

    def get_recent_items(self, limit=30):
        recent_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Recent")
        shell = win32com.client.Dispatch("WScript.Shell")
        items = []

        for file in sorted(os.listdir(recent_dir), key=lambda x: os.path.getmtime(os.path.join(recent_dir, x)), reverse=True):
            if file.endswith(".lnk"):
                path = os.path.join(recent_dir, file)
                try:
                    shortcut = shell.CreateShortcut(path)
                    target = shortcut.TargetPath
                    if os.path.exists(target):
                        items.append(target)
                        if len(items) >= limit:
                            break
                except:
                    continue
        return items

    def open_file(self, path):
        try:
            os.startfile(path)
        except:
            subprocess.Popen(["explorer", path])

# Run app
root = tk.Tk()
app = SidebarApp(root)
root.mainloop()
