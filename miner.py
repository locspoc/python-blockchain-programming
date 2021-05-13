# Miner

import socketutils
import transactions
import txblock
import signatures
import threading
import time


wallets = [('localhost',5005)]
tx_list = []
head_blocks=[None]
break_now=False


def findLongestBlockchain():
    longest = -1
    long_head = None
    for b in head_blocks:
        current = b
        this_len = 0
        while current != None:
            this_len = this_len + 1
            current = current.previousBlock
        if this_len > longest:
            long_head = b
            longest = this_len
    
    return long_head

def minerServer(my_addr):
    global tx_list
    global break_now
    head_blocks=[None]
    my_ip, my_port = my_addr
    server = socketutils.newServerConnection(my_ip,my_port)
    # Get Txs from wallets
    while not break_now:
        newTx = socketutils.recvObj(server)
        if isinstance(newTx,transactions.Tx):
            tx_list.append(newTx)
            print("Recd tx")
    return False

def nonceFinder(wallet_list, miner_public):
    global break_now
    # add Txs to new block
    while not break_now:
        newBlock = txblock.TxBlock(findLongestBlockchain())
    # while len (tx_list) <2:
    #     time.sleep(1)
        for tx in tx_list:
            newBlock.addTx(tx)
        # Compute and add minig reward
        total_in,total_out = newBlock.count_totals()
        mine_reward = transactions.Tx()
        mine_reward.add_output(miner_public,25.0+total_in-total_out)
        newBlock.addTx(mine_reward)
        # Find nonce
        print("Finding Nonce...")
        newBlock.find_nonce(10000)
        if newBlock.good_nonce():
            print("Good nonce found")
            # Send new block
            for ip_addr,port in wallet_list:
                print("Sending to " + ip_addr + ":" + str(port))
                socketutils.sendObj(ip_addr, newBlock, 5005)
            head_blocks.remove(newBlock.previousBlock)
            head_blocks.append(newBlock)
    return True

if __name__ == "__main__":

    my_pr, my_pu = signatures.generate_keys()
    t1 = threading.Thread(target=minerServer, args=(('localhost', 5005),))
    t2 = threading.Thread(target=nonceFinder, args=(wallets, my_pu))
    server = socketutils.newServerConnection('localhost',5006)
    t1.start()
    t2.start()
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

    for i in range(30):
        newBlock = socketutils.recvObj(server)
        if newBlock:
            break

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

    time.sleep(20)
    break_now=True
    time.sleep(10)
    server.close()

    t1.join()
    t2.join()

    print("Done!")
