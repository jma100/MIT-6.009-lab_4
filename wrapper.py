import doctest
import time
import traceback
from copy import deepcopy

try:
    import lab
    reload(lab)
except ImportError:
    import solution
    lab = solution

TESTDOC_FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.REPORT_ONLY_FIRST_FAILURE
def testdoc(target):
    if target == "lab":
        results = doctest.testmod(lab, optionflags=TESTDOC_FLAGS, report=False)
    elif target == "readme":
        results = doctest.testfile("readme.md", optionflags=TESTDOC_FLAGS, report=False)
    return results[0] == 0

def checkdoc(kind):
    tests = doctest.DocTestFinder(exclude_empty=False).find(lab)
    for test in tests:
        if test.name == "lab":
            continue
        if kind == "docstrings" and not test.docstring:
            return "Oh no, '{}' has no docstring!".format(test.name)
        if kind == "doctests" and not test.examples:
            return "Oh no, '{}' has no doctests!".format(test.name)
    return {"docstrings": "All functions are documented; great!",
            "doctests": "All functions have tests; great!"}[kind]

def dig(game, *args): # Dig mutates game in place
    result = lab.dig(game, *args)
    return [result, game]

def nd_dig(game, *args):
    result = lab.nd_dig(game, *args)
    return [result, game]

def new_game(num_rows, num_cols, bombs):
    return lab.new_game(num_rows, num_cols, map(tuple, bombs))

def nd_new_game(dims, bombs):
    return lab.nd_new_game(dims, map(tuple, bombs))

def integration_test(game, coords):
    results = []
    for coord in coords:
        results.append([("dig", lab.dig(game, *coord)),
                        ("board", deepcopy(game)),
                        ("render", lab.render(game)),
                        ("render/xray", lab.render(game, True)),
                        ("render_ascii", lab.render_ascii(game)),
                        ("render_ascii/xray", lab.render_ascii(game, True))])
    return results

def integration_test_nd(game, coords):
    results = []
    for coord in coords:
        results.append([("dig", lab.nd_dig(game, coord)),
                        ("board", deepcopy(game)),
                        ("render", lab.nd_render(game)),
                        ("render/xray", lab.nd_render(game, True))])
    return results

def ui_new_game(d):
    r = lab.new_game(d["num_rows"], d["num_cols"], d["bombs"])
    return r

def ui_dig(d):
    game, row, col = d["game"], d["row"], d["col"]
    status, nb_dug = lab.dig(game, row, col)
    return [game, status, nb_dug]

def ui_render(d):
    r = lab.render(d["game"], d["xray"])
    return r

FUNCTIONS = {
    "checkdoc": checkdoc,
    "testdoc": testdoc,
    "new_game": new_game,
    "dig": dig,
    "render": lab.render,
    "render_ascii": lab.render_ascii,
    "nd_new_game": nd_new_game,
    "nd_dig": nd_dig,
    "nd_render": lab.nd_render,
    "integration_2d": integration_test,
    "integration_nd": integration_test_nd
}

def run_test(input_data):
    start_time = time.time()

    try:
        result = FUNCTIONS[input_data["function"]](*input_data["args"])
        return (time.time() - start_time), result
    except ValueError as e:
        return None, e.message
    except:
        return None, traceback.format_exc()
