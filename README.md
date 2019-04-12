# Neo Python Smart Contract Migration Test

This is an example repo for testing a Smart Contract migration with neo python.

## Contracts

There are two nearly similar contracts that can be imported and executed individually.
Code is base on the neo-python example contracts.

`deployed-contract.py` is the one that will be imported and migrated to a new contract.
`new-contract` is the one that we want to migrate to.

## Test setup

For testing I'm using `neo-local` repo. Comes with

```
  neo-python:
    container_name: neo-python
    depends_on:
      - neo-cli-privatenet-1
      - neo-cli-privatenet-2
      - neo-cli-privatenet-3
      - neo-cli-privatenet-4
      - neo-scan-api
      - neo-scan-sync
    image: 'cityofzion/neo-python:v0.8.4'
    networks:
      - inside
      - host-exposed
    tty: true
    volumes:
      - './smart-contracts:/smart-contracts'
      - './wallets:/wallets'
      - ./container-override-files/neo-python/protocol.privnet.json:/neo-python/neo/data/protocol.privnet.json
      - "/blockchain/sc-migration-test:/sc_migration_test"

```

### Deployment of First contract

```
# open wallet
wallet open neo-privnet.wallet

# build contract 
sc build /sc_migration_test/deployed-contract.py

# deploy contract 
sc deploy /sc_migration_test/deployed-contract.avm True False False 0710 05 --fee=0.01

# enabling sc events logging
config sc-events on

# storing something in the contract
sc invoke 0xe1d955a7a6c2c2af58eb2ea0abf28f3a2a9ee568 add ['AAA', 3] 

# getting the balance
sc invoke 0xe1d955a7a6c2c2af58eb2ea0abf28f3a2a9ee568 balance ['AAA'] 

```

### Getting Script hash of Second contract

```
# new contract
sc build /sc_migration_test/new-contract.py

# issuing deploy to get script hash (not deploying though)
sc deploy /sc_migration_test/new-contract.avm True False False 0710 05 --fee=0.01

# Grabbing the script hash from the output
{
    "hash": "0x0546b7c512bd2fc13d5579b35e5ed84602e576ac",
    "script": "011fc56b6a00527ac46a51527ac468164e656f2e53746f726167652e476574436f6e74657874616a52527ac46a00c30361646487646e0006616464696e67680f4e656f2e52756e74696d652e4c6f676a52c36a51c300c37c680f4e656f2e53746f726167652e476574616a53527ac46a53c36a51c351c3936a54527ac46a52c36a51c300c36a54c35272680f4e656f2e53746f726167652e507574616a54c36c7566616a00c30672656d6f7665876454006a52c36a51c300c37c680f4e656f2e53746f726167652e476574616a53527ac46a52c36a51c300c36a53c36a51c351c3945272680f4e656f2e53746f726167652e507574616a53c36a51c351c3946c7566616a00c30762616c616e6365876421006a52c36a51c300c37c680f4e656f2e53746f726167652e476574616c7566616a00c3076d69677261746587642401174d696772617465206f7065726174696f6e207374617274680f4e656f2e52756e74696d652e4c6f670207106a55527ac401056a56527ac4516a57527ac4136d6967726174656420636f6e747261637420336a58527ac403302e336a59527ac40b6c6f63616c68756d616e336a5a527ac40d6e657840656d61696c2e636f6d6a5b527ac40d74657374206d696772617465336a5c527ac46a51c300c36a55c36a56c36a57c36a58c36a59c36a5ac36a5bc36a5cc3587951795a727551727557795279597275527275567953795872755372755579547957727554727568144e656f2e436f6e74726163742e4d696772617465616a5d527ac411636f6e7472616374206d69677261746564680f4e656f2e52756e74696d652e4c6f676a5dc36c756661006c7566",
    "parameters": [
        "String",
        "Array"
    ],
    "returntype": "ByteArray"
}
```

### Migrating the deployed contract

The script has to be passed in HEX, so add `0x` to the script.

```
sc invoke 0xe1d955a7a6c2c2af58eb2ea0abf28f3a2a9ee568 migrate [0x011fc56b6a00527ac46a51527ac468164e656f2e53746f726167652e476574436f6e74657874616a52527ac46a00c30361646487646e0006616464696e67680f4e656f2e52756e74696d652e4c6f676a52c36a51c300c37c680f4e656f2e53746f726167652e476574616a53527ac46a53c36a51c351c3936a54527ac46a52c36a51c300c36a54c35272680f4e656f2e53746f726167652e507574616a54c36c7566616a00c30672656d6f7665876454006a52c36a51c300c37c680f4e656f2e53746f726167652e476574616a53527ac46a52c36a51c300c36a53c36a51c351c3945272680f4e656f2e53746f726167652e507574616a53c36a51c351c3946c7566616a00c30762616c616e6365876421006a52c36a51c300c37c680f4e656f2e53746f726167652e476574616c7566616a00c3076d69677261746587642401174d696772617465206f7065726174696f6e207374617274680f4e656f2e52756e74696d652e4c6f670207106a55527ac401056a56527ac4516a57527ac4136d6967726174656420636f6e747261637420336a58527ac403302e336a59527ac40b6c6f63616c68756d616e336a5a527ac40d6e657840656d61696c2e636f6d6a5b527ac40d74657374206d696772617465336a5c527ac46a51c300c36a55c36a56c36a57c36a58c36a59c36a5ac36a5bc36a5cc3587951795a727551727557795279597275527275567953795872755372755579547957727554727568144e656f2e436f6e74726163742e4d696772617465616a5d527ac411636f6e7472616374206d69677261746564680f4e656f2e52756e74696d652e4c6f676a5dc36c756661006c7566] 
```


# Migration works unfortunately return values are different

```
# If I normally deploy the contract it returns me the values like this

 > sc invoke 0x0546b7c512bd2fc13d5579b35e5ed84602e576ac balance ['BBB']
 ---------------------------
Test invoke successful
Total operations: 61
Results [{'type': 'ByteArray', 'value': '01'}]
Invoke TX GAS cost: 0.0
Invoke TX fee: 0.0001
----------------------------

neo> [I 190412 11:45:08 EventHub:62] [SmartContract.Execution.Success][7492] [060b418755cdd2bb594a8a58d6c4947e960a1cdb] [tx 52c53d0ad1c2054164a8e0ac85ac8c136bb16dc5d44d72dd104c872c94372001] {'type': 'Array', 'value': [{'type': 'Array', 'value': [{'type': 'ByteArray', 'value': b'2y\x06'}]}, {'type': 'ByteArray', 'value': b'balance'}]}
 
# The migrated coontract however returns

--------------------------
Test invoke successful
Total operations: 7
Results [{'type': 'Array', 'value': [{'type': 'ByteArray', 'value': '327906'}]}, {'type': 'ByteArray', 'value': '62616c616e6365'}]
Invoke TX GAS cost: 0.0
Invoke TX fee: 0.0001
--------------------------

Enter your password to continue and deploy this contract

```

