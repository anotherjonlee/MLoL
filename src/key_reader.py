def key():

    from configparser import ConfigParser
    
    config = ConfigParser()

    config.read('src/config.ini')
    
    return config['api']['key']