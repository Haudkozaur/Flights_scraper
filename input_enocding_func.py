def encode_input(values, key_name, key_last_name):
    name = values[f'{key_name}']
    last_name = values[f'{key_last_name}']
    name = name.lower().capitalize()
    last_name = last_name.upper()
    return last_name + " " + name
