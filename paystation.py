import socket  # Used for send commands via tcp sockets
import json  # Used for parse commands and responses
import time  # Used use to calculate the time of a transaction


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
                        print("\n--- Respuesta del Servidor (JSON formateado) ---")
                        print(
                            json.dumps(parsed_response, indent=4)
                        )  # Pretty print con indentación
                    except json.JSONDecodeError:
                        print("\n--- Respuesta del Servidor (no es JSON válido) ---")
                        print(response_data)
                    except UnicodeDecodeError:
                        print(
                            "\n--- Respuesta del Servidor (no se pudo decodificar UTF-8) ---"
                        )
                        print(
                            response_data
                        )  # Imprime bytes crudos si no se puede decodificar
                else:
                    print("\nNo se recibió respuesta del servidor.")

        except ConnectionRefusedError:
            print(
                f"Error: La conexión fue rechazada. Asegúrese de que el servidor esté activo y escuchando en {self.target_ip}:{self.target_port}."
            )

        except socket.timeout:
            print("Error: Tiempo de espera agotado. El servidor no respondió a tiempo.")

        except socket.gaierror:
            print(
                f"Error: No se pudo resolver la dirección IP '{self.target_ip}'. Verifique la IP o el nombre de host."
            )

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def update_token(self):
        if int(self.token_ecr) < 99999999:
            self.token_ecr = str(int(self.token_ecr) + 1).zfill(8)

    def sale(self):
        pass  # Implementar lógica de venta aquí

    def close(self):
        pass  # Implementar logica de venta


if __name__ == "__main__":
    sales = 100
    ps = PayStation()
    while sales > 0:
        ps.update_token()
        print(ps.token_ecr)
        sales -= 1
