import heapq
from heapq import heapify, heappush, heappop

from linkedlist import LinkedList


def _make_data_structures(frames: list, dist_functions):
    """
    Creates an heap of linked list nodes where each node holds a frame.
    The key of the heap is the distance (ascending) between the frame and it's parent (previous frame)
    :param frames: the frames list
    :param dist_functions: distance functions to use as a metric for the heap
    :return: the heap and the attached linked list
    """
    heap = []
    heapify(heap)
    ll = LinkedList()

    for frame in frames:
        ll.insert(frame)

    node = ll.first
    while node != ll.last:
        dist = dist_functions(node.value, node.next.value)
        heappush(heap, (dist, node, node.next))
        node = node.next

    return heap, ll


def _drop_frames(heap, dist_function, dist_threshold):
    """
    Remove from the frames linked list (by using the heap) all the the frames
    which their distance from their parent is less than dist_threshold.
    :return: number of frames dropped
    """
    num_drops = 0
    while True:
        dist, node1, node2 = heappop(heap)

        # the heap might still contain dead values, i.e. distances of deleted frames
        if node1.value is None or node2.value is None:
            continue

        if dist > dist_threshold:
            heappush(heap, (dist, node1, node2))
            break

        node2.value = None  # frame dropped
        num_drops += 1
        node1.next = node2.next

        if node1.next is not None:
            new_dist = dist_function(node1.value, node1.next.value)
            heappush(heap, (new_dist, node1, node1.next))

    return num_drops


def _calc_dist_tolerance(heap):
    """
    :return: the average of the smallest and largest distances between frames in th heap
    """
    largest_dist = heapq.nlargest(1, heap)
    smallest_dist = heapq.nsmallest(1, heap)
    avg_dist = (largest_dist[0][0] + smallest_dist[0][0]) / 2
    return avg_dist


def build_frames_tree(num_of_levels: int, frames: list, dist_function):
    tree_levels = {}
    heap, ll = _make_data_structures(frames, dist_function)

    iter_frames = len(frames)
    i = 0
    while i < num_of_levels:
        level = ll.to_list()
        tree_levels[iter_frames] = level
        try:
            threshold = _calc_dist_tolerance(heap)
            num_dropped = _drop_frames(heap, dist_function, threshold)
            iter_frames = iter_frames - num_dropped
            i += 1
        except IndexError:
            break

    return tree_levels