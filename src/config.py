class Config:
    def __init__(self, cParams: dict):
        self.filePath: str = cParams.get("file", None)
        self.dirPath: str = cParams.get("dir", None)
        self.borderAmount: float = cParams.get("border", 5)
        self.colour: str = cParams.get("colour", "white")
        self.ratio: str = cParams.get("ratio", None)
        self.useLong: bool = cParams.get("useLong", False)
        self.resize: str = cParams.get("resize", None)
        