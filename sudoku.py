import time


class Sudoku(object):
    # pass in 0 as a blank list and modify after
    def __init__(self, data):
        self.solved, self.original = [], []
        temp1, temp2 = [], []
        # print(data)
        for ind, val in enumerate(data):
            if val == '0':
                temp1.append(set(range(1, 10)))
                temp2.append(0)

            else:
                temp1.append(int(val))
                temp2.append(int(val))

            if (ind + 1) % 9 == 0:
                self.solved.append(temp1)
                self.original.append(temp2)
                temp1, temp2 = [], []

        self.starttime = time.time()
        self.solve()


    def __str__(self):
        string = f'solved in {time.time() - self.starttime} seconds\n'
        string += 'original sudoku\n'
        for i in self.original:
            string += str(i) + '\n'
        string += 'solved sudoku\n'
        for i in self.solved:
            string += str(i) + '\n'
        return string.strip()


    def copy(self, lst):
        val = []
        for i in lst:
            val.append([b.copy() if isinstance(b, set) else b for b in i])
        return val


    def solve(self) -> bool:
        solved, hung = False, False
        while not hung and not solved:
            solved, hung = True, True
            for row, col in [(i // 9, i % 9) for i in range(81)]:
                if isinstance(self.solved[row][col], int):
                    a = self._remove_cross(row, col, self.solved[row][col])
                    b = self._remove_block(row, col, self.solved[row][col])
                    if a or b:
                        hung = False

                else:
                    solved = False

        if solved:
            return True

        if hung:
            copy = self.copy(self.solved)
            length = float('inf')
            for row, col in [(i // 9, i % 9) for i in range(81)]:
                if isinstance(self.solved[row][col], set) and\
                   len(self.solved[row][col]) < length:
                    guesses = self.solved[row][col]
                    length = len(guesses)
                    break

            for guess in guesses:
                self.solved[row][col] = guess
                if self.solve():
                    return True
                else:
                    self.solved = self.copy(copy)

            return False


    def _remove_cross(self, row, col, num) -> bool:
        change = False
        for ind in range(9):
            if isinstance(self.solved[row][ind], set):
                self.solved[row][ind].discard(num)
                if len(self.solved[row][ind]) == 1:
                    val = self.solved[row][ind].pop()
                    if self._check(row, ind, val):
                        self.solved[row][ind] = val
                        change = True
            if isinstance(self.solved[ind][col], set):
                self.solved[ind][col].discard(num)
                if len(self.solved[ind][col]) == 1:
                    val = self.solved[ind][col].pop()
                    if self._check(ind, col, val):
                        self.solved[ind][col] = val
                        change = True

        return change


    def _remove_block(self, row, col, num) -> bool:
        r_inc, c_inc, change = row // 3 * 3, col // 3 * 3, False
        for r_ind, c_ind in [(i // 3 + r_inc, i % 3 + c_inc) for i in range(9)]:
            if isinstance(self.solved[r_ind][c_ind], set):
                self.solved[r_ind][c_ind].discard(num)
                if len(self.solved[r_ind][c_ind]) == 1:
                    val = self.solved[r_ind][c_ind].pop()
                    if self._check(r_ind, c_ind, val):
                        self.solved[r_ind][c_ind] = val
                        change = True
        return change


    def _check(self, row, col, val):
        check1, check2 = set([val]), set([val])
        for ind in range(9):
            type1 = isinstance(self.solved[row][ind], int)
            type2 = isinstance(self.solved[ind][col], int)
            if type1 and self.solved[row][ind] in check1:
                return False
            elif type1:
                check1.add(self.solved[row][ind])

            if type2 and self.solved[ind][col] in check2:
                return False
            elif type2:
                check2.add(self.solved[ind][col])
        return True


if __name__ == '__main__':

    # a = Sudoku('003200001010030070600005800400009500030070090002800003006100009040080020300004600')
    # a = Sudoku('530070000600195000098000060800060003400803001700020006060000280000419005000080079')
    # a = Sudoku('100070030830600000002900608600004907090000050307500004203009100000002043040080009')
    a = Sudoku('009748000700000000020109000007000240064010590098000300000803020000000006000275900')
    print(a)
