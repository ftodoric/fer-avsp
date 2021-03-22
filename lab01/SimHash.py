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


def hex_to_bin(hex_str):
    bin_str = ""
    for i in range(0, len(hex_str), 2):
        bin_str += bin(int((hex_str[i] + hex_str[i+1]),
                       16)).replace("0b", "").zfill(8)
    return bin_str


def hamming_dist(bin_str1, bin_str2):
    h_dist = 0
    for i in range(len(bin_str1)):
        if bin_str1[i] != bin_str2[i]:
            h_dist += 1
    return h_dist


def main():
    # get texts
    number_of_texts = int(input())
    hashes = []
    sorted_hashes = []
    for i in range(int(number_of_texts)):
        text = input().strip()
        text_hash = hex_to_bin(simhash(text))
        hashes.append(text_hash)
        sorted_hashes.append(text_hash)

    sorted_hashes.sort()

    # get queries
    number_of_queries = int(input())
    for i in range(int(number_of_queries)):
        query = input().strip().split(" ")

        # process the query
        text_index = int(query[0])
        max_distance = int(query[1])
        target_text_hash = hashes[text_index]
        results = []
        for i in range(len(hashes)):
            if i == text_index:
                continue
            h_dist = hamming_dist(hashes[i], target_text_hash)
            if h_dist <= max_distance:
                results.append(i)
        print(len(results))


main()
