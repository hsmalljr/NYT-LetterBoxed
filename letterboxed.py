import pygtrie
import heapq

def read_corpus(filename):
    print('Reading corpus from {}...'.format(filename))
    corpus = pygtrie.CharTrie()
    for word in open(filename, 'r').readlines():
        stripped_word = word.strip()
        if len(stripped_word) > 2:
            corpus[stripped_word] = True
    print('Corpus contains {} words.\n'.format(len(corpus)))
    
    return corpus

#CORPUS = read_corpus('words.txt')
CORPUS = read_corpus('big_words.txt')
# SIDES = [
# 	{'t', 'e', 'd'},
# 	{'v', 'u', 'l'},
# 	{'i', 'h', 'a'},
# 	{'g', 'n', 'r'},
# ]
SIDES = [
    {'r', 'a', 'e'},
    {'u', 'n', 'o'},
    {'q', 'w', 't'},
    {'s', 'm', 'y'},
]
ALL_LETTERS = {letter for side in SIDES for letter in side}

def get_reachable_words():
    print('Finding all reachable words...')
    print('Box:')
    for index, side in enumerate(SIDES):
        print('  * side {} = {}'.format(index + 1, ', '.join(side)))

    reachable_words = set()
    for current_side_index, side in enumerate(SIDES):
        for letter in side:
            reachable_words |= get_reachable_words_helper(current_side_index, letter)

    print('Found {} reachable words.\n'.format(len(reachable_words)))

    return reachable_words
            
def get_reachable_words_helper(current_side_index, current_word):
    reachable_words = {current_word} if CORPUS.has_key(current_word) else set()

    if not CORPUS.has_subtrie(current_word):
	    return reachable_words
    
    for next_side_index, side in enumerate(SIDES):
        if next_side_index == current_side_index:
            continue
        for next_letter in side:
            reachable_words |= get_reachable_words_helper(next_side_index, current_word + next_letter)
    
    return reachable_words

REACHABLE_WORDS = get_reachable_words()

def find_solution_paths():
    paths = []
    for word in REACHABLE_WORDS:
        heapq.heappush(paths, path_and_score([word]))

    max_num_solutions = 50
    max_path_length = 100
    finished_paths = []

    print('Finding {} solutions (of minimal length)...'.format(max_num_solutions))
    while len(paths) > 0:
        if len(finished_paths) >= max_num_solutions:
            return

        _, path = heapq.heappop(paths)
        path_letters = { letter for word in path for letter in word}

        if len(path) > max_path_length:
            continue

        if path_letters == ALL_LETTERS:
            max_path_length = len(path)
            finished_paths.append(path)
            print('{}) {}'.format(len(finished_paths), ' -> '.join(path)))
            continue

        for word in REACHABLE_WORDS:
            if path[-1][-1] == word[0]:
                new_path = path + [word]
                heapq.heappush(paths, path_and_score(new_path))

    print('Done.')

def path_and_score(path):
    num_words_in_path = len(path)
    num_chars_in_path = sum(len(word) for word in path)
    num_distinct_chars_in_path = len({letter for word in path for letter in word})

    # 1) Less words is a better path
    # 2) More distinct letters is a better path
    # 3) Less total letters is a better path
    score = 100000*num_words_in_path - 1000*num_distinct_chars_in_path + num_chars_in_path 
    
    return (score, path)


find_solution_paths()
