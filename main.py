import socket
import sys
from threading import Thread


def process_client_request(connection, address):
    with connection:
        print('connected by', address)
        while True:
            data = connection.recv(1024)
            if not data:
                print('no more data, close connection')
                break
            connection.send(data)


HOST = None
PORT = 50007

if __name__ == '__v4__':

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
        socket.bind((HOST, PORT))
        socket.listen()
        connection, address = socket.accept()

        with connection:
            print('connected by client at', address)
            while True:
                data = connection.recv(1024)
                print(data)
                if not data:
                    print('No data!')
                    break

                connection.sendall(data)


if __name__ == '__main__':
    main_socket = None

    for result in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = result
        print(f'af: {af}, socktype: {socktype}, proto: {proto}, canonname: {canonname}, sa: {sa}')
        try:
            main_socket = socket.socket(af, socktype, proto)
        except OSError as msg:
            print('try next')
            main_socket = None
            continue
        try:
            main_socket.bind(sa)
            while True:
                main_socket.listen(10)
                connection, address = main_socket.accept()
                Thread(target=process_client_request, args=(connection, address)).start()
        except OSError as msg:
            print('try next')
            main_socket.close()
            main_socket = None
            continue

        break


    if main_socket is None:
        print('could not open socket')
        sys.exit(1)




