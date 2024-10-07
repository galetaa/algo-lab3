import unittest
import timeit
import random
import string
import os
from student_queue import Student, StudentQueue


class TestStudentQueue(unittest.TestCase):

    def setUp(self):
        self.queue = StudentQueue()
        self.student1 = Student("Иван Иванов", "Группа1", 2, 20, 4.5)
        self.student2 = Student("Петр Петров", "Группа2", 3, 21, 4.2)
        self.student3 = Student("Анна Сидорова", "Группа1", 2, 19, 4.8)

    def test_enqueue_dequeue(self):
        self.queue.enqueue(self.student1)
        self.queue.enqueue(self.student2)
        self.assertEqual(len(self.queue), 2)
        self.assertEqual(self.queue.dequeue(), self.student1)
        self.assertEqual(len(self.queue), 1)

    def test_is_empty(self):
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(self.student1)
        self.assertFalse(self.queue.is_empty())

    def test_front(self):
        self.assertIsNone(self.queue.front())
        self.queue.enqueue(self.student1)
        self.queue.enqueue(self.student2)
        self.assertEqual(self.queue.front(), self.student1)

    def test_reverse(self):
        self.queue.enqueue(self.student1)
        self.queue.enqueue(self.student2)
        self.queue.enqueue(self.student3)
        self.queue.reverse()
        self.assertEqual(self.queue.dequeue(), self.student3)
        self.assertEqual(self.queue.dequeue(), self.student2)
        self.assertEqual(self.queue.dequeue(), self.student1)

    def test_contains(self):
        self.queue.enqueue(self.student1)
        self.queue.enqueue(self.student2)
        self.assertTrue(self.queue.contains(self.student1))
        self.assertFalse(self.queue.contains(self.student3))

    def test_contains_by_name(self):
        self.queue.enqueue(self.student1)
        self.queue.enqueue(self.student2)
        self.assertTrue(self.queue.contains_by_name("Иван Иванов"))
        self.assertFalse(self.queue.contains_by_name("Анна Сидорова"))

    def test_save_load_file(self):
        self.queue.enqueue(self.student1)
        self.queue.enqueue(self.student2)
        self.queue.save_to_file("test_queue.pkl")
        new_queue = StudentQueue()
        new_queue.load_from_file("test_queue.pkl")
        self.assertEqual(len(new_queue), 2)
        self.assertEqual(new_queue.dequeue(), self.student1)
        os.remove("test_queue.pkl")


def generate_random_student():
    return Student(
        ''.join(random.choices(string.ascii_letters, k=10)),
        f"Group{random.randint(1, 5)}",
        random.randint(1, 5),
        random.randint(18, 25),
        round(random.uniform(2.0, 5.0), 1)
    )


def benchmark_enqueue(n):
    queue = StudentQueue()
    for _ in range(n):
        queue.enqueue(generate_random_student())


def benchmark_dequeue(n):
    queue = StudentQueue()
    for _ in range(n):
        queue.enqueue(generate_random_student())
    for _ in range(n):
        queue.dequeue()


def benchmark_reverse(n):
    queue = StudentQueue()
    for _ in range(n):
        queue.enqueue(generate_random_student())
    queue.reverse()


def benchmark_contains(n):
    queue = StudentQueue()
    students = [generate_random_student() for _ in range(n)]
    for student in students:
        queue.enqueue(student)
    for _ in range(n):
        queue.contains(random.choice(students))


def run_benchmarks():
    sizes = [100, 1000, 10000]
    for size in sizes:
        print(f"\nBenchmarks for size {size}:")
        print(f"Enqueue: {timeit.timeit(lambda: benchmark_enqueue(size), number=1):.6f} seconds")
        print(f"Dequeue: {timeit.timeit(lambda: benchmark_dequeue(size), number=1):.6f} seconds")
        print(f"Reverse: {timeit.timeit(lambda: benchmark_reverse(size), number=1):.6f} seconds")
        print(f"Contains: {timeit.timeit(lambda: benchmark_contains(size), number=1):.6f} seconds")


if __name__ == "__main__":
    print("Running tests:")
    unittest.main()
    print("\nRunning benchmarks:")
    run_benchmarks()
