def process_input(collection):
    if not isinstance(collection, list):
        raise ValueError(
            "{} is not a list nor can it be converted into one".format(
                collection))

    return collection
