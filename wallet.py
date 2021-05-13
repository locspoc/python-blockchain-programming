# Wallet

import socketutils
import transactions
import signatures

head_blocks = [None]

pr1,pu1 = signatures.generate_keys()
pr2,pu2 = signatures.generate_keys()
pr3,pu3 = signatures.generate_keys()

Tx1 = transactions.Tx()
Tx2 = transactions.Tx()

Tx1.add_input(pu1, 4.0)
Tx1.add_input(pu2, 1.0)
Tx1.add_output(pu3, 4.8)
Tx2.add_input(pu3, 4.0)
Tx2.add_output(pu2, 4.0)
Tx2.add_reqd(pu1)

Tx1.sign(pr1)
Tx1.sign(pr2)
Tx2.sign(pr3)
Tx2.sign(pr1)

try:
    socketutils.sendObj('localhost', Tx1)
    print("Sent Tx1")
    socketutils.sendObj('localhost', Tx2)
    print("Sent Tx2")
except:
    print("Error! Connection unsuccessful")

server = socketutils.newServerConnection('localhost',5005)
for i in range(30):
    newBlock = socketutils.recvObj(server)
    if newBlock:
        break
server.close()

if newBlock.is_valid():
    print("Success! Block is valid")
if newBlock.good_nonce():
    print("Success! Nonce is valid")
for tx in newBlock.data:
    try:
        if tx.inputs[0][0] == pu1 and tx.inputs[0][1] == 4.0:
            print("Tx1 is present")
    except:
        pass
    try:
        if tx.inputs[0][0] == pu3 and tx.inputs[0][1] == 4.0:
            print("Tx2 is present")
    except:
        pass

for b in head_blocks:
    if newBlock.previousHash == b.computeHash():
        newBlock.previousBlock = b
        head_blocks.remove(b)
        head_blocks.append(newBlock)

# Add newBlock to blockchain
