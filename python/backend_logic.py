import sqlite3
import bcrypt
from hashlib import sha256
from master_password import master_password

class pass_manager:

  def __init__(self,file):
    self.file = file
    with sqlite3.connect(file) as conn:
      print('Your Connection has been established')
    conn.close()
    self.create_table()

  def get_cursor(self, cursor=False):
    with sqlite3.connect(self.file, isolation_level=None) as conn:
      if cursor:
        return conn.cursor()

  def create_table(self):
    sql_query = '''
      CREATE TABLE IF NOT EXISTS HASHKEYS(
      SERVICE text NOT NULL,
      USERNAME text,
      SECRET_KEY text,
      BCRYPT_PASSWORD text
      )
    '''
    self.execute_query(sql_query)

  def execute_query(self,sql_query, values_to_insert=None):
    cursor = self.get_cursor(cursor=True)
    if values_to_insert:
      return cursor.execute(sql_query, values_to_insert)
    else:
      return cursor.execute(sql_query)

  def encode_sh2(self, master_password, service):
    return sha256(master_password.encode('utf-8') + service.lower().encode('utf-8')).hexdigest()[:10]
    
  def encode_bcrypt(self, secret_key):
    salt = bcrypt.gensalt(rounds=5)
    return bcrypt.hashpw(secret_key.encode('utf-8'), salt)

  def store_password(self, service, username='root'):
    secret_key = self.encode_sh2(master_password, service)
    bcrypt_key = self.encode_bcrypt(secret_key)
    values_to_insert = (service, username,
      secret_key, bcrypt_key,)
    sql_query = '''
      INSERT INTO HASHKEYS(SERVICE, USERNAME, SECRET_KEY,BCRYPT_PASSWORD) VALUES(?,?,?,?);
    '''
    self.execute_query(sql_query, values_to_insert)
    print('Password Stored Successfully')
    return bcrypt_key
    
  def get_password(self, service, username='root'):
    values_to_insert = (service, username,)
    sql_query = '''
      SELECT * FROM HASHKEYS WHERE SERVICE=(?) AND USERNAME=(?)
    '''
    table = self.execute_query(sql_query, values_to_insert)
    try:
      for row in table:
        key = row
      return key
    except:
      return 0

  def get_table(self):
    sql_query = '''
      SELECT * FROM HASHKEYS
    ''' 
    table = self.execute_query(sql_query)
    for row in table:
      key = row
      yield key

  def delete_row(self, service, username):
    values_to_insert = (service, username,)
    sql_query = '''
      DELETE FROM HASHKEYS WHERE SERVICE=(?) AND USERNAME=(?)
    ''' 
    res = self.execute_query(sql_query, values_to_insert)
    return res