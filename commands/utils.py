def get_input(prompt: str, default=None):
    """
    Get input from the user.
    """
    if default:
        return input(f'{prompt} [{default}]: ') or default
    else:
        return input(f'{prompt}: ')
    
def get_input_boolean(prompt: str, default=None):
    """
    Gets a yes or no value from the terminal.
    """
    return get_input(prompt + ' (y/n)', default) == 'y'