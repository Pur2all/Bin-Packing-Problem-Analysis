import heapq
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
from mpl_toolkits.mplot3d import Axes3D


def bin_pack_mbo(objects, bins, size_of_bins):
    sorted_objects = sorted(objects)[::-1]
    bins_heap = deepcopy(bins)

    heapq.heapify(bins_heap)

    for obj in sorted_objects:
        most_empty_bin = heapq.heappop(bins_heap)
        most_empty_bin += obj
        heapq.heappush(bins_heap, most_empty_bin)

    return sum(abs(size_of_bins - a_bin) for a_bin in bins_heap)


def bin_pack_merging(objects, bins, size_of_bins):
    bins_list = deepcopy(bins)
    bins_length = len(bins_list)
    objects_heap = deepcopy(list(objects))

    heapq.heapify(objects_heap)

    while len(objects_heap) != bins_length:
        first_smaller_object, second_smaller_object = heapq.heappop(objects_heap), heapq.heappop(objects_heap)
        merged_object = first_smaller_object + second_smaller_object
        heapq.heappush(objects_heap, merged_object)

    for i, _ in enumerate(bins_list):
        bins_list[i] += heapq.heappop(objects_heap)

    return sum(abs(size_of_bins - a_bin) for a_bin in bins_list)


def calculate_size_of_bins(objects, number_of_bins, number_of_objects):
    sum_of_objects_size = sum(objects)

    if sum_of_objects_size % number_of_bins != 0:
        rest = sum_of_objects_size % number_of_bins
        i = np.random.randint(0, number_of_objects)
        objects[i] += number_of_bins - rest
        sum_of_objects_size += number_of_bins - rest

    size_of_bins = sum_of_objects_size // number_of_bins

    return size_of_bins


def display_chart(objects_history, bins_history, results):
    fig, ax = plt.subplots(2, 1, figsize=(16, 9), subplot_kw={"projection": "3d"})
    fig.canvas.set_window_title("Bin Packing Problem Analysis")
    ax[0].axis("off")
    row_labels = [f"Bins: {n_bins}, Objects: {n_objects}" for n_bins, n_objects in zip(bins_history, objects_history)]

    ax[0].table(cellText=[(mbo, merging) for mbo, merging in results],
                rowLabels=row_labels,
                colLabels=("MBO Algorithm", "Merging Algorithm"),
                cellLoc="center",
                loc="center",
                colWidths=[.2] * 3)
    ax[1].plot(objects_history, bins_history, list(map(lambda element: element[0], results)), 
               linestyle="None", marker="o", color="red", label="MBO Algorithm")
    ax[1].plot(objects_history, bins_history, list(map(lambda element: element[1], results)), 
               linestyle="None", marker="o", color="blue", label="Merging Algorithm")

    ax[1].set_xlabel("Number of objects to pack")
    ax[1].set_ylabel("Number of bins")
    ax[1].set_zlabel("Value of the execution")

    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    results = []
    objects_history = []
    bins_history = []

    number_of_experiments = int(input("How many experiments do you want to do? "))

    for experiment in range(number_of_experiments):
        print(f"\nExperiment number {experiment + 1}")

        number_of_bins = int(input("Insert number of bins: "))
        number_of_objects = int(input("Insert number of objects to pack: "))

        objects = np.random.randint(1, 1001, size=number_of_objects)

        size_of_bins = calculate_size_of_bins(objects, number_of_bins, number_of_objects)
        bins = [0] * number_of_bins

        mbo_algorithm_result = bin_pack_mbo(objects, bins, size_of_bins)
        merging_algorithm_result = bin_pack_merging(objects, bins, size_of_bins)

        objects_history += [number_of_objects]
        bins_history += [number_of_bins]
        results += [(mbo_algorithm_result, merging_algorithm_result)]

    display_chart(objects_history, bins_history, results)


if __name__ == "__main__":
    main()
