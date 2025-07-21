import iso8583
from iso8583.specs import default_ascii as spec

# encoded_raw = b"02004000000000000000101234567890"
# isomensage_raw = b"02003238058020c1861c000000000000001000071011241900681111241907100070000200374222740436100791d23121190000005700000f3030303030303035303030303030303136373339313030310003303031323134002530303030303030303030303030303030303030303030303030303038333001365f2a0202145f340100820220008407a0000000031010950500000000009a032507109c01009f02060000000010009f03060000000000009f0902008c9f100706010a03a028009f1a0202149f1e0834303331383035349f2608c9e147704b277bac9f2701809f3303e0b0c89f34031f03009f3501229f360202219f3704b673baaa9f41040000681100284b2d5350532d444f2d30322e38302e3802e3031412e342e322e34390010313234303331383035340006303030333538"
# decoded, encoded = iso8583.decode(encoded_raw, spec)
# iso8583.pp(decoded, spec)
# iso8583.pp(encoded, spec)


# Return the Active Data Element Fields list from the bitmap
def decode_bitmap(bitmap: str) -> list[int]:
    # If the func is called with an empty bitmap, return an empty list
    if not bitmap:
        return []
    # Convert the hex string to bytes
    bitmap_bytes = bytes.fromhex(bitmap)
    # Active Fields list
    active_fields = []
    for i, byte_value in enumerate(bitmap_bytes):
        for bit_position in range(8):
            field_number = i * 8 + bit_position + 1
            if byte_value & (1 << (7 - bit_position)):
                active_fields.append(field_number)
    return active_fields


mti = "0200"
bitmap = "3238058020c1861c"
print(bitmap)
decoded_bitmap = decode_bitmap(bitmap)
print(f"Decoded Bitmap: {decoded_bitmap}")

msg = mti + bitmap + 
