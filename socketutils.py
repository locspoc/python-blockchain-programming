#socketutils
import socket
import pickle
import select

TCP_PORT = 5005
BUFFER_SIZE = 1024

def newServerConnection(ip_addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip_addr,TCP_PORT))
    s.listen()
    return s

def recvObj(socket):
    inputs,outputs,errs = select.select([socket],[],[socket],6)
    if socket in inputs:
        new_sock,addr = socket.accept()
        all_data = b''
        while True:
            data = new_sock.recv(BUFFER_SIZE)
            if not data: break
            all_data = all_data + data
        return pickle.loads(all_data)
    return None

def sendBlock(ip_addr, blk):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip_addr, TCP_PORT))
    data = pickle.dumps(blk)
    s.send(data)
    s.close()
    return False

if __name__ == "__main__":
    server = newServerConnection('192.168.1.106')
    o = recvObj(server)
    print("Success!") #If returns after time, then successful
    # print(o)
    server.close()
