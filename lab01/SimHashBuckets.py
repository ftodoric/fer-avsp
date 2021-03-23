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


def hash2int(band, hash, band_width):
    bin_hash = hex_to_bin(hash)
    start = (band - 1)*band_width
    end = start + band_width
    return int(bin_hash[start:end], 2)


def lsh(hashes, N):
    NUM_OF_BANDS = 8
    SIMHASH_LEN = 128
    BAND_WIDTH = int(SIMHASH_LEN/NUM_OF_BANDS)

    candidates = {}

    for band in range(1, NUM_OF_BANDS + 1):
        partitions = {}
        for current_id in range(0, N):
            # pick hash and get integer value of hash band
            hash = hashes[current_id]
            val = hash2int(band, hash, BAND_WIDTH)

            # update candidates
            partition_texts = set()
            if val in partitions:
                partition_texts = partitions[val].copy()
                for text_id in partition_texts:
                    if current_id in candidates:
                        candidates[current_id].add(text_id)
                    else:
                        candidates[current_id] = {text_id}
                    if text_id in candidates:
                        candidates[text_id].add(current_id)
                    else:
                        candidates[text_id] = {current_id}
            else:
                partition_texts = set()

            partition_texts.add(current_id)
            partitions[val] = partition_texts.copy()

    return candidates


def main():
    # get texts
    number_of_texts = int(input())
    hashes = []
    for i in range(int(number_of_texts)):
        text = input().strip()
        text_hash = simhash(text)
        hashes.append(text_hash)

    candidates = lsh(hashes, number_of_texts)

    # get queries
    number_of_queries = int(input())
    for i in range(int(number_of_queries)):
        query = input().strip().split(" ")

        # process the query
        text_index = int(query[0])
        max_distance = int(query[1])
        target_text_hash = hashes[text_index]
        results = []
        if text_index in candidates:
            for candidate in candidates[text_index]:
                if candidate == text_index:
                    continue
                h_dist = hamming_dist(hex_to_bin(hashes[candidate]),
                                      hex_to_bin(target_text_hash))
                if h_dist <= max_distance:
                    results.append(i)
            print(len(results))
        else:
            print(0)


main()
