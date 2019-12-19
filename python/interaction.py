import backend_logic

print('='*30)
print('Welcome to this Password Manager')
if input('Type 1 to continue'):
  pass_manager_obj = backend_logic.pass_manager('pass_manager.db')
  print('='*30)
  print('These are the options available')
  print('st -> Store Password')
  print('ge -> Get Password')
  print('vw -> View Records')
  print('dl -> Delete Record')
  response = input('Choose your options: ')

  if response == 'st':
    service, username = input('Enter Service and Username here: ').split()
    key = pass_manager_obj.store_password(service, username)
    print('Your Encrypted password for service {} with username {} : {}'.format(service, username, key))

  if response == 'ge':
    service, username = input('Enter Service and Username here: ').split()
    password = pass_manager_obj.get_password(service, username)
    if password:
      print('Your Encrypted password for service {} with username {} : {}'.format(service, username, password))
    else:
      print('Record for service {} and username{} not found'.format(service, username))

  
  if response == 'vw':
      for keys in pass_manager_obj.get_table():
        print(keys)

  if response == 'dl':
    service, username = input('Enter Service and Username here: ').split()
    res = pass_manager_obj.delete_row(service, username)
    print(res)

else:
  print('Try Again Later On')

'''
Todo : 
  1.Collision Control
  2.Multiple User Access
'''