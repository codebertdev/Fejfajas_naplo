import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
from datetime import date

from sr_tracker_utils import SrHeadacheEntry, sr_calculate_average


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Headache Tracker")
        self.entries = []

        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self._build_input_section()
        self._build_list_section()
        self._build_stats_section()

    def _build_input_section(self):
        input_frame = ttk.LabelFrame(self.main_frame, text="Új bejegyzés")
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        lbl_date = ttk.Label(input_frame, text="Dátum (YYYY-MM-DD):")
        lbl_date.grid(row=0, column=0, sticky="w", padx=(5, 5), pady=(5, 5))

        self.entry_date = ttk.Entry(input_frame)
        self.entry_date.grid(row=0, column=1, sticky="ew", padx=(5, 5), pady=(5, 5))
        self.entry_date.insert(0, date.today().isoformat())

        lbl_intensity = ttk.Label(input_frame, text="Erősség (0-10):")
        lbl_intensity.grid(row=1, column=0, sticky="w", padx=(5, 5), pady=(5, 5))

        self.scale_intensity = ttk.Scale(input_frame, from_=0, to=10, orient="horizontal")
        self.scale_intensity.grid(row=1, column=1, sticky="ew", padx=(5, 5), pady=(5, 5))
        self.scale_intensity.set(5)

        self.lbl_intensity_value = ttk.Label(input_frame, text="5")
        self.lbl_intensity_value.grid(row=1, column=2, sticky="w", padx=(5, 5), pady=(5, 5))

        self.scale_intensity.bind("<B1-Motion>", self._update_intensity_label)
        self.scale_intensity.bind("<ButtonRelease-1>", self._update_intensity_label)

        lbl_note = ttk.Label(input_frame, text="Megjegyzés:")
        lbl_note.grid(row=2, column=0, sticky="nw", padx=(5, 5), pady=(5, 5))

        self.text_note = tk.Text(input_frame, height=3, width=40)
        self.text_note.grid(row=2, column=1, columnspan=2, sticky="ew", padx=(5, 5), pady=(5, 5))

        btn_add = ttk.Button(input_frame, text="Bejegyzés mentése", command=self._add_entry)
        btn_add.grid(row=3, column=1, sticky="e", padx=(5, 5), pady=(5, 5))

        btn_predict = ttk.Button(input_frame, text="Holnapi tippelt erősség", command=self._predict_tomorrow)
        btn_predict.grid(row=3, column=2, sticky="w", padx=(5, 5), pady=(5, 5))

    def _build_list_section(self):
        list_frame = ttk.LabelFrame(self.main_frame, text="Korábbi bejegyzések")
        list_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.listbox_entries = tk.Listbox(list_frame, height=10)
        self.listbox_entries.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(5, 5))

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox_entries.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", padx=(0, 5), pady=(5, 5))
        self.listbox_entries.configure(yscrollcommand=scrollbar.set)

    def _build_stats_section(self):
        stats_frame = ttk.LabelFrame(self.main_frame, text="Statisztika")
        stats_frame.grid(row=2, column=0, sticky="ew")
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)

        btn_avg = ttk.Button(stats_frame, text="Átlagos fejfájás erősség", command=self._show_average)
        btn_avg.grid(row=0, column=0, sticky="ew", padx=(5, 5), pady=(5, 5))

        self.lbl_avg = ttk.Label(stats_frame, text="Nincs még kiszámolt átlag.")
        self.lbl_avg.grid(row=0, column=1, sticky="w", padx=(5, 5), pady=(5, 5))

    def _update_intensity_label(self, event=None):
        value = int(round(self.scale_intensity.get()))
        self.lbl_intensity_value.configure(text=str(value))

    def _add_entry(self):
        date_str = self.entry_date.get().strip()
        try:
            intensity_value = int(round(self.scale_intensity.get()))
        except ValueError:
            messagebox.showerror("Hiba", "Az erősség nem értelmezhető.")
            return

        if intensity_value < 0 or intensity_value > 10:
            messagebox.showerror("Hiba", "Az erősségnek 0 és 10 között kell lennie.")
            return

        note_text = self.text_note.get("1.0", "end").strip()

        if not date_str:
            messagebox.showerror("Hiba", "A dátum mező nem lehet üres.")
            return

        entry = SrHeadacheEntry(date_str, intensity_value, note_text)
        self.entries.append(entry)
        self.listbox_entries.insert("end", entry.to_display_string())

        self.text_note.delete("1.0", "end")

    def _show_average(self):
        if not self.entries:
            messagebox.showinfo("Átlag", "Még nincs elég adat az átlaghoz.")
            return

        avg = sr_calculate_average(self.entries)
        rounded = math.ceil(avg * 10) / 10
        self.lbl_avg.configure(text=f"Átlagos erősség: {rounded}/10")

    def _predict_tomorrow(self):
        predicted = random.randint(0, 10)
        messagebox.showinfo("Tippelt holnapi erősség", f"A tippelt fejfájás erősség holnapra: {predicted}/10")
