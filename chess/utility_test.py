from chess.utility import get_pieces
from chess.utility import is_empty
from chess.utility import get_potential_rook_moves
from chess.utility import get_potential_king_moves
from chess.utility import get_legal_moves
from chess.utility import only_kings_left

def test_get_pieces():
    board = {
        'row': 4, 
        'column': 4, 
        'pieces': [
            {'type': 'rook', 'color': 'white', 'x': 0, 'y': 0}, 
            {'type': 'king', 'color': 'white', 'x': 1, 'y': 0}, 
            {'type': 'king', 'color': 'black', 'x': 3, 'y': 3}
        ]
    }
    player_pieces = get_pieces('white', board)
    
    assert len(player_pieces) == 2
    assert player_pieces[0]['type'] == 'rook'
    assert player_pieces[0]['color'] == 'white'
    assert player_pieces[0]['x'] == 0
    assert player_pieces[0]['y'] == 0
    
    assert player_pieces[1]['type'] == 'king'
    assert player_pieces[1]['color'] == 'white'
    assert player_pieces[1]['x'] == 1
    assert player_pieces[1]['y'] == 0

def test_is_empty():
    board = {
        'row': 4, 
        'column': 4, 
        'pieces': [
            {'type': 'rook', 'color': 'white', 'x': 0, 'y': 0}, 
            {'type': 'king', 'color': 'black', 'x': 3, 'y': 3}
        ]
    }
    
    assert is_empty({'x': 0, 'y': 1}, board)
    assert not is_empty({'x': 0, 'y': 0}, board)
    assert not is_empty({'x': 3, 'y': 3}, board)
    
def test_get_potential_rook_moves():
    board = {'row': 4, 'column': 4}
    moves = get_potential_rook_moves({'x': 1, 'y': 2}, board)
    assert len(moves) == 6
    
    # horizontal
    assert {'x': 1, 'y': 0} in moves
    assert {'x': 1, 'y': 1} in moves
    assert {'x': 1, 'y': 3} in moves
    
    # vertical
    assert {'x': 0, 'y': 2} in moves
    assert {'x': 2, 'y': 2} in moves
    assert {'x': 3, 'y': 2} in moves
    
def test_get_potential_king_moves():
    board = {'row': 3, 'column': 3}
    test_cases = [
        {
            'square': {'x': 0, 'y': 0}, 
            'expected': [
                {'x': 1, 'y': 0}, 
                {'x': 0, 'y': 1}, 
                {'x': 1, 'y': 1}
            ]
        },
        {
            'square': {'x': 1, 'y': 0},
            'expected': [
                {'x': 0, 'y': 0},
                {'x': 2, 'y': 0},
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 1}
            ]
        },
        {
            'square': {'x': 2, 'y': 0},
            'expected': [
                {'x': 1, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 1}
            ]
        },
        {
            'square': {'x': 0, 'y': 1},
            'expected': [
                {'x': 0, 'y': 0},
                {'x': 0, 'y': 2},
                {'x': 1, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': 1, 'y': 2}
            ]
        },
        {
            'square': {'x': 1, 'y': 1},
            'expected': [
                {'x': 0, 'y': 0},
                {'x': 1, 'y': 0},
                {'x': 2, 'y': 0},
                {'x': 0, 'y': 1},
                {'x': 2, 'y': 1},
                {'x': 0, 'y': 2},
                {'x': 1, 'y': 2},
                {'x': 2, 'y': 2}
            ]
        },
        {
            'square': {'x': 2, 'y': 1},
            'expected': [
                {'x': 1, 'y': 0},
                {'x': 1, 'y': 1},
                {'x': 1, 'y': 2},
                {'x': 2, 'y': 0},
                {'x': 2, 'y': 2}
            ]
        },
        {
            'square': {'x': 0, 'y': 2},
            'expected': [
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 1},
                {'x': 1, 'y': 2}
            ]
        },
        {
            'square': {'x': 1, 'y': 2},
            'expected': [
                {'x': 0, 'y': 1},
                {'x': 1, 'y': 1},
                {'x': 2, 'y': 1},
                {'x': 0, 'y': 2},
                {'x': 2, 'y': 2}
            ]
        },
        {
            'square': {'x': 2, 'y': 2},
            'expected': [
                {'x': 1, 'y': 1},
                {'x': 1, 'y': 2},
                {'x': 2, 'y': 1}
            ]
        }
    ]
    for test_case in test_cases:
        print ('running test case:', test_case)
        moves = get_potential_king_moves(test_case['square'], board)
        
        assert len(moves) == len(test_case['expected'])
        for expected_move in test_case['expected']:
            assert expected_move in moves
            
def test_get_legal_moves():
    board = {'row': 3, 'column': 3, 'pieces': [
        {'type': 'king', 'color': 'white', 'x': 0, 'y': 0},
	{'type': 'rook', 'color': 'white', 'x': 1, 'y': 0},
	{'type': 'king', 'color': 'black', 'x': 2, 'y': 2}
    ]}
    test_cases = [
        {
            'board': {'row': 3, 'column': 3, 'pieces': [
                {'type': 'king', 'color': 'white', 'x': 0, 'y': 0},
		{'type': 'rook', 'color': 'white', 'x': 1, 'y': 0},
		{'type': 'king', 'color': 'black', 'x': 2, 'y': 2}
            ]},
            'player': 'black',
            'expected': [
                {'piece': {'type': 'king', 'color': 'black', 'x': 2, 'y': 2}, 
                 'moves': [{'x': 2, 'y': 1}]
                }
            ]
        },
	{
            'board': {'row': 3, 'column': 3, 'pieces': [
                {'type': 'king', 'color': 'white', 'x': 0, 'y': 0},
		{'type': 'rook', 'color': 'white', 'x': 1, 'y': 0},
		{'type': 'king', 'color': 'black', 'x': 2, 'y': 2}
            ]},
            'player': 'white',
            'expected': [
                {'piece': {'type': 'king', 'color': 'white', 'x': 0, 'y': 0}, 
                 'moves': [{'x': 0, 'y': 1}]
                },
		{'piece': {'type': 'rook', 'color': 'white', 'x': 1, 'y': 0}, 
                 'moves': [{'x': 2, 'y': 0}, {'x': 1, 'y': 1}, {'x': 1, 'y': 2}]
                },
            ]
        },
	# Checkmate case
	{
            'board': {'row': 3, 'column': 3, 'pieces': [
                {'type': 'king', 'color': 'white', 'x': 2, 'y': 0},
		{'type': 'rook', 'color': 'white', 'x': 0, 'y': 2},
		{'type': 'king', 'color': 'black', 'x': 2, 'y': 2}
            ]},
            'player': 'black',
            'expected': []
        },
	# Capture case
	{
            'board': {'row': 3, 'column': 2, 'pieces': [
		{'type': 'king', 'color': 'white', 'x': 0, 'y': 0},
		{'type': 'rook', 'color': 'white', 'x': 0, 'y': 2},
		{'type': 'king', 'color': 'black', 'x': 1, 'y': 2}
            ]},
            'player': 'black',
            'expected': [
		{'piece': {'type': 'king', 'color': 'black', 'x': 1, 'y': 2}, 
                 'moves': [{'x': 0, 'y': 2}]
                }
	    ]
        }
    ]
    for test_case in test_cases:
        print ('running test case:', test_case)
        moves = get_legal_moves(test_case['player'], test_case['board'])
        
        assert len(moves) == len(test_case['expected'])
        for expected_move in test_case['expected']:
            assert expected_move in moves
	
def test_only_kings_left():
    test_cases = [
        {
            'board': {'row': 3, 'column': 3, 'pieces': [
                {'type': 'king', 'color': 'white', 'x': 0, 'y': 0},
		{'type': 'rook', 'color': 'white', 'x': 1, 'y': 0},
		{'type': 'king', 'color': 'black', 'x': 2, 'y': 2}
            ]},
            'expected': False
        },
	{
            'board': {'row': 3, 'column': 3, 'pieces': [
                {'type': 'king', 'color': 'white', 'x': 0, 'y': 0},
		{'type': 'king', 'color': 'black', 'x': 2, 'y': 2}
            ]},
            'expected': True
        }
    ]
    for test_case in test_cases:
        print ('running test case:', test_case)
        assert only_kings_left(test_case['board']) == test_case['expected']
