def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def convert_from_string(string: str, size: int = 9):
    return [[int(i) for i in line] for line in chunks(lst=string, n=size)]
