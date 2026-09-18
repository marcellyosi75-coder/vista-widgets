import math
from datetime import datetime

WIDGET_INFO = {
    "key": "clock",
    "title": "Analog Clock",
    "version": "1.0",
    "author": "marcellyosi75",
    "description": "Jam analog simple",
}

class Widget(BaseWidget):
    def __init__(self, parent, key, sidebar):
        super().__init__(parent, key, sidebar, "Analog Clock")
        self.canvas = tk.Canvas(self.body, width=180, height=180,
                                 bg="#0f2347", highlightthickness=0)
        self.canvas.pack()
        self._draw_static()
        self._tick()

    def _draw_static(self):
        c = self.canvas
        c.create_oval(10, 10, 170, 170, outline="#4a9eff", width=2)
        for i in range(12):
            a = math.radians(i * 30 - 90)
            x1 = 90 + 68 * math.cos(a)
            y1 = 90 + 68 * math.sin(a)
            x2 = 90 + 76 * math.cos(a)
            y2 = 90 + 76 * math.sin(a)
            w = 3 if i % 3 == 0 else 1
            c.create_line(x1, y1, x2, y2, fill="#8fb0d8", width=w)

    def _tick(self):
        if not self.alive():
            return
        c = self.canvas
        c.delete("hands")
        now = datetime.now()
        h, m, s = now.hour % 12, now.minute, now.second

        a = math.radians((h + m/60) * 30 - 90)
        c.create_line(90, 90, 90 + 42*math.cos(a), 90 + 42*math.sin(a),
                      fill="#ffffff", width=4, tags="hands", capstyle="round")
        a = math.radians((m + s/60) * 6 - 90)
        c.create_line(90, 90, 90 + 58*math.cos(a), 90 + 58*math.sin(a),
                      fill="#ffffff", width=3, tags="hands", capstyle="round")
        a = math.radians(s * 6 - 90)
        c.create_line(90, 90, 90 + 66*math.cos(a), 90 + 66*math.sin(a),
                      fill="#4a9eff", width=1, tags="hands")
        c.create_oval(85, 85, 95, 95, fill="#4a9eff", outline="", tags="hands")

        self.canvas.after(1000, self._tick)
