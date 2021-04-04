import hashlib
import simhash


def hash2int(band, hash, band_width):
    bin_hash = simhash.hex_to_bin(hash)
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


if __name__ == '__main__':
    # get texts
    number_of_texts = int(input())
    hashes = []
    for i in range(int(number_of_texts)):
        text = input().strip()
        text_hash = simhash.simhash(text)
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
                h_dist = simhash.hamming_dist(simhash.hex_to_bin(hashes[candidate]),
                                              simhash.hex_to_bin(target_text_hash))
                if h_dist <= max_distance:
                    results.append(i)
            print(len(results))
        else:
            print(0)
