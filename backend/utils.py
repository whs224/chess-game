def algebraic_to_index(pos):
    file_to_col = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    col = file_to_col[pos[0].lower()]
    row = 8 - int(pos[1])
    return (row, col)

def index_to_algebraic(row, col):
    col_to_file = 'abcdefgh'
    return f"{col_to_file[col]}{8 - row}"