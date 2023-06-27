import subprocess
import socket


def get_available_port():
    # Creating a socket
    new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding socket to a random port and getting the assigned port
    new_socket.bind(('', 0))
    _, port = new_socket.getsockname()

    # Closing the socket
    new_socket.close()

    return port


def run_clients():
    # Getting the number of clients from the user
    num_clients = int(input("Enter the number of clients to run: "))

    # Getting an available port
    port = get_available_port()

    # Starting the server only if the number of clients is greater than 0
    if num_clients > 0:
        # To run server.py
        server_process = subprocess.Popen(['python', 'server.py', str(port)])

        # To run client.py that many times
        for num in range(num_clients):
            subprocess.Popen(['python', 'client.py',  str(port), str(num)])

        # Wait for the server process to finish
        server_process.wait()


if __name__ == '__main__':
    run_clients()
