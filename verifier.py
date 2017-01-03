import traceback

MESSAGE = {
    "testdoc": "There's something wrong with the doctests... try running simpletests.py first :)",
    "new_game": "Oh no, new_game isn't working correctly...",
    "dig": "Oh no, dig seems to be wrong...",
    "render": "Oh no, render isn't quite right...",
    "render_ascii": "Oh no, there's something wrong with render_ascii...",
    "nd_dig": "Oh no, nd_dig seems to be wrong...",
    "nd_render": "Oh no, nd_render isn't quite right...",
    "nd_new_game": "Oh no, nd_new_game isn't quite right...",
    "integration_2d": "Oh no, combining multiple operations doesn't work quite right...",
    "integration_nd": "Oh no, combining multiple operations in n dimensions doesn't work quite right..."
}

def verify_helper(running_time, result, input_data, reference):
    TIME_LIMIT = 10.0

    try:
        if float(running_time) >= float(TIME_LIMIT):
            return False, "Your code is too slow... Check your data structures and general approach."

        ok = (result == reference)
        message = "Good job! Everything looks fine." if ok else MESSAGE.get(input_data["function"], str(result))
        return ok, message
    except:
        print traceback.format_exc()
        return False, "Your code could not be verified :( Stack trace is printed above so you can debug."

def verify(output, input_data, gold):
    running_time, result = output

    if running_time is None:
        return False, result

    return verify_helper(running_time, result, input_data, gold)
