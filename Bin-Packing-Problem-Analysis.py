import heapq
import matplotlib.pyplot as plt
import numpy as np
import random
from copy import deepcopy


class Bin:
    def __init__(self, capacity):
        self.__capacity = capacity

    def get_remaining_capacity(self):
        return self.__capacity

    def add_object(self, object_to_pack):
        self.__capacity -= object_to_pack

    def __lt__(self, other):
        return False if self.__capacity < other.__capacity else True

    def __repr__(self):
        return f"{self.__capacity}"


def first_algorithm():
    cloned_objects = sorted(deepcopy(objects))[::-1]
    bins_heap = deepcopy(bins)

    heapq.heapify(bins_heap)

    for obj in cloned_objects:
        most_empty_bin = heapq.heappop(bins_heap)
        most_empty_bin.add_object(obj)
        heapq.heappush(bins_heap, most_empty_bin)
        
    return sum(abs(cloned_bin.get_remaining_capacity()) for cloned_bin in bins_heap)


def second_algorithm():
    cloned_bins = deepcopy(bins)
    bins_length = len(cloned_bins)
    cloned_objects = deepcopy(objects)
    heapq.heapify(cloned_objects)

    while len(cloned_objects) != bins_length:
        first_smaller_object, second_smaller_object = heapq.heappop(cloned_objects), heapq.heappop(cloned_objects)
        merged_object = first_smaller_object + second_smaller_object
        heapq.heappush(cloned_objects, merged_object)
    
    for cloned_bin in cloned_bins:
        cloned_bin.add_object(heapq.heappop(cloned_objects))

    return sum(abs(cloned_bin.get_remaining_capacity()) for cloned_bin in cloned_bins)


if __name__ == "__main__":
    number_of_bins = int(input("Insert number of bins: "))
    number_of_objects = int(input("Insert number of objects to pack: "))

    size_of_bins = 1 / number_of_bins
    bins = [Bin(size_of_bins) for _ in range(number_of_bins)]

    objects = [random.randrange(1, 1001) for _ in range(number_of_objects)]
    sum_of_objects_size = sum(objects)
    objects = [obj / sum_of_objects_size for obj in objects] 

    first_algorithm_result = first_algorithm()
    second_algorithm_result = second_algorithm()

    print(f"Value of the execution of the first algorithm: {first_algorithm_result}")
    print(f"Value of the execution of the second algorithm: {second_algorithm_result}")
