import math

class ProgressCircle:
    def __init__(self, options):
        self.canvas = options['canvas']
        self.min_radius = options['min_radius']
        self.entries = []
        self.ctx = None

    def add_entry(self, entry):
        self.entries.append(entry)

    def start(self, total_tasks):
        radius = max(self.min_radius, min(self.canvas.width, self.canvas.height) / 2 - 5)
        center_x = self.canvas.width / 2
        center_y = self.canvas.height / 2
        current_angle = -math.pi / 2

        self.ctx = self.canvas.getContext('2d')  # Corrigido aqui

        for entry in self.entries:
            progress = entry['progress_listener']() / total_tasks
            end_angle = current_angle + 2 * math.pi * progress

            self.ctx.beginPath()
            self.ctx.moveTo(center_x, center_y)
            self.ctx.arc(center_x, center_y, radius, current_angle, end_angle)
            self.ctx.lineTo(center_x, center_y)
            self.ctx.fillStyle = entry['fill_color']
            self.ctx.fill()

            current_angle = end_angle

            if entry['info_listener']:
                text_x = center_x + math.cos(end_angle - math.pi / 2) * (radius + 10)
                text_y = center_y + math.sin(end_angle - math.pi / 2) * (radius + 10)
                self.ctx.fillText(entry['info_listener'](), text_x, text_y)

    def remove(self):
        self.ctx.clearRect(0, 0, self.canvas.width, self.canvas.height)
