import re

def extract_last_request_response(log_file_path):
    with open(log_file_path, 'r') as file:
        log_data = file.read()

    # Dividir el log en bloques por "Connection has been lost"
    blocks = log_data.split("Connection has been lost")
    
    # Tomar el último bloque que contiene el Request y Response
    last_block = blocks[-2] if len(blocks) > 1 else ""

    # Extraer Request y Response usando expresiones regulares
    request_match = re.search(r'Request(.*?)Response', last_block, re.DOTALL)
    response_match = re.search(r'Response(.*)', last_block, re.DOTALL)

    request_data = request_match.group(1) if request_match else ""
    response_data = response_match.group(1) if response_match else ""

    # Crear diccionarios para Request y Response
    request_dict = {}
    response_dict = {}

    # Procesar Request
    for line in request_data.strip().splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            # Extraer solo el número de la clave
            key_number = re.search(r'\d+', key)
            if key_number:
                request_dict[key_number.group()] = value.strip()

    # Procesar Response
    for line in response_data.strip().splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            # Extraer solo el número de la clave
            key_number = re.search(r'\d+', key)
            if key_number:
                response_dict[key_number.group()] = value.strip()

    return request_dict, response_dict

# Ejemplo de uso
log_file_path = 'ISO.log'
request_dict, response_dict = extract_last_request_response(log_file_path)
if __name__ == "__main__":
    # Ejemplo de uso
    log_file_path = 'ISO.log'
    request_dict, response_dict = extract_last_request_response(log_file_path)
    
    print("Request Dictionary:")
    #print(request_dict)
    for clave, valor in request_dict.items():
        print(f"Valor de '{clave}': {valor}")
    print("\nResponse Dictionary:")
    print(response_dict)
