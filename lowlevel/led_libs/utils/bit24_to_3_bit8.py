def bit24_to_3_bit8(val):
    """
    Convert 24-bit value to a 3 component 8 bit value
    :param val: 24-bit value
    :return: list of 3 8-bit int components
    """
    # Get binary value without 0b prefix
    bin_val = bin(val)[2:]
    # Get binary value padded with zeros
    bin_val = "0" * (24 - len(bin_val)) + bin_val
    # Extract components as int
    red = int(bin_val[:8], 2)
    green = int(bin_val[8:16], 2)
    blue = int(bin_val[16:24], 2)
    return red, green, blue