import json

class SceneDataManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.load()

    def load(self):
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                return json.load(f)
        return {}

    def get_object_data(self, key, default):
        return self.data.get(key, default)

    def update_object(self, key, rect):
        self.data[key] = {
            "x": rect.x,
            "y": rect.y,
            "width": rect.width,
            "height": rect.height
        }
        self.save()

    def save(self):
        with open(self.data_file, "w") as f:
            json.dump(self.data, f, indent=4)