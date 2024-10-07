import unittest
import timeit
import random
import string
import os
from car_avl_tree import Car, AVLTree


class TestAVLTree(unittest.TestCase):

    def setUp(self):
        self.avl_tree = AVLTree()

        self.car1 = Car("Toyota", "JT2BF22K1W0123456", 2.0, 25000, 180)
        self.car2 = Car("Honda", "1HGCM82633A004852", 1.8, 22000, 175)
        self.car3 = Car("Ford", "1FAHP3EN2AW123456", 2.5, 28000, 190)

    def test_insert_and_search(self):
        self.avl_tree.insert(self.car1)
        self.avl_tree.insert(self.car2)

        self.assertEqual(self.avl_tree.search(25000), self.car1)
        self.assertEqual(self.avl_tree.search(22000), self.car2)
        self.assertIsNone(self.avl_tree.search(30000))

    def test_delete(self):
        self.avl_tree.insert(self.car1)
        self.avl_tree.insert(self.car2)
        self.avl_tree.insert(self.car3)

        self.avl_tree.delete(25000)

        self.assertIsNone(self.avl_tree.search(25000))
        self.assertIsNotNone(self.avl_tree.search(22000))
        self.assertIsNotNone(self.avl_tree.search(28000))

    def test_contains(self):
        self.avl_tree.insert(self.car1)
        self.avl_tree.insert(self.car2)

        self.assertTrue(self.avl_tree.contains(self.car1))
        self.assertTrue(self.avl_tree.contains(self.car2))
        self.assertFalse(self.avl_tree.contains(self.car3))

    def test_contains_by_vin(self):
        self.avl_tree.insert(self.car1)
        self.avl_tree.insert(self.car2)

        self.assertTrue(self.avl_tree.contains_by_vin("JT2BF22K1W0123456"))
        self.assertTrue(self.avl_tree.contains_by_vin("1HGCM82633A004852"))
        self.assertFalse(self.avl_tree.contains_by_vin("1FAHP3EN2AW123456"))

    def test_save_load_file(self):
        self.avl_tree.insert(self.car1)
        self.avl_tree.insert(self.car2)

        self.avl_tree.save_to_file("test_avl_tree.pkl")

        new_avl_tree = AVLTree()

        new_avl_tree.load_from_file("test_avl_tree.pkl")

        self.assertTrue(new_avl_tree.contains(self.car1))
        self.assertTrue(new_avl_tree.contains(self.car2))

        os.remove("test_avl_tree.pkl")

    def test_balance(self):
        for i in range(1, 8):
            self.avl_tree.insert(Car(f"Brand{i}", f"VIN{i}", 2., i * 10000, 180))

        self.assertEqual(self.avl_tree.root.height, 3)

    def test_duplicate_insert(self):
        self.avl_tree.insert(self.car1)
        self.avl_tree.insert(Car("Toyota2", "JT2BF22K1W0123456", 2., 25000, 180))

        found_car = self.avl_tree.search(25000)

        self.assertEqual(found_car.vin, "JT2BF22K1W0123456")


def generate_random_car():
    return Car(
        ''.join(random.choices(string.ascii_uppercase, k=5)),
        ''.join(random.choices(string.ascii_uppercase + string.digits, k=17)),
        round(random.uniform(1.0, 5.0), 1),
        round(random.uniform(10000, 100000), -3),
        round(random.uniform(120, 250), 0))


def benchmark_insert(n):
    avl_tree = AVLTree()

    for _ in range(n):
        avl_tree.insert(generate_random_car())


def benchmark_search(n):
    avl_tree = AVLTree()

    cars = [generate_random_car() for _ in range(n)]

    for car in cars:
        avl_tree.insert(car)

    for _ in range(n):
        avl_tree.search(random.choice(cars).price)


def benchmark_delete(n):
    avl_tree = AVLTree()

    cars = [generate_random_car() for _ in range(n)]

    for car in cars:
        avl_tree.insert(car)

    for car in cars:
        avl_tree.delete(car.price)


def benchmark_contains_by_vin(n):
    avl_tree = AVLTree()

    cars = [generate_random_car() for _ in range(n)]

    for car in cars:
        avl_tree.insert(car)

    for _ in range(n):
        avl_tree.contains_by_vin(random.choice(cars).vin)


def run_benchmarks():
    sizes = [100, 1000, 10000]

    for size in sizes:
        print(f"\nBenchmarks for size {size}:")
        print(f"Insert: {timeit.timeit(lambda: benchmark_insert(size), number=1):.6f} seconds")
        print(f"Search: {timeit.timeit(lambda: benchmark_search(size), number=1):.6f} seconds")
        print(f"Delete: {timeit.timeit(lambda: benchmark_delete(size), number=1):.6f} seconds")
        print(f"Contains by VIN: {timeit.timeit(lambda: benchmark_contains_by_vin(size), number=1):.6f} seconds")


if __name__ == "__main__":
    print("Running tests:")
    unittest.main()
    print("\nRunning benchmarks:")
    run_benchmarks()
