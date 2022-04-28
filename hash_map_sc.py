# Name: Brian Chamberlain
# OSU Email: chambbri@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/11/2022
# Description: Creates a hash map data structure with a dynamic array to store elements and singly linked list
# for table collisions


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
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
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Method clear clears the contents of the hash map. It does not change the underlying hash table capacity
        """
        self.buckets = DynamicArray()  # create new empty dynamic array
        # initialize array with empty SLL at each bucket
        for _ in range(self.capacity):
            self.buckets.append(LinkedList())
        self.size = 0  # reset size

    def get(self, key: str) -> object:
        """
        Method get returns the value associated with the given key. If the key does not exist it returns None
        """
        # loop through the dynamic array (buckets)
        for bucket in range(self.capacity):
            node = self.buckets[bucket].contains(key)  # contains will return an SLL node or none if the key is not in
            # the SLL
            if node is not None and node.key == key:
                return node.value  # key is found and return True
        return None  # there was no match, return None

    def put(self, key: str, value: object) -> None:
        """
        Method put updates the key/value pair in the hash map. If the given key already exists in the hash map, the
        value is replaced with the new value
        """
        bucket = self.hash_function(key) % self.capacity  # find the bucket for the key/value to be added
        node = self.buckets[bucket].contains(key)  # find if the SLL already contains the key

        # if the SLL does contain the key, contains will return the node. Update the value of that node
        if node is not None and node.key == key:
            node.value = value

        # otherwise the key does not exist, so insert the node to the SLL
        else:
            self.buckets[bucket].insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Method remove removes the given key and it's associated value from the hash map. If the key is not in the hash
        map, nothing is done.
        """
        # loop through all buckets. Since contains key does not return the node or bucket that the key is in, we still
        # need to find which key the bucket is in, if it exists
        for bucket in range(self.capacity):
            node = self.buckets[bucket].contains(key)
            if node is not None and node.key == key:
                self.buckets[bucket].remove(key)  # remove node from SLL
                self.size -= 1  # update size

    def contains_key(self, key: str) -> bool:
        """
        Method contains_key returns True if key is in the hash map, otherwise it returns False.
        """
        # loop through the dynamic array (buckets)
        for bucket in range(self.capacity):
            node = self.buckets[bucket].contains(key)  # contains will return an SLL node or none if the key is not in
            # the SLL
            if node is not None and node.key == key:
                return True  # key is found and return True
        return False  # there was no match, return False

    def empty_buckets(self) -> int:
        """
        Method empty_buckets returns the number of empty buckets in the hash table.
        """
        empty_buckets = 0

        # loop through array
        for bucket in range(self.capacity):
            if self.buckets[bucket].length() == 0:
                empty_buckets += 1  # if the length of the SLL is 0, the bucket is empty, increase cnt by 1

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
        # do not do anything if the new capacity is less than 1
        if new_capacity < 1:
            return

        new_array = DynamicArray()  # create the new array
        for _ in range(new_capacity):  # initialize an empty linked list at each element of the new array
            new_array.append(LinkedList())

        # iterate through the existing hash map
        for bucket in range(self.capacity):
            linked_list = self.buckets[bucket]

            # iterate through the linked list at each bucket of the array
            for node in linked_list:
                if node is not None:
                    key = node.key
                    new_bucket = self.hash_function(key) % new_capacity  # rehash the key to the new capacity
                    new_array[new_bucket].insert(key, node.value)  # add the key/value pair to the new array

        self.buckets = new_array  # copy data from the new array
        self.capacity = new_capacity

    def get_keys(self) -> DynamicArray:
        """
        Method get_keys returns a DynamicArray that contains all keys stored in the hash map
        """
        key_array = DynamicArray()  # initialize key array

        # iterate through each bucket in hash map array
        for bucket in range(self.capacity):
            linked_list = self.buckets[bucket]  # initialize singly linked list to loop through

            # loop through linked list nodes
            for node in linked_list:
                if node is not None:
                    key_array.append(node.key)  # add key to key_array

        return key_array


# BASIC TESTING
if __name__ == "__main__":
    """
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets())
    print(m.table_load())
    m.put('hi', 20)
    print(m)
    m.put('hi', 30)
    print(m)
    print(m.contains_key('bye'))
    print(m.empty_buckets())
    print(m.table_load())
    m.clear()
    print(m)
    m.put('hi', 20)
    print(m)
    """

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
