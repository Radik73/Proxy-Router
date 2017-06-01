def select(port):
    if port == '8888':
        val = 'Staging'
        return val
    elif port == '8887':
        val = 'Production_like'
        return val
    elif port == '8885':
        val = 'Production'
        return val
    elif port == '8886':
        val = 'Additional_server'
        return val