# Miner

import socketutils
import transactions
import txblock
import signatures


wallets = ['localhost']
tx_list = []
head_blocks=[None]


def findLongestBlockchain():
    longest = -1
    long_head = None
    for b in head_blocks():
        current = b
        this_len = 0
        while current != None:
            this_len = this_len + 1
            current = current.previousBlock
        if this_len > longest:
            long_head = b
            longest = this_len
    
    return long_head

def minerServer(my_ip, wallet_list, my_public):
    server = socketutils.newServerConnection(my_ip)
    # Get 2 Txs from wallets
    for i in range(10):
        newTx = socketutils.recvObj(server)
        if isinstance(newTx,transactions.Tx):
            tx_list.append(newTx)
            print("Recd tx")
        if len(tx_list) >= 2:
            break
    # add Txs to new block
    newBlock = txblock.TxBlock(findLongestBlockchain())
    newBlock.addTx(tx_list[0])
    newBlock.addTx(tx_list[1])
    # Compute and add minig reward
    total_in,total_out = newBlock.count_totals()
    mine_reward = transactions.Tx()
    mine_reward.add_output(my_public,25.0+total_in-total_out)
    newBlock.addTx(mine_reward)
    # Find nonce
    for i in range (10):
        print("Finding Nonce...")
        newBlock.find_nonce()
        if newBlock.good_nonce():
            print("Good nonce found")
            break
    if not newBlock.good_nonce():
        print ("Error. Couldn't find nonce")
        return False
    # Send new block
    for ip_addr in wallet_list:
        print("Sending to " + ip_addr)
        socketutils.sendObj(ip_addr, newBlock, 5006)
    head_blocks.remove(newBlock.previousBlock)
    head_blocks.append(newBlock)
    return False

my_pr, my_pu = signatures.generate_keys()
minerServer('localhost', wallets, my_pu)
