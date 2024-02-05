import os
from time import sleep
from urllib.request import urlopen
from util import ScreenIO, get_screen

network = ScreenIO("network", led=(2, 3), button=4, timeout=5)
server = ScreenIO("server", led=(5, 6), button=13, timeout=10 * 60)

tunnel = ScreenIO("tunnel", led=(17, 27), button=22, timeout=60)


def is_connected():
    try:
        urlopen('http://google.com', timeout=1)
        return True
    except:
        return False


def start_network():
    network.led.danger()
    print("Starting network...")

    while True:
        if is_connected():
            print("Network is connected!")
            network.led.success()
            break

        network.led.warning(1)
        print("No internet connection. Retrying...")


def restart_network():
    print("Restarting network...")
    start_network()


def start_server():
    server.led.danger()
    print("Starting server...")
    os.system(f"cd ~/mcserver && screen -S {server.name} -d -m java -jar -Xms512M -Xmx1008M server.jar nogui")
    server_screen = get_screen(server.name)
    file = open("/home/os/mcserver/logs/latest.log", "w")
    file.close()
    time = 0
    while True:
        with open("/home/os/mcserver/logs/latest.log") as my_file:
            lines = my_file.read()
            if "Done" in lines:
                print("Server started!")
                server.led.success()
                break
            if not server_screen.exists or time > server.timeout:
                print("Failed to start server!")
                server.led.danger()
                break

        server.led.warning(1)
        time += 1


def restart_server():
    print("Restarting server...")
    
    if server.pressed:
        return
    
    if not server.pressed:
        server.pressed = True 

    screen = get_screen(server.name)
    if screen is not None:
        screen.send_commands("stop")
        server.led.warning(3)

    start_server()
    server.pressed = False


def start_port_forward():
    tunnel.led.danger()
    print("Starting port forwarding...")
    os.system(f"cd ~/mcserver && screen -S {tunnel.name} -d -m")
    tunnel_screen = get_screen(tunnel.name)
    tunnel_screen.send_commands("./playit-tunnel > ~/mcserver/tunnel.log ")
    time = 0
    while True:
        with open("/home/os/mcserver/tunnel.log") as my_file:
            lines = my_file.read()
            if "registered" in lines:
                tunnel_screen.kill()
                tunnel.led.warning(1)

                file = open("/home/os/mcserver/tunnel.log", "w")
                file.close()

                os.system(f"cd ~/mcserver && screen -S {tunnel.name} -d -m ./playit-tunnel")
                tunnel.led.warning(3)
                print("Port forwarding started!")
                tunnel.led.success()

                break
            if time > tunnel.timeout or not tunnel_screen.exists or "Error" in lines or "error" in lines:
                tunnel_screen.kill()
                print("Failed to start port forwarding!")
                tunnel.led.danger()
                break

        tunnel.led.warning(1)
        time += 1


def restart_port_forward():
    print("Restarting port forwarding...")
    screen = get_screen(tunnel.name)
    if screen is not None:
        screen.kill()

    start_port_forward()


def main():
    network.button.when_activated = restart_network
    tunnel.button.when_activated = restart_port_forward
    server.button.when_activated = restart_server

    network.led.danger()
    tunnel.led.danger()
    server.led.danger()

    start_network()
    start_port_forward()
    start_server()

    try:
        while True:
            sleep(30)

            if get_screen(server.name) is None:
                restart_server()
                

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == '__main__':
    main()
