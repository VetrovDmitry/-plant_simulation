def XOR(*args):
    response = None
    for arg in args:
        if arg is False:
            response = False
            return response
        else:
            pass
    response = True
    return response

    
if __name__ == "__main__":
    print(XOR(True, True, False))