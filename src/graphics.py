class Graphic:
    def __init__(self, stream: str) -> None:
        self.stream = stream
        self.text = ""
        self.colors = []
    
        self.load()
    
    def load(self):
        text = self.stream
        for line in text.splitlines():
            for element in line.split(';'):
                self.text += element[0]
                self.colors.append(int(element[1]))

class Loader:
    def __init__(self, graphic_path):
        self.path = graphic_path + ".gfx" if ".gfx" not in graphic_path else graphic_path

        self.graphics = {}
    
        self.load()

    def get(self, key: str):
        return self.graphics.get(key)

    def load(self):
        text = open(self.path, 'r').read()
        stream = name = ""
        for line in text.splitlines():
            if line.startswith("//"):
                if stream != "":
                    stream = stream.removesuffix("\n")
                    self.graphics.update({ name: Graphic(stream) })
                stream = ""
                name = line.removeprefix("//").strip()
            else:
                stream += line + "\n"
        stream = stream.removesuffix("\n")
        self.graphics.update({ name: Graphic(stream) })