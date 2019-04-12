from boa.interop.Neo.Storage import Get,Put,Delete,GetContext
from boa.interop.Neo.Contract import Migrate, Destroy

def Main(operation, args):

    ctx = GetContext()

    if operation == 'add':
        print("adding")
        balance = Get(ctx, args[0])
        new_balance = balance + args[1]
        Put(ctx, args[0], new_balance)
        return new_balance

    elif operation == 'remove':
        balance = Get(ctx, args[0])
        Put(ctx, args[0], balance - args[1])
        return balance - args[1]

    elif operation == 'balance':
        return Get(ctx, args[0])

    
    elif operation == 'migrate':    
        print("Migrate operation") 
        
        # taken out of neo boa test example
        param_list = bytearray(b'\x07\x10')
        return_type = bytearray(b'\x05')
        properties = 1
        name = 'migrated contract 3'
        version = '0.3'
        author = 'localhuman3'
        email = 'nex@email.com'
        description = 'test migrate3'

        new_contract = Migrate(args[0], param_list, return_type, properties, name, version, author, email, description)
        print("contract migrated")

        return new_contract
                  
    

    return False

def is_valid_addr(addr):

    if len(addr) == 20:
        return True
    return False