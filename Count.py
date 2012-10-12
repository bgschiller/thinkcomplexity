def count_maker(digitgen, first_is_zero=True):
    '''Given an iterator which yields the str(digits) of a number system and counts using it. 
    first_is_zero reflects the truth of the statement "this number system begins at zero" It should only be turned off for something like a label system.'''
    def counter(n):
        i = 0
        for val in count(digitgen, first_is_zero):
            yield val
            if i > n:
                break
            i += 1
    return counter

def count(digitgen, first_is_zero=True):
    '''Takes an iterator which yields the digits of a number system and counts using it.
	If first_is_zero is True, digitgen begins counting with a zero, so when we roll over to a new place, the first value in the new place should be the element following zero.
	compare the two test cases for a better understanding.'''
    
    def subcount(digitgen, places):
        if places == 1:
            for d in digitgen():
                yield d
        else:
            for d in digitgen():
                for ld in subcount(digitgen, places - 1):
                    yield d + ld
                    
    for d in digitgen():
        yield d
    
    places = 2
    while True:
        first = first_is_zero
        for d in digitgen():
            if first:
                first = False
                continue
            for ld in subcount(digitgen, places - 1):
                yield d + ld
        places += 1

if __name__ == "__main__":
    import string
    def labelelements():
        for char in string.ascii_lowercase:
            yield char
        for char in string.ascii_uppercase:
            yield char
    
    def base2():
        for d in range(2):
            yield str(d)

    label_counter = count_maker(labelelements, first_is_zero=False)

    for label in label_counter(200):
        print label

    base2_counter = count_maker(base2, first_is_zero=True)
    for b2 in base2_counter(200):
        print b2

