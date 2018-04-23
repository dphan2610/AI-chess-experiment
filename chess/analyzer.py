from collections import Counter
import operator

def analyze(file_name):
    f = open(file_name, 'r')
    
    board_set = set()
    board_list = []
    entries = []
    for line in f:
        elements = line.split('|')
        board = elements[0]
        board_set.add(board)
        board_list.append(board)
        
        entries.append({'board': board, 'action': elements[1], 'result': elements[2]})
    f.close()
    
    for board in board_set:
        board_actions = []
        action_set = set()
        action_results = {}
        
        for entry in entries:
            if board == entry['board']:
                board_actions.append({'action': entry['action'], 'result': entry['result'].replace('\n', '')})
                action_set.add(entry['action'])
        
        for item in action_set:
            result_sum = 0
            count = 0
            for board_action in board_actions:
                if board_action['action'] == item:
                    result_sum += expected_value(board_action['result'])
                    count += 1
                    
            expected_outcome = result_sum / count
            action_results[item] = expected_outcome
            
        best_action = max(action_results.items(), key=operator.itemgetter(1))[0]
        print (board + '|' + best_action)

def expected_value(result):
    if result == '1':
        return 1
    return 0

def binarize(input_file, output_file):
    f = open(input_file, 'r')
    f_out = open(output_file, 'w')
    
    for line in f:
        elements = line.replace('\n', '').split('|')
        board = elements[0]
        action = elements[1]
        
        result = to_binary_by_character(board) + to_binary_by_character(action)
        f_out.write(result + '\n')
    
    f_out.close()
    f.close()
    
# 13F -> 000100111111
def to_binary_by_character(hex_string):
    result = ''
    for c in hex_string:
        result += bin(int(c, 16))[2:].zfill(4)
    return result
