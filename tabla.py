import tkinter as tk

# Tablero de Sudoku de ejemplo (puedes reemplazarlo con el tuyo)
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def check_board(board):
    # Verificar filas
    for row in board:
        if len(set(row)) != 9:
            return False

    # Verificar columnas
    for col in range(9):
        column_values = [board[row][col] for row in range(9)]
        if len(set(column_values)) != 9:
            return False

    # Verificar regiones 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            region_values = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if len(set(region_values)) != 9:
                return False

    return True

def solve_sudoku(board, row, col):
    if row == 8 and col == 9:
        return True
    if col == 9:
        row += 1
        col = 0
    if board[row][col] > 0:
        return solve_sudoku(board, row, col + 1)
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board, row, col + 1):
                return True
            board[row][col] = 0
    return False

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def update_board():
    for i in range(9):
        for j in range(9):
            value = sudoku_board[i][j]
            if value == 0:
                entry_grid[i][j].delete(0, 'end')
            else:
                entry_grid[i][j].delete(0, 'end')
                entry_grid[i][j].insert(0, str(value))

def solve():
    if solve_sudoku(sudoku_board, 0, 0) and check_board(sudoku_board):
        update_board()
        result_label.config(text="Solución válida")
    else:
        result_label.config(text="Sin solución válida")

def submit():
    for i in range(9):
        for j in range(9):
            value = entry_grid[i][j].get()
            if value:
                try:
                    value = int(value)
                    if 1 <= value <= 9:
                        sudoku_board[i][j] = value
                    else:
                        entry_grid[i][j].delete(0, 'end')
                except ValueError:
                    entry_grid[i][j].delete(0, 'end')
            else:
                sudoku_board[i][j] = 0

    if check_board(sudoku_board):
        result_label.config(text="Sudoku válido")
    else:
        result_label.config(text="Sudoku inválido")

root = tk.Tk()
root.title("Sudoku Solver")

entry_grid = [[None for _ in range(9)] for _ in range(9)]

for i in range(9):
    for j in range(9):
        entry_grid[i][j] = tk.Entry(root, width=5)
        entry_grid[i][j].grid(row=i, column=j)

update_board()

solve_button = tk.Button(root, text="Resolver", command=solve)
solve_button.grid(row=10, columnspan=9)

submit_button = tk.Button(root, text="Enviar", command=submit)
submit_button.grid(row=11, columnspan=9)

result_label = tk.Label(root, text="")
result_label.grid(row=12, columnspan=9)

root.mainloop()
