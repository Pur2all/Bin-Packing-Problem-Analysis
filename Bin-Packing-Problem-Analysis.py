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


def get_i_star(number_of_objects, objects, number_of_bins):
    i_star = -1

    for i in range(number_of_objects):
        remanings_sum = sum(objects[i + 1:])
        quantity = remanings_sum / (number_of_bins - i)

        if objects[i] > quantity:
            i_star = i
        else:
            break
    
    return i_star + 1


def display_chart(object_history):
    history = np.array(object_history)
    fig, ax = plt.subplots(2, 1, figsize=(16, 9))
    ax[0].axis("off")
    row_labels = [f"Bins: {n_bins}, Objects: {n_objects}" for n_bins, n_objects in zip(bins_history, history)]
    table = ax[0].table(cellText=[(first, second, lower_bound) for first, second, lower_bound in results], 
                        rowLabels=row_labels, 
                        colLabels=("First Algorithm", "Second Algorithm", "Lower Bound"),
                        cellLoc="center", 
                        loc="center",
                        colWidths=[.2] * 3)
    ax[1].plot(history, np.array(list(map(lambda element: element[0], results))), marker="o", color="red", label="first algorithm")
    ax[1].plot(history, np.array(list(map(lambda element: element[1], results))), marker="o", color="blue", label="second algorithm")
    ax[1].plot(history, np.array(list(map(lambda element: element[2], results))), marker="o", color="green", label="lower bound")
    ax[1].set_ylabel("Value of the execution")
    ax[1].set_xlabel("Number of objects to pack")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    results = []
    objects_history = []
    bins_history = []
    
    number_of_experiments = int(input("How many experiments do you want to do? "))

    for experiment in range(number_of_experiments):
        print(f"\nExperiments number {experiment + 1}")

        number_of_bins = int(input("Insert number of bins: "))
        number_of_objects = int(input("Insert number of objects to pack: "))

        size_of_bins = 1 / number_of_bins
        bins = [Bin(size_of_bins) for _ in range(number_of_bins)]

        objects = [random.randrange(1, 1001) for _ in range(number_of_objects)]
        sum_of_objects_size = sum(objects)
        objects = [obj / sum_of_objects_size for obj in objects]
        
        first_algorithm_result = first_algorithm()
        second_algorithm_result = second_algorithm()

        temp_objects = sorted(deepcopy(objects))[::-1]
        
        if temp_objects[0] < size_of_bins:
            r_vector = [size_of_bins] * number_of_bins
        else:
            i_star = get_i_star(number_of_objects, temp_objects, number_of_bins)

            r_vector = temp_objects[:i_star]

            if i_star < number_of_bins: 
                remainings_sum = sum(temp_objects[i_star:])
                value = remainings_sum / (number_of_bins - i_star)
                r_vector += [value] * (number_of_bins - i_star)

        r_vector_result = sum(abs(size_of_bins - value) for value in r_vector)

        objects_history += [number_of_objects]
        bins_history += [number_of_bins]
        results += [(first_algorithm_result, second_algorithm_result, r_vector_result)]

    display_chart(objects_history)
