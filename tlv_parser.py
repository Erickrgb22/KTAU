import binascii

def hex_to_ascii(hex_string):
    """
    Convierte una cadena hexadecimal a su representación ASCII.
    Ignora caracteres que no pueden ser decodificados a ASCII.
    """
    try:
        # Asegurarse de que la cadena hexadecimal tenga una longitud par
        if len(hex_string) % 2 != 0:
            # Esto puede ocurrir si el valor es un solo nibble, lo cual es raro en TLV
            # pero binascii.unhexlify requiere una longitud par.
            # Para simplificar, si es impar, lo tratamos como un error o lo ignoramos.
            # En un caso real, se debería manejar según la especificación TLV.
            return f"[Hex impar: {hex_string}]"

        return binascii.unhexlify(hex_string).decode('ascii', errors='ignore')
    except (binascii.Error, UnicodeDecodeError):
        return f"[No ASCII o error de decodificación: {hex_string}]"

def is_constructed_tag(tag):
    """
    Determina si un tag es un tag construido (contiene otros TLVs).
    Para este ejemplo, basándonos en tu cadena de ejemplo, asumimos que
    los tags 'F1' y 'F2' son construidos.
    En una implementación real, esto se basaría en la especificación TLV
    (ej. EMV: si el quinto bit del primer byte del tag es '1', es construido).
    """
    return tag in ["F0", "F1", "F2"] # Añado "F0" aquí

def parse_tlv_recursive(tlv_string, indent_level=0):
    """
    Analiza una cadena TLV (Tag-Length-Value) de forma recursiva.

    Asume el siguiente formato:
    - Tag: 2 caracteres hexadecimales (representa 1 byte)
    - Length: 2 caracteres hexadecimales (representa 1 byte, indica la longitud del valor en bytes)
    - Value: Cadena hexadecimal. Si el tag es construido, este valor es otra cadena TLV.

    Args:
        tlv_string (str): La cadena TLV a analizar.
        indent_level (int): Nivel de indentación actual para la salida jerárquica.

    Returns:
        list: Una lista de diccionarios, donde cada diccionario representa un TLV.
              Cada diccionario contiene 'tag', 'length' (en decimal), y
              o bien 'value_text' (para tags primitivos) o 'nested_tlvs' (para tags construidos).
              Retorna una lista vacía si la cadena es inválida o está vacía.
    """
    parsed_data = []
    index = 0
    while index < len(tlv_string):
        # Extraer Tag (2 caracteres hexadecimales = 1 byte)
        if index + 2 > len(tlv_string):
            # print(f"Advertencia: Cadena TLV incompleta en el Tag en la posición {index}. Finalizando análisis.")
            break
        tag = tlv_string[index : index + 2].upper() # Convertir a mayúsculas para consistencia
        index += 2

        # Extraer Length (2 caracteres hexadecimales = 1 byte)
        if index + 2 > len(tlv_string):
            # print(f"Advertencia: Cadena TLV incompleta en el Length para el Tag '{tag}' en la posición {index}. Finalizando análisis.")
            break
        length_hex = tlv_string[index : index + 2]
        index += 2

        try:
            # Convertir Length de hex a int (representa la longitud del valor en BYTES)
            length_bytes = int(length_hex, 16)
            # La longitud de la cadena hexadecimal del valor es el doble de la longitud en bytes
            value_length_chars = length_bytes * 2
        except ValueError:
            print(f"Error: Longitud inválida '{length_hex}' para el Tag '{tag}' en la posición {index - 2}. Finalizando análisis.")
            break

        # Extraer Value
        if index + value_length_chars > len(tlv_string):
            print(f"Error: Cadena TLV incompleta en el Value para el Tag '{tag}' (esperado {value_length_chars} chars, quedan {len(tlv_string) - index}) en la posición {index}. Finalizando análisis.")
            break
        value_hex = tlv_string[index : index + value_length_chars]
        index += value_length_chars

        tlv_item = {
            "tag": tag,
            "length": length_bytes, # Longitud en decimal (bytes)
        }

        if is_constructed_tag(tag):
            # Si es un tag construido, parsear el valor recursivamente
            tlv_item["nested_tlvs"] = parse_tlv_recursive(value_hex, indent_level + 1)
        else:
            # Si es un tag primitivo, convertir el valor a texto ASCII
            tlv_item["value_text"] = hex_to_ascii(value_hex)
            tlv_item["value_hex"] = value_hex # Mantener el valor hex original también

        parsed_data.append(tlv_item)
    return parsed_data

def print_tlv_data(data, indent=0):
    """Imprime los datos TLV parseados de forma jerárquica y legible."""
    indent_str = "  " * indent
    for item in data:
        print(f"{indent_str}Tag: {item['tag']}, Length: {item['length']} bytes")
        if "value_text" in item:
            print(f"{indent_str}  Value (ASCII): '{item['value_text']}'")
            print(f"{indent_str}  Value (Hex):   '{item['value_hex']}'")
        elif "nested_tlvs" in item:
            print(f"{indent_str}  Nested TLVs:")
            if not item["nested_tlvs"]:
                print(f"{indent_str}    (Vacío o no pudo ser parseado)")
            else:
                print_tlv_data(item["nested_tlvs"], indent + 1)

# --- Función principal para la interacción con el usuario ---
def main():
    print("--- Analizador TLV Recursivo ---")
    print("Introduce la cadena TLV (solo caracteres hexadecimales, sin espacios):")
    tlv_input = input("> ").strip()

    if not tlv_input:
        print("No se introdujo ninguna cadena TLV.")
        return

    # Validar que la entrada sea solo caracteres hexadecimales
    if not all(c in "0123456789abcdefABCDEF" for c in tlv_input):
        print("Error: La cadena TLV contiene caracteres no hexadecimales. Por favor, introduce solo 0-9, a-f, A-F.")
        return

    print("\nAnalizando la cadena TLV...")
    parsed_result = parse_tlv_recursive(tlv_input)

    if parsed_result:
        print("\n--- Resultado del Análisis TLV ---")
        print_tlv_data(parsed_result)
    else:
        print("No se pudo analizar la cadena TLV o estaba vacía/inválida.")

if __name__ == "__main__":
    main()

