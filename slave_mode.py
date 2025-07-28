import socket
import json
import sys
import time


def send_json_tcp():
    """
    Pide IP, puerto y campos de un mensaje JSON, lo envía por TCP y muestra la respuesta.
    """
    print("--- Enviar Mensaje JSON por TCP ---")

    # 1. Solicitar IP y Puerto
    target_ip = "192.168.88.207"
    target_port = 59800
    #
    # 2. Solicitar Campos del Mensaje JSON
    print("\n--- Ingrese los datos para el mensaje JSON ---")

    while True:
        try:
            base_amount = int(input("baseAmount (ej. 23430): ").strip())
            break
        except ValueError:
            print("Entrada inválida. baseAmount debe ser un número entero.")

    while True:
        try:
            tax1_amount = int(input("tax1Amount (ej. 1000): ").strip())
            break
        except ValueError:
            print("Entrada inválida. tax1Amount debe ser un número entero.")

    while True:
        try:
            tax2_amount = int(input("tax2Amount (ej. 0): ").strip())
            break
        except ValueError:
            print("Entrada inválida. tax2Amount debe ser un número entero.")

    tip_amount_input = (
        input("tipAmount (ingrese 'null' o un número, ej. null o 500): ")
        .strip()
        .lower()
    )
    tip_amount = None if tip_amount_input == "null" else int(tip_amount_input)
    # Validar que si no es 'null', sea un número. Si falla, el JSON serializer lo manejará o se puede añadir un try-except aquí.
    if tip_amount_input != "null":
        try:
            tip_amount = int(tip_amount_input)
        except ValueError:
            print(
                "Advertencia: tipAmount ingresado no es 'null' ni un número válido. Se enviará como 'null'."
            )
            tip_amount = None

    token_ecr = input("tokenECR (ej. abcd-176): ").strip()

    start_time = time.time()

    command = "SALE"
    iso_num_code = "0214"

    # Construir el diccionario Python
    message_data = {
        "command": command,
        "isoNumCode": iso_num_code,
        "baseAmount": base_amount,
        "tax1Amount": tax1_amount,
        "tax2Amount": tax2_amount,
        "tipAmount": tip_amount,
        "tokenECR": token_ecr,
    }

    # Convertir el diccionario a una cadena JSON
    try:
        json_message = json.dumps(message_data)
        print(f"\nMensaje JSON a enviar:\n{json_message}")
    except TypeError as e:
        print(
            f"Error al serializar el JSON: {e}. Revise los tipos de datos ingresados."
        )
        sys.exit(1)  # Salir si el JSON no se puede serializar

    # 3. Enviar el JSON por TCP y esperar respuesta
    print(f"\nIntentando conectar a {target_ip}:{target_port}...")
    try:
        # Crear un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Conectar al servidor
            sock.connect((target_ip, target_port))
            print("Conexión establecida. Enviando mensaje...")

            # Enviar el mensaje JSON codificado a bytes (UTF-8 es común)
            sock.sendall(json_message.encode("utf-8"))

            # Esperar y recibir la respuesta
            # Ajusta el tamaño del buffer si esperas respuestas muy grandes
            response_data = b""
            print("Esperando respuesta...")
            # Recibir datos en chunks hasta que no haya más o se cierre la conexión
            while True:
                chunk = sock.recv(4096)  # Recibe hasta 4096 bytes
                if (
                    not chunk
                ):  # Si no hay más datos, la conexión se cerró o se terminó de enviar
                    break
                response_data += chunk

            print("Respuesta recibida.")
            end_time = time.time() - start_time
            print(f"tiempo de respuesta: {end_time:.2f} segundos")
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
            f"Error: La conexión fue rechazada. Asegúrese de que el servidor esté activo y escuchando en {target_ip}:{target_port}."
        )

    except socket.timeout:
        print("Error: Tiempo de espera agotado. El servidor no respondió a tiempo.")

    except socket.gaierror:
        print(
            f"Error: No se pudo resolver la dirección IP '{target_ip}'. Verifique la IP o el nombre de host."
        )

    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    send_json_tcp()
