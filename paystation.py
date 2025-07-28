import socket  # Used for send commands via tcp sockets
import json  # Used for parse commands and responses
import time  # Used use to calculate the time of a transaction
import sys  # Used to exit the program


# This class is use to simulate the actions made by a PayStation
class PayStation:
    target_ip: str  # POS ip address
    target_port: int  # POS port
    target_timeout: int = 120  # POS timeout
    token_ecr: str = "00000000"  # Sale Token
    batch = {}  # PayStation batch

    def __init__(self, target_ip: str = "0.0.0.0", target_port: int = 59800):
        self.target_ip = target_ip
        self.target_port = target_port

    def send_command(self, command):
        print(f"\nTry to connect to {self.target_ip}:{self.target_port}...")
        try:
            # Start TCP Socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to Socket

                sock.connect((self.target_ip, self.target_port))
                print(f"Conected to {self.target_timeout}:{self.target_port}")

                # Start timer for response
                timer = time.time()

                # Send command encoded int UTF-8
                sock.sendall(command.encode("utf-8"))

                # Wait for response
                response_data = b""
                print("Waiting repose from POS...")

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

                # End timer and print response time
                timer -= time.time()
                print(f"POS Response Time: {timer:.2f}")

                if response_data:
                    try:
                        # Decodificar la respuesta y intentar parsearla como JSON
                        decoded_response = response_data.decode("utf-8")
                        parsed_response = json.loads(decoded_response)
                        print("\n--- Response from POS (JSON) ---")
                        print(
                            json.dumps(parsed_response, indent=4)
                        )  # Pretty print con indentación
                    except json.JSONDecodeError:
                        print("\n--- Response from POS (not valid JSON) ---")
                        print(response_data)
                    except UnicodeDecodeError:
                        print("\n--- Response from POS (cant decode UTF-8) ---")
                        print(
                            response_data
                        )  # Imprime bytes crudos si no se puede decodificar
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
    ps = PayStation()
    while True:
        try:
            user_in = int(
                input("\nBienvenido seleccione una opción:\n[1] Venta\n[2] Cierre\n")
            )
            match user_in:
                case 1:
                    ps.sale(True)
                case 2:
                    ps.close()
        except KeyboardInterrupt:
            print("Sesion Cancelada")
            sys.exit()
        finally:
            input("Sesion Finalizada")
