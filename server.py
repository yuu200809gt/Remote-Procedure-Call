import socket
import os
import json
import math

# ====== 呼び出し可能なメソッドを定義 ======
class Callable:
    @staticmethod
    def floor(args):
        x = float(args[0])
        return math.floor(x)

    @staticmethod
    def nroot(args):
        n = int(args[0])
        x = int(args[1])
        return x ** (1 / n)

    @staticmethod
    def reverse(args):
        return args[0][::-1]

    @staticmethod
    def validAnagram(args):
        str1 = args[0].replace(" ", "").lower()
        str2 = args[1].replace(" ", "").lower()

        if len(str1) != len(str2):
            return False

        count = [0] * 26
        for a, b in zip(str1, str2):
            count[ord(a) - 97] += 1
            count[ord(b) - 97] -= 1

        return all(c == 0 for c in count)

    @staticmethod
    def sort(args):
        return sorted(args)

# ====== ソケットサーバのメイン処理 ======
def main():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_address = '/tmp/socket_file.sock'

    try:
        os.unlink(server_address)
    except FileNotFoundError:
        pass

    print('Start up on {}'.format(server_address))
    sock.bind(server_address)
    sock.listen(1)

    method_table = {
        'floor': Callable.floor,
        'nroot': Callable.nroot,
        'reverse': Callable.reverse,
        'validAnagram': Callable.validAnagram,
        'sort': Callable.sort,
    }

    while True:
        print('Waiting for a connection...')
        connection, _ = sock.accept()

        try:
            print('Client connected.')

            data = connection.recv(1024)
            if not data:
                print('No data received')
                return

            request = json.loads(data.decode('utf-8'))
            method = request.get('method')
            params = request.get('params', [])
            request_id = request.get('id', 1)

            if method in method_table:
                result = method_table[method](params)
                response = {
                    'result': result,
                    'result_type': type(result).__name__,
                    'id': request_id
                }
            else:
                response = {
                    'result': None,
                    'error': 'Unknown method',
                    'id': request_id
                }

            connection.sendall(json.dumps(response).encode())

        except Exception as e:
            print('Error:', e)

        finally:
            print('Closing connection...')
            connection.close()

if __name__ == '__main__':
    main()
