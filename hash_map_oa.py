# Name: Brian Chamberlain
# OSU Email: chambbri@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/11/2022
# Description: Creates a hash map data structure with a dynamic array to store elements and open addressing
# for table collisions


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Method clear clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        self.buckets = DynamicArray()  # initialize new dynamic array

        # set all buckets to None
        for _ in range(self.capacity):
            self.buckets.append(None)

        self.size = 0

    def get(self, key: str) -> object:
        """
        Method get returns the value associated with the given key. If the key does not exist it returns None. Quadratic
        Probing is used to find the key
        """
        # quadratic probing required
        bucket = self.hash_function(key) % self.capacity  # find the bucket the key should be in
        quad_probe = 1
        index = self.buckets[bucket]  # initialize index so we do not have to keep calling self
        init_bucket = self.hash_function(key) % self.capacity  # need for quadratic probing as bucket will be updated

        # using quadratic probing, look until we have found key or find a spot bucket with None
        while index is not None and index.key != key:
            bucket = (init_bucket + quad_probe ** 2) % self.capacity
            index = self.buckets[bucket]
            quad_probe += 1

        # if the key was found, return the value
        if index is not None and index.key == key and not index.is_tombstone:
            return self.buckets[bucket].value

        return None  # the key was not found, so return None

    def put(self, key: str, value: object) -> None:
        """
        Method put updates the key/value pair in the hash map. If the given key already exists in the hash map, the
        value is replaced with the new value. The table must be resized if the load factor is >= 0.5 before adding the
        new key/value pair
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required

        if self.table_load() >= 0.5:
            self.resize_table(self.capacity * 2)

        bucket = self.hash_function(key) % self.capacity  # find bucket for key/value pair to be added
        index = self.buckets[bucket]  # save index of array so we do not need to keep calling self

        quad_probe = 1  # initialize quadratic probing parameter
        init_bucket = self.hash_function(key) % self.capacity

        # loop until an empty spot is found or the current index key is the same or the index is a tombstone
        while index is not None and index.key != key and not index.is_tombstone:
            bucket = (init_bucket + quad_probe ** 2) % self.capacity  # use quadratic probing to find empty bucket
            index = self.buckets[bucket]  # update index
            quad_probe += 1  # update quad_probe for next time through loop

        # if the key already exists at the index, replace the value
        if index is not None and index.key == key:
            self.buckets[bucket].value = value

        # if the index contains a tombstone, update the key/value and update is_tombstone to False
        elif index is not None and index.is_tombstone:
            self.buckets[bucket].key = key
            self.buckets[bucket].value = value
            self.buckets[bucket].is_tombstone = False
            self.size += 1  # add one to size since this bucket is no longer a tombstone

        # an empty bucket has been found, add the new key value pair
        else:
            self.buckets[bucket] = HashEntry(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Method remove removes the given key and it's associated value from the hash map. If the key is not in the hash
        map, nothing is done.
        """
        # quadratic probing required
        bucket = self.hash_function(key) % self.capacity  # find the bucket the key should be in
        quad_probe = 1
        index = self.buckets[bucket]  # initialize index so we do not have to keep calling self
        init_bucket = self.hash_function(key) % self.capacity  # need for quadratic probing as bucket will be updated

        # using quadratic probing, look until we have found key or find a spot bucket with None
        while index is not None and index.key != key:
            bucket = (init_bucket + quad_probe ** 2) % self.capacity
            index = self.buckets[bucket]
            quad_probe += 1

        # if the key was found, set the tombstone to true, which removes the key/value pair per ed thread
        if index is not None and index.key == key and not index.is_tombstone:
            self.buckets[bucket].is_tombstone = True
            self.size -= 1  # update size

    def contains_key(self, key: str) -> bool:
        """
        Method contains_key returns True if key is in the hash map, otherwise it returns False.
        """
        # quadratic probing required
        bucket = self.hash_function(key) % self.capacity  # find the bucket the key should be in
        quad_probe = 1
        index = self.buckets[bucket]  # initialize index so we do not have to keep calling self
        init_bucket = self.hash_function(key) % self.capacity  # need for quadratic probing as bucket will be updated

        # using quadratic probing, look until we have found key or find a spot bucket with None
        while index is not None and index.key != key:
            bucket = (init_bucket + quad_probe ** 2) % self.capacity
            index = self.buckets[bucket]
            quad_probe += 1

        # if the key was found, return True
        if index is not None and index.key == key and not index.is_tombstone:
            return True

        return False  # the key was not found, so return False

    def empty_buckets(self) -> int:
        """
        Method empty_buckets returns the number of empty buckets in the hash table.
        """
        empty_buckets = 0

        for bucket in range(self.capacity):
            # a bucket is empty if it is set to None or if it is a tombstone
            if self.buckets[bucket] is None or self.buckets[bucket].is_tombstone:
                empty_buckets += 1  # increase count if either condition is met

        return empty_buckets

    def table_load(self) -> float:
        """
        Method table_load returns the current hash table load factor
        """

        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Method resize_table changes the capacity of the internal hash table, while retaining
        existing key/value pairs. The keys are rehashed so that they are in the proper bucket
        in the new dynamic array.
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1 or new_capacity < self.size:
            return

        new_hash = HashMap(new_capacity, self.hash_function)  # initialize new hash map for copying data

        # loop through buckets in existing array
        for bucket in range(self.capacity):
            # check that there is a key/value pair in the bucket and that it is not a tombstone
            if self.buckets[bucket] is not None and not self.buckets[bucket].is_tombstone:
                # get the key and value once there is a valid one found
                key = self.buckets[bucket].key
                value = self.buckets[bucket].value
                # add value to new hash using put
                new_hash.put(key, value)

        # update properties of the original hash map from new hash map created for resize
        self.buckets = new_hash.buckets
        self.capacity = new_hash.capacity

    def get_keys(self) -> DynamicArray:
        """
        Method get_keys returns a DynamicArray that contains all keys stored in the hash map
        """
        key_array = DynamicArray()  # initiate new array to store keys

        for bucket in range(self.capacity):
            index = self.buckets[bucket]  # set index so we do not keep having to reference bucket
            # verify bucket is not none and that it is not a tombstone
            if index is not None and not index.is_tombstone:
                key_array.append(self.buckets[bucket].key)  # add to the array

        return key_array


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)
    
    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
