import pytds

def db_conn():
    return pytds.connect('host', 'db_name', 'uid', 'pwd')