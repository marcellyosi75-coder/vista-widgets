from pathlib import Path

WIDGET_INFO = {
    "key": "cpu_temp",
    "title": "CPU Temperature",
    "version": "1.0",
    "author": "marcellyosi75",
    "description": "Suhu CPU realtime",
}


class Widget(BaseWidget):
    def __init__(self, parent, key, sidebar):
        super().__init__(parent, key, sidebar, "CPU Temp")

        self.temp_lbl = tk.Label(self.body, text="--°C",
                                  bg="#0f2347", fg="#ffffff",
                                  font=("sans", 24, "bold"))
        self.temp_lbl.pack(pady=(6, 2))

        self.bar_canvas = tk.Canvas(self.body, height=14, bg="#050d1c",
                                     highlightthickness=0)
        self.bar_canvas.pack(fill="x", pady=(0, 4))
        self.bar = self.bar_canvas.create_rectangle(
            0, 0, 0, 14, fill="#7cb342", outline="")

        self.status_lbl = tk.Label(self.body, text="",
                                    bg="#0f2347", fg="#8fb0d8",
                                    font=("sans", 8))
        self.status_lbl.pack(pady=(0, 4))

        self._tick()

    def _read_temp(self):
        # Coba beberapa path umum
        paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/devices/virtual/thermal/thermal_zone0/temp",
        ]
        for p in paths:
            try:
                v = int(Path(p).read_text().strip())
                # Kadang dalam mili-degree
                return v / 1000.0 if v > 1000 else float(v)
            except Exception:
                continue
        return None

    def _tick(self):
        if not self.alive():
            return
        t = self._read_temp()
        if t is None:
            self.temp_lbl.config(text="N/A")
            self.status_lbl.config(text="Sensor tidak tersedia")
        else:
            self.temp_lbl.config(text=f"{t:.1f}°C")
            if t < 50:
                color, status = "#7cb342", "Normal"
            elif t < 70:
                color, status = "#e67e22", "Hangat"
            else:
                color, status = "#c0392b", "Panas!"

            w = self.bar_canvas.winfo_width() or 150
            pct = min(100, t / 100 * 100)
            self.bar_canvas.coords(self.bar, 0, 0, w * pct / 100, 14)
            self.bar_canvas.itemconfig(self.bar, fill=color)
            self.status_lbl.config(text=status)

        self.temp_lbl.after(5000, self._tick)
