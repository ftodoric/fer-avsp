import hashlib


def convert_to_hex_string(bin_string):
    hex_string = ""
    for i in range(0, len(bin_string), 4):
        bin_part = bin_string[i] + bin_string[i+1] + \
            bin_string[i+2] + bin_string[i+3]
        hex_string += str(hex(int(bin_part, 2))).replace("0x", "")
    return hex_string


def simhash(text):
    sh = [0 for i in range(128)]
    words = text.split(" ")
    for word in words:
        # get md5 hash
        hash = hashlib.md5()
        hash.update(word.encode(encoding="utf-8"))

        # iterate through hash bits
        k = 0
        for i in range(0, len(hash.hexdigest()), 2):
            hex_digit = hash.hexdigest()[i] + hash.hexdigest()[i+1]
            scale = 16
            num_of_bits = 8
            for bit in bin(int(hex_digit, scale))[2:].zfill(num_of_bits):
                if bit == '1':
                    sh[k] += 1
                else:
                    sh[k] -= 1
                k += 1

    # final step
    for i in range(len(sh)):
        if sh[i] >= 0:
            sh[i] = 1
        else:
            sh[i] = 0

    bin_string = str(sh).replace(", ", "").strip("[]")
    return convert_to_hex_string(bin_string)
