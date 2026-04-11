class Cell:
    def __init__(self, hex_value: str = 'f'):
        self.n, self.e, self.s, self.w = self.hex_to_bool(hex_value)

    def binary_repr(self) -> str:
        return f"{self.w}{self.s}{self.e}{self.n}"

    @staticmethod
    def hex_to_bool(hex: str) -> list[bool]:
        val: int = int(hex, 16)
        return [
            bool((val >> 0) & 1),
            bool((val >> 1) & 1),
            bool((val >> 2) & 1),
            bool((val >> 3) & 1),
        ]

