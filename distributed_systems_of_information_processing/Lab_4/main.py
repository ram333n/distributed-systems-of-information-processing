import mmh3
from bitarray import bitarray

class BloomFilter:
    def __init__(self, size, hash_count):
        self.size = size
        self.hash_count = hash_count
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def add(self, element):
        for i in range(self.hash_count):
            idx_to_set = mmh3.hash(element, i) % self.size
            self.bit_array[idx_to_set] = True

    def contains(self, element):
        for i in range(self.hash_count):
            idx_to_check = mmh3.hash(element, i) % self.size

            if not self.bit_array[idx_to_check]:
                return False

        return True


def main():
    item_1 = 'Hello'
    item_2 = 'World'
    item_3 = "Some random string"
    bloom_filter = BloomFilter(100, 3)

    print(f'Contains item_1={item_1}: {bloom_filter.contains(item_1)}')
    print(f'Contains item_2={item_2}: {bloom_filter.contains(item_2)}')

    bloom_filter.add(item_1)

    print(f'Contains item_1 after insert item_1: {item_1}: {bloom_filter.contains(item_1)}')
    print(f'Contains item_2 after insert item_1: {item_2}: {bloom_filter.contains(item_2)}')

    bloom_filter.add(item_2)

    print(f'Contains item_1 after insert item_2: {item_1}: {bloom_filter.contains(item_1)}')
    print(f'Contains item_2 after insert item_2: {item_2}: {bloom_filter.contains(item_2)}')

    print(f'Contains item_3={item_3}: {bloom_filter.contains(item_3)}')

if __name__ == '__main__':
    main()