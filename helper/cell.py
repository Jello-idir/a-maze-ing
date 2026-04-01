class Cell:
	def __init__(self) -> None:
		self.top: Cell = None
		self.bottom: Cell = None
		self.left: Cell = None
		self.right: Cell = None
		self.hex: int = 0
		self.value: str = "."
		self.neighbor: Cell = None
		self.is_origin: bool = False
		self.north = False
		self.east = False
		self.south = False
		self.west = False
