from common import Action, Dir

class Cell:
    def __init__(self, id: int) -> None:
        self.id = id

        self.top: Cell = None
        self.bottom: Cell = None
        self.left: Cell = None
        self.right: Cell = None

        self.hex: int = 15
        self.neighbor: Cell = None

    def __edit_wall(self, action: Action, dir: Dir) -> None:
        if self.hex >> dir.value & 1 and action == Action.OPEN:
            self.hex -= 2 ** dir.value
        elif not (self.hex >> dir.value & 1) and action == Action.CLOSE:
            self.hex += 2 ** dir.value

    def open(self, dir: Dir) -> None:
        self.__edit_wall(Action.OPEN, dir)

        neighbor = [
            self.top,
            self.right,
            self.bottom,
            self.left
        ][dir.value]
        if (neighbor):
            neighbor.__edit_wall(Action.OPEN,
                        Dir(dir.value + 2 * (dir.value < 2)
                        - 2 * (dir.value >= 2))
                                )

    def close(self, dir: Dir) -> None:
        self.__edit_wall(Action.CLOSE, dir)
        neighbor = [
            self.top,
            self.right,
            self.bottom,
            self.left
        ][dir.value]
        if neighbor:
            neighbor.__edit_wall(Action.CLOSE,
                        Dir(dir.value + 2 * (dir.value < 2)
                        - 2 * (dir.value >= 2))
                                )


    def update_walls(self) -> None:
        next_blocks = [self.top, self.right, self.bottom, self.left]
        dirs = [Dir.N, Dir.E, Dir.S, Dir.W]

        for block, dir in zip(next_blocks, dirs):
            if block and self.neighbor and self.neighbor.id == block.id:
                self.open(dir)
                break

