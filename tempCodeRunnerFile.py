def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))