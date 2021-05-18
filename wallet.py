# Wallet

import socketutils
import transactions
# import signatures
# import time
# import miner
# import threading
import txblock

head_blocks = [None]
wallets = [('localhost',5006)]
miners = [('localhost',5005)]
break_now = False
verbose = False

def StopAll():
    global break_now
    break_now = True

def walletServer(my_addr):
    global head_blocks
    head_blocks = [None]
    server = socketutils.newServerConnection('localhost',5006)
    while not break_now:
        newBlock = socketutils.recvObj(server)
        if isinstance(newBlock,txblock.TxBlock):
            if verbose: print("Rec'd block")
            for b in head_blocks:
                if b == None:
                    if newBlock.previousHash == None:
                        newBlock.previousBlock = b
                        if not newBlock.is_valid():
                            print("Error! newBlock is not valid")
                        else:
                            head_blocks.remove(b)
                            head_blocks.append(newBlock)
                            if verbose: print("Added to head blocks")
                elif newBlock.previousHash == b.computeHash():
                    newBlock.previousBlock = b
                    if not newBlock.is_valid():
                        print("Error! newBlock is not valid")
                    else:
                        head_blocks.remove(b)
                        head_blocks.append(newBlock)
                        if verbose: print("Added to head blocks")
                # TODO What if I add to an earlier (non-head) block?
    server.close()
    return True

def getBalance(pu_key):
    long_chain = txblock.findLongestBlockchain(head_blocks)
    this_block = long_chain
    bal = 0.0
    while this_block != None:
        for tx in this_block.data:
            for addr,amt in tx.inputs:
                if addr == pu_key:
                    bal = bal - amt
            for addr,amt in tx.outputs:
                if addr == pu_key:
                    bal = bal + amt
        this_block = this_block.previousBlock
    return bal

def sendCoins(pu_send, amt_send, pr_send, pu_recv, amt_recv, miner_list):
    newTx = transactions.Tx()
    newTx.add_input(pu_send, amt_send)
    newTx.add_output(pu_recv, amt_recv)
    newTx.sign(pr_send)
    socketutils.sendObj('localhost', newTx)
    return True

if __name__ == "__main__":

    import time
    import miner
    import threading
    import signatures

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

    # t1.join()
    # t2.join()
    # t3.join()

    # print ("Exit successful.")

    #Query balances
    bal1 = getBalance(pu1)
    print ("Balance 1 = " + str(bal1))
    bal2 = getBalance(pu2)
    bal3 = getBalance(pu3)

    #Send coins
    sendCoins(pu1, 1.0, pr1, pu2, 1.0, miners)
    sendCoins(pu1, 1.0, pr1, pu3, 0.3, miners)

    time.sleep(30)

    #Query balances
    new1 = getBalance(pu1)
    print ("Balance 1 = " + str(new1))
    new2 = getBalance(pu2)
    new3 = getBalance(pu3)

    #Verify balances
    if abs(new1-bal1+2.0) > 0.00000001:
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
    
    miner.StopAll()
    StopAll()

    t1.join()
    t2.join()
    t3.join()

    print ("Exit successful.")
