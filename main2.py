from typing import List


class Board:
    def __init__(self, size: int):
        self.N = size
        self.queens: List[int] = []
        self.matches: List[List[int]] = []

    def is_queen_valid(self, row: int, col: int):
        for r, c in enumerate(self.queens):
            if r == row or c == col or abs(row - r) == abs(col - c):
                return False
        return True

    def solution(self) -> List[List[int]]:
        self.queens = []
        col = row = 0
        i = 0
        while True:
            while col < self.N and not self.is_queen_valid(row, col):
                col += 1
            if col < self.N:
                self.queens.append(col)

                if row + 1 >= self.N:
                    self.matches.append(self.queens.copy())
                    self.queens.pop()
                    col = self.N
                else:
                    row += 1
                    col = 0

            if col >= self.N:
                # not possible to place a queen in this row anymore
                if row == 0:
                    return self.matches.copy()  # all combinations were tried
                col = self.queens.pop() + 1  # Increment column
                row -= 1
            i += 1


board = Board(4)

print(board.solution())
