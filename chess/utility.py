# Get all valid moves from current board state.
# Assume the following is true:
#   Board is in legal state (i.e. kings are not next to each other, etc.)
#   Player is either 'white' 'black'
# 
# Return a list of all legal moves, something like this:
#   moves = [ {KING, [{3, 4}, {3, 2}]}, {PAWN3, [{1, 1}, {1, 2}, {2, 2}], etc.]
# 
# def get_legal_moves_for(player, board):
#   Algorithm:
#       Get all pieces whose color is the same as player -> pieces
#       For each piece:
#           If it's a Rook, then loop through 4 directions (left, right, up, down)
# 
from copy import deepcopy
from random import randint

def simulation(times):
    for x in range(times):
        play()

def play():
    board = {'row': 3, 'column': 3, 'pieces': [
        {'type': 'king', 'color': 'white', 'x': 0, 'y': 0},
	      {'type': 'rook', 'color': 'white', 'x': 1, 'y': 0},
	      {'type': 'king', 'color': 'black', 'x': 2, 'y': 2}
    ]}
    current_player = 'white'
    move_statistics = []
    
    while True:
        moves = get_legal_moves(current_player, board)
        
        # No more legal moves
        if not moves:
            break;
        
        move_piece = get_random_move(moves, board)
        move = move_piece['move']
        
        # Playground stuff only
        if current_player == 'white':
            move_numeric = move_piece_to_numeric(move_piece)
            move_statistics.append({'board': board, 'action': move_piece})
	    
        board = make_move(move_piece, board)
        
        if only_kings_left(board):
            break
            
        current_player = get_opponent_player(current_player)  
        
    king_piece = get_king_piece(current_player, board)
    king_square = {'x': king_piece['x'], 'y': king_piece['y']}
    
    winner = 'draw'
    opponent_player = get_opponent_player(current_player)
    
    if king_will_be_in_check(current_player, king_square, board):
        winner = opponent_player
    
    final_statistics = get_updated_stats(move_statistics, winner)
    final_statistics_delimited = get_delimited_stats(final_statistics)
    
    print_stats_delimited(final_statistics_delimited)

def print_stats_delimited(move_statistics_delimited):
    for stat in move_statistics_delimited:
        print (stat)

def get_updated_stats(move_statistics, winner):
    new_stats = deepcopy(move_statistics)
    for stat in new_stats:
        stat['winner'] = winner
    return new_stats

def get_delimited_stats(move_statistics):
    delimited_stats = []
    for stat in move_statistics:
        board_numeric = board_to_numeric(stat['board'])
        action_numeric = move_piece_to_numeric(stat['action'])
        winner_numeric = winner_to_numeric(stat['winner'])
        
        delimited_stats.append(
            str(board_numeric) + '|' + 
            str(action_numeric) + '|' + 
            str(winner_numeric)
        )
    return delimited_stats

def winner_to_numeric(winner):
    if winner == 'draw':
        return 0
    if winner == 'white':
        return 1
    if winner == 'black':
        return 2

def get_winner(board):
    white_king_piece = get_king_piece('white', board)
    black_king_piece = get_king_piece('black', board)
    
    white_king_square = {
        'x': white_king_piece['x'], 
        'y': white_king_piece['y']}
    black_king_square = {
        'x': black_king_piece['x'], 
        'y': black_king_piece['y']}
    
    if king_will_be_in_check('white', white_king_square, board):
        return 'black'
    if king_will_be_in_check('black', black_king_square, board):
        return 'white'
    return 'none'
        
    

def move_piece_to_numeric(move_piece):
    piece_type = move_piece['piece']['type']
    piece_color = move_piece['piece']['color']
    piece_type_num = piece_type_to_numeric(move_piece['piece'])
    
    move = move_piece['move']
    return int(str(piece_type_num) + str(move['x']) + str(move['y']))

def make_move(move_piece, board):
    move = move_piece['move']
    
    new_board = deepcopy(board)
    new_piece = deepcopy(move_piece['piece'])
    
    new_piece['x'] = move['x']
    new_piece['y'] = move['y']
    
    new_board['pieces'].remove(move_piece['piece'])
    new_board['pieces'].append(new_piece)
    
    # Check if can capture
    piece = get_piece({'x': move['x'], 'y': move['y']}, board)
    if piece != 'empty':
        new_board['pieces'].remove(piece)
    
    return new_board

def get_random_move(move_pieces, board):
    piece_index = randint(0, len(move_pieces) - 1)
    move_piece = move_pieces[piece_index]
    
    move_index = randint(0, len(move_piece['moves']) - 1)
    move = move_piece['moves'][move_index]
    
    return {'piece': move_piece['piece'], 'move': move}

def get_legal_moves(player, board):
    moves = []
    player_pieces = get_pieces(player, board)
    potential_move_pieces = get_all_potential_moves(player_pieces, board)
    return get_valid_moves(potential_move_pieces, board)
    

def get_all_potential_moves(pieces, board):
    potential_moves = []
    for piece in pieces:
        current_square = {'x': piece['x'], 'y': piece['y']}
        if piece['type'] == 'rook':
            potential_moves.append(
                {
                    'piece': piece, 
                    'moves': get_valid_rook_moves(piece, board)
                }
            )
        if piece['type'] == 'king':
            potential_moves.append(
                {
                    'piece': piece, 
                    'moves': get_potential_king_moves(current_square, board)
                }
            )
    return potential_moves

def get_valid_moves(potential_move_pieces, board):
    valid_move_pieces = []
    current_player = potential_move_pieces[0]['piece']['color']
    for move_piece in potential_move_pieces:
        valid_moves = []
        
        for move in move_piece['moves']:
            piece = get_piece({'x': move['x'], 'y': move['y']}, board)
            if piece != 'empty' and piece['color'] == current_player:
                continue
                
            # Special case
            if move_piece['piece']['type'] == 'king':
                if king_will_be_in_check(current_player, move, board):
                    continue
            valid_moves.append(move)
                    
            # TODO: need to add check if king is pinned
            
        if valid_moves:
            valid_move_pieces.append({'piece': move_piece['piece'], 'moves': valid_moves})
    return valid_move_pieces

# Determine if king will be in check in the square
def king_will_be_in_check(current_player, square, board):
    opponent_player = get_opponent_player(current_player)
    
    # nice trick to check king vs king
    opponent_king = get_king_piece(opponent_player, board)
    opponent_king_square = {'x': opponent_king['x'], 'y': opponent_king['y']}
    next_opponent_king_moves = get_potential_king_moves(opponent_king_square, board)
    
    if square in next_opponent_king_moves:
        return True
    
    for x in range (square['x'] - 1, -1, -1):
        current_square = {'x': x, 'y': square['y']}
        if is_empty(current_square, board):
            continue        
            
        piece = get_piece(current_square, board)
        if piece['color'] == current_player:
            break
        if piece['type']  != 'rook':
            break
        
        # King is in check by rook from the left
        return True
    
    for x in range (square['x'] + 1, board['column'], 1):
        current_square = {'x': x, 'y': square['y']}
        if is_empty(current_square, board):
            continue        
            
        piece = get_piece(current_square, board)
        if piece['color'] == current_player:
            break
        if piece['type']  != 'rook':
            break
        
        # King is in check by rook from the right
        return True
    
    for y in range (square['y'] - 1, -1, -1):
        current_square = {'x': square['x'], 'y': y}
        if is_empty(current_square, board):
            continue        
            
        piece = get_piece(current_square, board)
        if piece['color'] == current_player:
            break
        if piece['type']  != 'rook':
            break
        
        # King is in check by rook from the north
        return True
    
    for y in range (square['y'] + 1, board['row'], 1):
        current_square = {'x': square['x'], 'y': y}
        if is_empty(current_square, board):
            continue        
            
        piece = get_piece(current_square, board)
        if piece['color'] == current_player:
            break
        if piece['type']  != 'rook':
            break
        
        # King is in check by rook from the south
        return True
    return False

# Get piece based on the location    
def get_piece(square, board):
    for piece in board['pieces']:
        if piece['x'] == square['x'] and piece['y'] == square['y']:
            return piece
    return 'empty'

def get_king_piece(color, board):
    for piece in board['pieces']:
        if piece['type'] == 'king' and piece['color'] == color:
            return piece
  

def get_opponent_player(current_player):
    if current_player == 'white':
        return 'black'
    return 'white'

# Get all pieces on the board that belong to the player
def get_pieces(player, board):
    player_pieces = []
    for piece in board['pieces']:
        if piece['color'] == player:
            player_pieces.append(piece)
    return player_pieces

# Determine if a square is empty
def is_empty(square, board):
    for piece in board['pieces']:
        if piece['x'] == square['x'] and piece['y'] == square['y']:
            return False
    return True

# Return true if the board contains only white king and black king
def only_kings_left(board):
    white_pieces = get_pieces('white', board)
    black_pieces = get_pieces('black', board)
    if (len(white_pieces) == 1 and len(black_pieces) == 1 and 
        white_pieces[0]['type'] == 'king' and 
        black_pieces[0]['type'] == 'king'):
        return True
    return False

# Get rook moves as if the board is empty (no pieces on the board)
def get_potential_rook_moves(current_square, board):
    moves = []
    for x in range (board['column']):
        if x != current_square['x']:
            moves.append({'x': x, 'y': current_square['y']})
    for y in range (board['row']):
        if y != current_square['y']:
            moves.append({'x': current_square['x'], 'y': y})
    return moves

# Get rook moves. Obstacles will be taken into account
# Will NOT test if the king is in check after the move
# TODO: handle special case: capture opponent's pieces
def get_valid_rook_moves(piece, board):
    moves = []
    current_x = piece['x']
    current_y = piece['y']
    
    # left
    for x in range (current_x - 1, -1, -1):
        square = {'x': x, 'y': current_y}
        if not is_empty(square, board):
            break      
        moves.append(square)
     
    # right
    for x in range (current_x + 1, board['column'], 1):
        square = {'x': x, 'y': current_y}
        if not is_empty(square, board):
            break      
        moves.append(square)
        
     # up
    for y in range (current_y - 1, -1, -1):
        square = {'x': current_x, 'y': y}
        if not is_empty(square, board):
            break      
        moves.append(square)
        
    # down
    for y in range (current_y + 1, board['row'], 1):        
        square = {'x': current_x, 'y': y}
        if not is_empty(square, board):
            break      
        moves.append(square)
        
    return moves

def get_potential_king_moves(current_square, board):
    moves = []
    current_x = current_square['x']
    current_y = current_square['y']
    
    if current_x > 0:
        moves.append({'x': current_x - 1, 'y': current_y})
    if current_x < board['column'] - 1:
        moves.append({'x': current_x + 1, 'y': current_y})
    if current_y > 0:
        moves.append({'x': current_x, 'y': current_y - 1})
    if current_y < board['row'] - 1:
        moves.append({'x': current_x, 'y': current_y + 1})
        
    if current_x > 0 and current_y > 0:
        moves.append({'x': current_x - 1, 'y': current_y - 1})
    if current_x > 0 and current_y < board['row'] - 1:
        moves.append({'x': current_x - 1, 'y': current_y + 1})
    if current_x < board['column'] - 1 and current_y > 0:
        moves.append({'x': current_x + 1, 'y': current_y - 1})
    if current_x < board['column'] - 1 and current_y < board['row'] - 1:
        moves.append({'x': current_x + 1, 'y': current_y + 1})
    return moves

def piece_type_to_numeric(piece):
    piece_type = piece['type']
    piece_color = piece['color']
    piece_type_num = 0
    
    if piece_color == 'white':
        if piece_type == 'king':
            piece_type_num = 2
        elif piece_type == 'rook':
            piece_type_num = 3
    if piece_color == 'black':
        if piece_type == 'king':
            piece_type_num = 4
        elif piece_type == 'rook':
            piece_type_num = 5
            
    return int(str(piece_type_num))

def board_to_numeric(board):
    board_str = ''
    for y in range(board['row']):
        for x in range(board['column']):
            piece = get_piece({'x': x, 'y': y}, board)
            if piece == 'empty':
                board_str += '1'
                continue
            board_str += str(piece_type_to_numeric(piece))
    return int(board_str)

def move_piece_to_numeric(move_piece):
    piece_type = move_piece['piece']['type']
    piece_color = move_piece['piece']['color']
    piece_type_num = piece_type_to_numeric(move_piece['piece'])
    
    move = move_piece['move']
    return int(str(piece_type_num) + str(move['x']) + str(move['y']))
