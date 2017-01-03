"""6.009 Lab 5 -- Mines"""
import copy

def dump(game):
    """Print a human-readable representation of game.

    Arguments:
       game (dict): Game state


    >>> dump({'dimensions': [1, 2], 'mask': [[False, False]], 'board': [['.', 1]]})
    dimensions: [1, 2]
    board: ['.', 1]
    mask:  [False, False]
    """
    lines = ["dimensions: {}".format(game["dimensions"]),
             "board: {}".format("\n       ".join(map(str, game["board"]))),
             "mask:  {}".format("\n       ".join(map(str, game["mask"])))]
    print("\n".join(lines))

def bomb_count(game,row,col):
    """
    Args:
        game (dict): Game state
        row (int): Current row
        col (int0: Current col

    Returns:
        1 or 0 for if a bomb is neighboring the current cell or not

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> bomb_count(game,0,0)
    1
    """
    if 0 <= row < game["dimensions"][0] and 0 <= col < game["dimensions"][1]:
        if game["board"][row][col] == '.':
            return 1
    return 0

def new_game(num_rows, num_cols, bombs):
    """Start a new game.

    Return a game state dictionary, with the "board" and "mask" fields
    adequately initialized.

    Args:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs

    Returns:
       A game state dictionary

    >>> dump(new_game(2, 4, [(0, 0), (1, 0), (1, 1)]))
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, False, False, False]
           [False, False, False, False]
    """
    board = [[0 for i in range(num_cols)] for i in range(num_rows)]
    dims = [num_rows, num_cols]
    game = {"dimensions": dims,
            "board": board,
            "mask": [[False for i in range(num_cols)] for j in range(num_rows)]}
    DELTAS = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)]
    for y in range(num_cols):
        for x in range(num_rows):
            if (x,y) in bombs:
                game["board"][x][y] = '.'
    for y in range(num_cols):
        for x in range(num_rows):
            for dr,dc in DELTAS:
                if game["board"][x][y] != '.' and (x,y) != (x+dr,y+dc):
                    game["board"][x][y] += bomb_count(game,x+dr,y+dc)
    return game

def reveal_neighbors(game,mask,row,col):
    """Recursively reveal neighbors of (row,col) when (row,col) = 0
    Updates game["mask"] to reveal a neighbor then recursively reveals it's neighbors
    as long as the neighbor is within the dimensions of the board and it's not the original cell

    Args:
        game (dict): Game state
        mask (list): current mask
        row (int): Current row
        col (int): Current col

    Returns:
        count (int): A number representing how many cell were reveal for each dig

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> reveal_neighbors(game,game["mask"],0,3)
    4
    """
    DELTAS = [(dr, dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)]
    count = 1
    if mask[row][col] == False:
        mask[row][col] = True
        if game["board"][row][col] == 0:
            for dr,dc in DELTAS:
                drow = row+dr
                dcol = col+dc
                if 0 <= drow < game["dimensions"][0] and 0 <= dcol < game["dimensions"][1] and game["board"][drow][dcol] != '.':
                    count += reveal_neighbors(game,mask,drow,dcol)
        return count
    return 0

def victory_mask(board,dims):
    """Create a list to represent that mask state for a victory: (All cells that are not bombs are True)

    Args:
        board (list): Current board state
        dims (list): Dimensions of the board

    Returns:
        List: Representing the state of the mask is a victory occurs
    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> victory_mask(game["board"],game["dimensions"])
    [[False, True, True, True], [False, False, True, True]]
    """
    return [[board[row][cell] != '.' for cell in range(dims[1])] for row in range(dims[0])]


def dig(game, row, col):
    """Recursively dig up (row, col) and neighboring squares.

    Update game["mask"] to reveal (row, col); then recursively reveal (dig up)
    its neighbors, as long as (row, col) does not contain and is not adjacent to
    a bomb.  Return a pair: the first element indicates whether the game is over
    using a string equal to "victory", "defeat", or "ongoing", and the second
    one is a number indicates how many squares were revealed.

    The first element is "defeat" when at least one bomb is visible on the board
    after digging (i.e. game["mask"][bomb_location] == True), "victory" when all
    safe squares (squares that do not contain a bomb) and no bombs are visible,
    and "ongoing" otherwise.

    Args:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       Tuple[str,int]: A pair of game status and number of squares revealed

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> dig(game, 0, 3)
    ('victory', 4)
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [False, True, True, True]
           [False, False, True, True]

    >>> game = {"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask": [[False, True, False, False],
    ...                  [False, False, False, False]]}
    >>> dig(game, 0, 0)
    ('defeat', 1)
    >>> dump(game)
    dimensions: [2, 4]
    board: ['.', 3, 1, 0]
           ['.', '.', 1, 0]
    mask:  [True, True, False, False]
           [False, False, False, False]
    """
    reveal_count = 0
    if game["board"][row][col] == '.':
        reveal_count += 1
        game["mask"][row][col] = True
        return ("defeat",reveal_count)
    if game["mask"] == victory_mask(game["board"],game["dimensions"]):
        return ("victory",reveal_count)

    
    if game["board"][row][col] != '.' and game["board"][row][col] != 0:
        reveal_count += 1
        game["mask"][row][col] = True
        return ("ongoing",reveal_count)
    mask = game["mask"][:]
    reveal_count = reveal_neighbors(game,mask,row,col)
    if game["mask"] == victory_mask(game["board"],game["dimensions"]):
        return ("victory",reveal_count)
    return ("ongoing", reveal_count)
  
def render(game, xray=False):
    """Prepare a game for display.

    Returns a two-dimensional array (list of lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A 2D array (list of lists)

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, True, False],
    ...                   [False, False, True, False]]}, False)
    [['_', '3', '1', '_'],
     ['_', '_', '1', '_']]

    >>> render({"dimensions": [2, 4],
    ...         "board": [[".", 3, 1, 0],
    ...                   [".", ".", 1, 0]],
    ...         "mask":  [[False, True, False, True],
    ...                   [False, False, False, True]]}, True)
    [['.', '3', '1', ' '],
     ['.', '.', '1', ' ']]
    """
    
    if xray==True:
        render_list = [game["board"][i][:] for i in range(len(game["board"]))]
        for x in range(game["dimensions"][0]):
            for y in range(game["dimensions"][1]):
                if render_list[x][y] == 0:
                    render_list[x][y] = ' '
                else:
                    render_list[x][y] = str(render_list[x][y])
        return render_list
    render_list = [game["board"][i][:] for i in range(len(game["board"]))]
    for x in range(game["dimensions"][0]):
        for y in range(game["dimensions"][1]):
            if game["mask"][x][y] == xray:
                render_list[x][y] = '_'
            if render_list[x][y] == 0:
                render_list[x][y] = ' '
            else:
                render_list[x][y] = str(render_list[x][y])
    return render_list

def render_ascii(game, xray=False):
    """Render a game as ASCII art.

    Returns a string-based representation of argument "game".  Each tile of the
    game board should be rendered as in the function "render(game)".

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       A string-based representation of game

    >>> print(render_ascii({"dimensions": [2, 4],
    ...                     "board": [[".", 3, 1, 0],
    ...                               [".", ".", 1, 0]],
    ...                     "mask":  [[True, True, True, False],
    ...                               [False, False, True, False]]}))
    .31_
    __1_
    """
    render_list = render(game,xray)
    return "\n".join([''.join([item for item in row]) for row in render_list])

def create_nd_board(dims,value):
    """
    Arguments:
        dims (list): List of board dimensions
        value (Any): Value to initialize the board with
    Returns:
        A len(dims)-dimensional	array
    >>>	create_nd_board((1,3,2),42)
    [[[42, 42],	[42, 42], [42, 42]]]

    """

    if dims: return [create_nd_board(dims[1:],value) for i in xrange(dims[0])]
    else: return value

def nd_get_set(board,dims,coord,val=None,get=False):
    """Get or set the value in a N-d array.

    Args:
        board (list): Current board state
        dims (list): Dimensions of board
        coord (tuple): Coordinate of cell to get value of or set value to
        val: Value to put at coord
        get (bool): Default to false to make the function nd_set

    Returns:
        If get==True: The value at that coord
        else: Sets coord to val
    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_get_set(game["board"],game["dimensions"],(1,1,1),val=None)
    [3, None]

    >>> nd_get_set(game["board"],game["dimensions"],(1,1,0),get=True)
    3

    """
    if get==True:
        if len(dims) == 1:
            return board[coord[0]]
        return nd_get_set(board[coord[0]],dims[1:],coord[1:],get=True)
    
    if len(dims) == 1:
        board[coord[0]] = val
        return board
    return nd_get_set(board[coord[0]],dims[1:],coord[1:],val)

def nd_product(ar_list):
    """Produce the Cartesian product of sequences.
    Arguments:
        sequences (list): Sequences to compute the product of

    Returns:
        A list of tuples
    >>>	list(nd_product([(1,2,3), ("a","b")]))
    [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b'), (3, 'a'), (3, 'b')]

    """
    if not ar_list:
        yield ()
    else:
        for a in ar_list[0]:
            for prod in nd_product(ar_list[1:]):
                yield (a,)+prod

def nd_neighbors(dims,coord):
    """Produce all possible neighbors of the current cell including itself.

    Args:
        dims (list): List representing the dimensions of the board
        coord (tuple): Coordinates of cell to find neighbors for

    Returns:
        A list of tuples

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]} 
    >>> sorted(nd_neighbors(game["dimensions"], (1,2,0)))
    [(0, 1, -1), (0, 1, 0), (0, 1, 1), (0, 2, -1), (0, 2, 0), (0, 2, 1), (0, 3, -1), (0, 3, 0), (0, 3, 1), (1, 1, -1), (1, 1, 0), (1, 1, 1), (1, 2, -1), (1, 2, 0), (1, 2, 1), (1, 3, -1), (1, 3, 0), (1, 3, 1), (2, 1, -1), (2, 1, 0), (2, 1, 1), (2, 2, -1), (2, 2, 0), (2, 2, 1), (2, 3, -1), (2, 3, 0), (2, 3, 1)]
    """
    coord_rng = [range(i-1,i+2) for i in coord]
    all_neighbor = list(nd_product(coord_rng))
    return all_neighbor



    

def nd_new_game(dims, bombs):
    """Start a new game.

    Return a game state dictionary, with the "board" and "mask" fields
    adequately initialized.  This is an N-dimensional version of new_game().

    Args:
       dims (list): Dimensions of the board
       bombs (list): bomb locations as a list of tuples, each an N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> dump(nd_new_game([2, 4, 2], [(0, 0, 1), (1, 0, 0), (1, 1, 1)]))
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, False], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
           
    """
    board = create_nd_board(dims, 0)
    game = {"dimensions": dims,
                  "board": board,
                  "mask": create_nd_board(dims, False)}
    for b in bombs:
        nd_get_set(game["board"],dims,b,val= '.')

    coord_rng = [range(i) for i in dims]
    all_coords = list(nd_product(coord_rng))
    for i in all_coords:
        if nd_get_set(game["board"],dims,i,get=True) != '.':
            neighbors = nd_neighbors(dims,i)
            count = 0
            for j in neighbors:
                try:
                    if nd_get_set(game["board"],dims,j,get=True) == '.' and j != i and any(k < 0 for k in j)==False:
                        count += 1
                except:
                    continue
            
            nd_get_set(game["board"],dims,i,count)
    
    
    return game

def nd_reveal_neighbors(game,coords):
    """Recursively reveal neighbors of (row,col) when (row,col) = 0
    Updates game["mask"] to reveal a neighbor then recursively reveals it's neighbors
    as long as the neighbor is within the dimensions of the board and it's not the original cell

    Args:
        game (dict): Game state
        coords (tuple): Coordinates of current cell

    Returns:
        count (int): A number representing how many cell were reveal for each dig

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_reveal_neighbors(game,(0,3,0))
    8
    """
    dims = game["dimensions"]
    neighbors = nd_neighbors(game["dimensions"],coords)
    count = 1
    if nd_get_set(game["mask"],dims,coords,get=True) == False:
        nd_get_set(game["mask"],dims,coords,val=True)
        if nd_get_set(game["board"],dims,coords,get=True) == 0:
            for n in neighbors:
                try:
                    if nd_get_set(game["board"],dims,coords,get=True) != '.' and any(k < 0 for k in n)==False:
                        count += nd_reveal_neighbors(game,n)
                except:
                    continue
        return count
    return 0

def nd_victory_mask(board,dims):
    """Create a list to represent that mask state for a victory: (All cells that are not bombs are True)

    Args:
        board (list): Current board state
        dims (list): Dimensions of the board

    Returns:
        List: Representing the state of the mask is a victory occurs

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_victory_mask(game["board"],game["dimensions"])
    [[[True, False], [True, True], [True, True], [True, True]],
    [[False, True], [True, False], [True, True], [True, True]]]   
    """
    vic_mask = create_nd_board(dims,None)
    coord_rng = [range(i) for i in dims]
    all_coords = list(nd_product(coord_rng))
    for i in all_coords:
        value = nd_get_set(board,dims,i,get=True) != '.'
        nd_get_set(vic_mask,dims,i,val=value)
    return vic_mask


def nd_dig(game, coords):
    """Recursively dig up square at coords and neighboring squares.

    Update game["mask"] to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a pair: the first element indicates whether the game is over
    using a string equal to "victory", "defeat", or "ongoing", and the second
    one is a number indicates how many squares were revealed.

    The first element is "defeat" when at least one bomb is visible on the board
    after digging (i.e. game["mask"][bomb_location] == True), "victory" when all
    safe squares (squares that do not contain a bomb) and no bombs are visible,
    and "ongoing" otherwise.

    This is an N-dimensional version of dig().

    Args:
       game (dict): Game state
       coords (tuple): Where to start digging

    Returns:
       A pair of game status and number of squares revealed

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_dig(game, (0, 3, 0))
    ('ongoing', 8)
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, False], [False, True], [True, True], [True, True]]
           [[False, False], [False, False], [True, True], [True, True]]

    >>> game = {"dimensions": [2, 4, 2],
    ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                  [[False, False], [False, False], [False, False], [False, False]]]}
    >>> nd_dig(game, (0, 0, 1))
    ('defeat', 1)
    >>> dump(game)
    dimensions: [2, 4, 2]
    board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
           [['.', 3], [3, '.'], [1, 1], [0, 0]]
    mask:  [[False, True], [False, True], [False, False], [False, False]]
           [[False, False], [False, False], [False, False], [False, False]]
    """
    reveal_count = 0
    dims = game["dimensions"]
    vic_mask = nd_victory_mask(game["board"],game["dimensions"])
    if nd_get_set(game["board"],dims,coords,get=True) == '.':
        reveal_count += 1
        nd_get_set(game["mask"],dims,coords,val=True)
        return ("defeat",reveal_count)

    if game["mask"] == vic_mask:
        return ("victory",reveal_count)

    curr_coord = nd_get_set(game["board"],dims,coords,get=True)
    if curr_coord != '.' and curr_coord != 0:
        reveal_count += 1
        nd_get_set(game["mask"],dims,coords,val=True)
        return ("ongoing",reveal_count)

    reveal_count = nd_reveal_neighbors(game,coords)
    if game["mask"] == vic_mask:
        return ("victory",reveal_count)
    return ("ongoing", reveal_count)


def nd_render(game, xray=False):
    """Prepare a game for display.

    Returns an N-dimensional array (nested lists) of "_" (hidden squares), "."
    (bombs), " " (empty squares), or "1", "2", etc. (squares neighboring bombs).
    game["mask"] indicates which squares should be visible.  If xray is True (the
    default is False), game["mask"] is ignored and all cells are shown.

    This is an N-dimensional version of render().

    Args:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game["mask"]

    Returns:
       An n-dimensional array (nested lists)

    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
    ...                     [[False, False], [False, False], [True, True], [True, True]]]},
    ...           False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]
     
    >>> nd_render({"dimensions": [2, 4, 2],
    ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...            "mask": [[[False, False], [False, True], [False, False], [False, False]],
    ...                     [[False, False], [False, False], [False, False], [False, False]]]},
    ...           True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    x_game = copy.deepcopy(game)
    dims = game["dimensions"]
    coord_rng = [range(i) for i in dims]
    all_coords = list(nd_product(coord_rng))
    render_list = create_nd_board(dims,0)
    for i in all_coords:
        value = nd_get_set(x_game["board"],dims,i,get=True)
        nd_get_set(render_list,dims,i,val=value)
    if xray==True:
        for i in all_coords:
            if nd_get_set(render_list,dims,i,get=True) == 0:
                nd_get_set(render_list,dims,i,val= ' ')
            else:
                nd_get_set(render_list,dims,i,val=str(nd_get_set(render_list,dims,i,get=True)))
        return render_list
    for i in all_coords:
        if nd_get_set(x_game["mask"],dims,i,get=True) == xray:
            nd_get_set(render_list,dims,i,val= '_')
        if nd_get_set(render_list,dims,i,get=True) == 0:
            nd_get_set(render_list,dims,i,val= ' ')
        else:
            nd_get_set(render_list,dims,i,val=str(nd_get_set(render_list,dims,i,get=True)))
    return render_list

