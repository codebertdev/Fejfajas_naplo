
class SrHeadacheEntry:
    def __init__(self, date, intensity, note):
        self.date = date
        self.intensity = intensity
        self.note = note

    def to_display_string(self):
        short_note = self.note.strip().replace("\n", " ")
        if len(short_note) > 40:
            short_note = short_note[:37] + "..."
        return f"{self.date} | {self.intensity}/10 | {short_note}"


def sr_calculate_average(entries):
    if not entries:
        return 0.0
    total = 0
    for e in entries:
        total += e.intensity
    return total / len(entries)
