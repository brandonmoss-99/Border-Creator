import os

class Config:
    def __init__(self, cParams: dict):
        self.filePath: str = os.path.abspath(cParams.get("file", "."))
        self.dirPath: str = os.path.abspath(cParams.get("dir", "."))
        self.borderAmount: int = cParams.get("border", 5)
        self.colour: str = cParams.get("colour", "white")
        self.useLong: bool = cParams.get("useLong", False)
        