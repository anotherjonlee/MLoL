def key():
    """
    output: returns an api key from the config.ini file
    """
    
    from configparser import ConfigParser
    
    config = ConfigParser()

    config.read('../src/config.ini')    
    
    return config['api']['key']