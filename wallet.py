# Wallet

import socketutils
import transactions
import signatures
import time
import miner
import threading

head_blocks = [None]
wallets = [('localhost',5006)]
miners = [('localhost',5005)]

def walletServer(my_addr):
    return True

    server = socketutils.newServerConnection('localhost',5007)
    for i in range(30):
        newBlock = socketutils.recvObj(server)
        if newBlock:
            break
    server.close()

    for b in head_blocks:
        if newBlock.previousHash == b.computeHash():
            newBlock.previousBlock = b
            head_blocks.remove(b)
            head_blocks.append(newBlock)

    

def getBalance(pu_key):
    return 0.0

def sendCoins(pu_send, amt_send, pr_send, pu_recv, amt_recv, miner_list):
    return True

if __name__ == "__main__":
    miner_pr, miner_pu = signatures.generate_keys()
    t1 = threading.Thread(target=miner.minerServer, args=(('localhost', 5005),))
    t2 = threading.Thread(target=miner.nonceFinder, args=(wallets, miner_pu))
    t3 = threading.Thread(target=walletServer, args=(('localhost',5006),))
    t1.start()
    t2.start()
    t3.start()

    pr1,pu1 = signatures.generate_keys()
    pr2,pu2 = signatures.generate_keys()
    pr3,pu3 = signatures.generate_keys()

    t1.join()
    t2.join()
    t3.join()

    print ("Exit successful.")

    #Query balances
    bal1 = getBalance(pu1)
    bal2 = getBalance(pu2)
    bal3 = getBalance(pu3)

    #Send coins
    sendCoins(pu1, 1.0, pr1, pu2, 1.0, miners)
    sendCoins(pu1, 1.0, pr1, pu3, 0.3, miners)

    #Query balances
    new1 = getBalance(pu1)
    new2 = getBalance(pu2)
    new3 = getBalance(pu3)

    #Verify balances
    if abs(new1-bal1+1.3) > 0.00000001:
        print("Error! Wrong balance for pu1")
    else:
        print("Success. Good balance for pu1")
    if abs(new2-bal2-1.0) > 0.00000001:
        print("Error! Wrong balance for pu2")
    else:
        print("Success. Good balance for pu2")
    if abs(new3-bal3-0.3) > 0.00000001:
        print("Error! Wrong balance for pu3")
    else:
        print("Success. Good balance for pu3")
    
    Miner.break_now=True

    t1.join()
    t2.join()
    t3.join()

    print ("Exit successful.")
