import socket  # Used for send commands via tcp sockets
import json  # Used for parse commands and responses
import time  # Used use to calculate the time of a transaction
import sys  # Used to exit the program
import threading  # Used for handling the timer in a separate thread
from tqdm import tqdm  # Used for progress bar


# This class is use to simulate the actions made by a PayStation
class PayStation:
    target_ip: str  # POS ip address
    target_port: int  # POS port
    target_timeout: int = 120  # POS timeout
    token_ecr: str = "00000000"  # Sale Token
    batch = {}  # PayStation batch

    # Class initialization
    def __init__(self, target_ip: str = "0.0.0.0", target_port: int = 59800):
        self.target_ip = target_ip
        self.target_port = target_port
        self._timer_thread = None
        self._timer_stop_event = None

    # Starts a timer in a separate thread for long-running operations.
    def _start_timer(self, description: str):
        self._timer_stop_event = threading.Event()
        pbar = tqdm(
            total=0,  # Indefinite progress bar
            bar_format="{desc}: {elapsed}s",
            leave=False,
            dynamic_ncols=True,
            file=sys.stdout,
        )
        pbar.set_description(description)

        def timer_worker(pbar_instance):
            # Update the progress bar every 0.1 seconds until the stop event is set
            while not self._timer_stop_event.is_set():
                pbar_instance.refresh()  # Force a refresh of the progress bar
                time.sleep(0.1)
            pbar_instance.close()

        self._timer_thread = threading.Thread(target=timer_worker, args=(pbar,))
        self._timer_thread.start()

    # Stops the timer thread safely.
    def _stop_timer(self):
        if self._timer_thread and self._timer_thread.is_alive():
            self._timer_stop_event.set()  # Signal the thread to stop
            self._timer_thread.join()  # Wait for the thread to finish

    # Send command to POS via TCP Socket
    def send_command(self, command):
        command = json.dumps(command)  # Convert command to JSON
        try:
            # Start the timer before the blocking connect operation
            self._start_timer(
                f"Try to connect to {self.target_ip}:{self.target_port}..."
            )
            # Start TCP Socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((self.target_ip, self.target_port))
                self._stop_timer()  # Stop the timer after connection
                print(f"\nConected to {self.target_ip}:{self.target_port}")

                # Start timer for response
                timer = time.time()

                # Send command encoded in UTF-8
                sock.sendall(command.encode("utf-8"))

                # Wait for response
                response_data = b""
                # Start the timer again for the response wait
                self._start_timer("Waiting response from POS")

                # Recive data in Chunks until connection closes
                while True:
                    chunk = sock.recv(4096)  # Recive buffer 4096 bytes
                    if (
                        not chunk
                    ):  # If not chunks noting is recived or connection closes
                        break
                    response_data += (
                        chunk  # Add recived chunks to resposne_data payload
                    )

                # Stop the timer and print response time
                self._stop_timer()
                timer_end = time.time() - timer
                print(f"POS Response Time: {timer_end:.2f}")

                if response_data:
                    try:
                        # Decode the response and try to parse it as JSON
                        decoded_response = response_data.decode("utf-8")
                        parsed_response = json.loads(decoded_response)
                        print("\n--- Response from POS (JSON) ---")
                        print(json.dumps(parsed_response, indent=4))
                    except json.JSONDecodeError:
                        print("\n--- Response from POS (not valid JSON) ---")
                        print(response_data)
                    except UnicodeDecodeError:
                        print("\n--- Response from POS (cant decode UTF-8) ---")
                        print(response_data)  # Print raw bytes if it cannot be decoded
                else:
                    print("\nPOS not response")

        except ConnectionRefusedError:
            print(f"Error: POS Conection Refused {self.target_ip}:{self.target_port}.")
        except socket.timeout:
            print("Error: POS TimeOut")
        except socket.gaierror:
            print(f"Error: Cant resolve IP address'{self.target_ip}'.")
        except Exception as e:
            print(f"Unexpected Error: {e}")
        finally:
            # IMPORTANT: Always ensure the timer is stopped in case of an unhandled exception
            self._stop_timer()

    def update_token(self):
        if int(self.token_ecr) < 99999999:
            self.token_ecr = str(int(self.token_ecr) + 1).zfill(8)

    def sale(self, manual: bool = False):
        self.update_token()
        if manual:
            while True:
                try:
                    base_Amount = int(input("Insert Amount: ").strip())
                    break
                except ValueError:
                    print("Invalid Amount has to be a integer value type")

            # WIP Implement TAX an Tip Logic, defaults to 0
            tax1_Amount = 0
            tax2_Amount = 0
            tip_Amount = 0

            # JSON formated command
            command = {
                "command": "SALE",
                "isoNumCode": "0214",
                "baseAmount": base_Amount,
                "tax1Amount": tax1_Amount,
                "tax2Amount": tax2_Amount,
                "tipAmount": tip_Amount,
                "tokenECR": self.token_ecr,
            }
            self.send_command(command)

    def close(self):
        command = {"command": "CLOSE"}
        self.send_command(command)


if __name__ == "__main__":
    greeting = "KPS_Greeter"
    try:
        with open(greeting, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print(f"Error: File '{greeting}' not found.")
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        pass

    ps = PayStation("192.168.100.18")
    while True:
        try:
            user_in = int(input("\nSession Started:\n[1] SALE\n[2] CLOSE\n"))
            match user_in:
                case 1:
                    ps.sale(True)
                case 2:
                    ps.close()
        except KeyboardInterrupt:
            print("Session Cancel")
            sys.exit()
        except ValueError:
            print("Invalid input, please enter a number.")
        finally:
            input("Session Ended\nPress Return to continue...")
