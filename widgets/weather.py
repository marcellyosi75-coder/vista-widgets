import urllib.request
import json

WIDGET_INFO = {
    "key": "weather",
    "title": "Weather",
    "version": "1.0",
    "author": "marcellyosi75",
    "description": "Cuaca realtime Jakarta",
}


class Widget(BaseWidget):
    def __init__(self, parent, key, sidebar):
        super().__init__(parent, key, sidebar, "Weather")

        self.city_lbl = tk.Label(self.body, text="Jakarta",
                                  bg="#0f2347", fg="#8fb0d8",
                                  font=("sans", 9, "bold"))
        self.city_lbl.pack(pady=(4, 0))

        self.temp_lbl = tk.Label(self.body, text="--°C",
                                  bg="#0f2347", fg="#ffffff",
                                  font=("sans", 28, "bold"))
        self.temp_lbl.pack()

        self.desc_lbl = tk.Label(self.body, text="Loading...",
                                  bg="#0f2347", fg="#4a9eff",
                                  font=("sans", 10),
                                  wraplength=180, justify="center")
        self.desc_lbl.pack(pady=(0, 4))

        self.detail_lbl = tk.Label(self.body, text="",
                                    bg="#0f2347", fg="#8fb0d8",
                                    font=("sans", 8))
        self.detail_lbl.pack(pady=(0, 6))

        self._tick()

    def _tick(self):
        if not self.alive():
            return
        try:
            url = "https://wttr.in/Jakarta?format=j1"
            req = urllib.request.Request(
                url, headers={"User-Agent": "curl/7.68"})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read().decode())
            curr = data["current_condition"][0]
            temp = curr["temp_C"]
            feels = curr["FeelsLikeC"]
            desc = curr["weatherDesc"][0]["value"]
            humid = curr["humidity"]

            self.temp_lbl.config(text=f"{temp}°C")
            self.desc_lbl.config(text=desc)
            self.detail_lbl.config(
                text=f"Feels {feels}°C · {humid}%")
        except Exception:
            self.desc_lbl.config(text="Offline")
            self.temp_lbl.config(text="--°C")

        self.temp_lbl.after(600000, self._tick)  # 10 menit
