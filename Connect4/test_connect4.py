import pytest

from Connect4 import *

def test_create_board():
    assert create_board() == [[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
                              [None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
                              [None,None,None,None,None,None,None],[None,None,None,None,None,None,None]]
@pytest.mark.parametrize("board, symbol, column, new_board, selected_row",[
    # 1st test
    ([[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],[None,None,None,None,None,None,None]], 'X', 2,
    [[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],[None,None,'X',None,None,None,None]],5),
    # 2nd test
    ([[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,'O',None,None,None,None],[None,None,'X','X',None,None,None]], 'O', 2,
    [[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None],[None,None,'O',None,None,None,None],
    [None,None,'O',None,None,None,None],[None,None,'X','X',None,None,None]],3),
    # fully filled column 2 should return original board and selected row 999
    ([[None,None,'X',None,None,None,None],[None,None,'O',None,None,None,None],
    [None,None,'X',None,None,None,None],[None,None,'O',None,None,None,None],
    [None,None,'O',None,None,None,None],[None,None,'X','X',None,None,None]], 'X', 2,
    [[None, None, 'X', None, None, None, None], [None, None, 'O', None, None, None, None],
    [None, None, 'X', None, None, None, None], [None, None, 'O', None, None, None, None],
    [None, None, 'O', None, None, None, None], [None, None, 'X', 'X', None, None, None]],999)
])
def test_drop_piece(board,symbol,column, new_board, selected_row):
    result_board, result_row =  drop_piece(board,symbol,column)
    assert result_board == new_board
    assert result_row == selected_row

@pytest.mark.parametrize("row, col, dir_row, dir_col, board, symbol,result", [
# Check vertical 4
(2,6,1,0,[[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,None,None,'X'],[None,None,None,None,None,None,'X'],
    [None,None,None,None,None,None,'X'],[None,None,None,None,None,None,'X']],'X',True
),
# Check horizontal 4
(2,1,0,1,[[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,'O','O','O',None,None,None],[None,None,None,None,None,None,'X'],
    [None,None,None,None,None,None,'X'],[None,None,None,None,None,None,'X']],'O',False
),
(2,1,0,1,[[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,'O','O','O','O',None,None],[None,None,None,None,None,None,'X'],
    [None,None,None,None,None,None,'X'],[None,None,None,None,None,None,'X']],'O',True
),
# Check /
(2,4,1,-1,[[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,'O',None,None],[None,None,None,'O',None,None,'X'],
    [None,None,'O',None,None,None,'X'],[None,'O',None,None,None,None,'X']],'O',True
),
# Check \
(0,1,1,1,[[None,'X',None,None,None,None,None],[None,None,'X',None,None,None,None],
    [None,None,None,'X',None,None,None],[None,None,None,'O','X',None,'X'],
    [None,None,'O',None,None,None,'X'],[None,'O',None,None,None,None,'X']],'X',True
)
])
def test_check4(row, col, dir_row, dir_col, board, symbol, result):
    assert check4(row, col, dir_row, dir_col, board,symbol) == result

@pytest.mark.parametrize("row, col, board, symbol,result", [
# Check vertical 4
(2,6,[[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,None,None,'X'],[None,None,None,None,None,None,'X'],
    [None,None,None,None,None,None,'X'],[None,None,None,None,None,None,'X']],'X',True
),
# Check horizontal 4
(2,1,[[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,'O','O','O',None,None,None],[None,None,None,None,None,None,'X'],
    [None,None,None,None,None,None,'X'],[None,None,None,None,None,None,'X']],'O',False
),
(2,1,[[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,'O','O','O','O',None,None],[None,None,None,None,None,None,'X'],
    [None,None,None,None,None,None,'X'],[None,None,None,None,None,None,'X']],'O',True
),
# Check /
(2,4,[[None,None,None,None,None,None,None],[None,None,None,None,None,None,None],
    [None,None,None,None,'O',None,None],[None,None,None,'O',None,None,'X'],
    [None,None,'O',None,None,None,'X'],[None,'O',None,None,None,None,'X']],'O',True
),
# Check \
(0,1,[[None,'X',None,None,None,None,None],[None,None,'X',None,None,None,None],
    [None,None,None,'X',None,None,None],[None,None,None,'O','X',None,'X'],
    [None,None,'O',None,None,None,'X'],[None,'O',None,None,None,None,'X']],'X',True
)
])
def test_check_winner(row, col, board, symbol, result):
    assert check_winner(board, symbol, row, col) == result