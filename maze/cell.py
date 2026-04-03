from common import Action, Dir

class Cell:
    def __init__(self) -> None:
        self.top: Cell = None
        self.bottom: Cell = None
        self.left: Cell = None
        self.right: Cell = None

        self.hex: int = 15
        self.neighbor: Cell = None
        self.is_origin = False
        self.locked = False

    def __edit_wall(self, action: Action, dir: Dir) -> None:
        if self.hex >> dir.value & 1 and action == Action.OPEN:
            self.hex -= 2 ** dir.value
        elif not (self.hex >> dir.value & 1) and action == Action.CLOSE:
            self.hex += 2 ** dir.value

    def _open(self, dir: Dir) -> None:
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

    def _close(self, dir: Dir) -> None:
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

    @staticmethod
    def wall_status(target, dir: Dir) -> None:
        return target.hex >> dir.value & 1


    def update_walls(self) -> None:
        next_blocks = [self.top, self.right, self.bottom, self.left]
        curr_block_dirs = [Dir.N, Dir.E, Dir.S, Dir.W]
        next_block_dirs = [Dir.S, Dir.W, Dir.N, Dir.E]

        for block, cb_dir, nb_dir in zip(next_blocks, curr_block_dirs, next_block_dirs):
            if self.neighbor and block:
                neighbor_id = self.neighbor
                if neighbor_id == block:
                    self._open(cb_dir)
                    block._open(nb_dir)
