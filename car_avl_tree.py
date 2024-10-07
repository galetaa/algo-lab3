from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional, List
import pickle


@dataclass
class Car:
    brand: str
    vin: str
    engine_volume: float
    price: float
    average_speed: float


class Node:
    def __init__(self, car: Car):
        self.car = car
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.height = 1


class AVLTreeInterface(ABC):
    @abstractmethod
    def insert(self, car: Car) -> None:
        pass

    @abstractmethod
    def delete(self, price: float) -> None:
        pass

    @abstractmethod
    def search(self, price: float) -> Optional[Car]:
        pass

    @abstractmethod
    def contains(self, car: Car) -> bool:
        pass

    @abstractmethod
    def contains_by_vin(self, vin: str) -> bool:
        pass

    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def load_from_file(self, filename: str) -> None:
        pass


class AVLTree(AVLTreeInterface):
    def __init__(self):
        self.root: Optional[Node] = None

    def height(self, node: Optional[Node]) -> int:
        if not node:
            return 0
        return node.height

    def balance_factor(self, node: Node) -> int:
        return self.height(node.left) - self.height(node.right)

    def update_height(self, node: Node) -> None:
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def right_rotate(self, y: Node) -> Node:
        x = y.left
        T2 = x.right if x else None

        if x:
            x.right = y
        y.left = T2

        self.update_height(y)
        if x:
            self.update_height(x)

        return x if x else y

    def left_rotate(self, x: Node) -> Node:
        y = x.right
        T2 = y.left if y else None

        if y:
            y.left = x

        x.right = T2

        self.update_height(x)
        if y:
            self.update_height(y)

        return y if y else x

    def insert(self, car: Car) -> None:
        self.root = self._insert(self.root, car)

    def _insert(self, node: Optional[Node], car: Car) -> Node:
        if not node:
            return Node(car)

        if car.price < node.car.price:
            node.left = self._insert(node.left, car)
        elif car.price > node.car.price:
            node.right = self._insert(node.right, car)
        else:
            node.car = car
            return node

        self.update_height(node)

        balance = self.balance_factor(node)

        if balance > 1 and car.price < node.left.car.price:
            return self.right_rotate(node)

        if balance < -1 and car.price > node.right.car.price:
            return self.left_rotate(node)

        if balance > 1 and car.price > node.left.car.price:
            node.left = self.left_rotate(node.left)
            return self.right_rotate(node)

        if balance < -1 and car.price < node.right.car.price:
            node.right = self.right_rotate(node.right)
            return self.left_rotate(node)

        return node

    def delete(self, price: float) -> None:
        self.root = self._delete(self.root, price)

    def _delete(self, root: Optional[Node], price: float) -> Optional[Node]:
        if not root:
            return root

        if price < root.car.price:
            root.left = self._delete(root.left, price)
        elif price > root.car.price:
            root.right = self._delete(root.right, price)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            temp = self._min_value_node(root.right)
            root.car = temp.car
            root.right = self._delete(root.right, temp.car.price)

        if root is None:
            return root

        self.update_height(root)

        balance = self.balance_factor(root)

        if balance > 1 and self.balance_factor(root.left) >= 0:
            return self.right_rotate(root)

        if balance > 1 and self.balance_factor(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and self.balance_factor(root.right) <= 0:
            return self.left_rotate(root)

        if balance < -1 and self.balance_factor(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def _min_value_node(self, node: Node) -> Node:
        current = node
        while current.left is not None:
            current = current.left
        return current

    def search(self, price: float) -> Optional[Car]:
        return self._search(self.root, price)

    def _search(self, root: Optional[Node], price: float) -> Optional[Car]:
        if root is None or root.car.price == price:
            return root.car if root else None

        if price < root.car.price:
            return self._search(root.left, price)
        return self._search(root.right, price)

    def contains(self, car: Car) -> bool:
        return self.search(car.price) is not None

    def contains_by_vin(self, vin: str) -> bool:
        return self._contains_by_vin(self.root, vin)

    def _contains_by_vin(self, node: Optional[Node], vin: str) -> bool:
        if node is None:
            return False
        if node.car.vin == vin:
            return True
        return self._contains_by_vin(node.left, vin) or self._contains_by_vin(node.right, vin)

    def save_to_file(self, filename: str) -> None:
        cars = self._inorder_traversal(self.root)
        with open(filename, 'wb') as file:
            pickle.dump(cars, file)

    def load_from_file(self, filename: str) -> None:
        with open(filename, 'rb') as file:
            cars = pickle.load(file)
        self.root = None
        for car in cars:
            self.insert(car)

    def _inorder_traversal(self, root: Optional[Node]) -> List[Car]:
        result = []
        if root:
            result.extend(self._inorder_traversal(root.left))
            result.append(root.car)
            result.extend(self._inorder_traversal(root.right))
        return result


if __name__ == "__main__":
    avl_tree = AVLTree()

    cars = [
        Car("Toyota", "JT2BF22K1W0123456", 2.0, 25000, 180),
        Car("Honda", "1HGCM82633A004852", 1.8, 22000, 175),
        Car("Ford", "1FAHP3EN2AW123456", 2.5, 28000, 190),
        Car("Chevrolet", "1G1BE5SM9H7123456", 1.5, 20000, 170),
        Car("BMW", "WBACG8103J3123456", 3.0, 45000, 220),
        Car("Mercedes", "WDDGF4HB5CR123456", 2.0, 40000, 200),
        Car("Audi", "WAUZZZ8K0AA123456", 2.0, 38000, 210),
        Car("Volkswagen", "WVWZZZ1KZAW123456", 1.4, 23000, 185),
        Car("Nissan", "JN1BJ0HP3JW123456", 1.6, 21000, 175),
        Car("Hyundai", "KMHDU4AD0AU123456", 1.6, 19000, 165)
    ]

    for car in cars:
        avl_tree.insert(car)

    print("Поиск автомобиля стоимостью 28000:")
    found_car = avl_tree.search(28000)
    print(found_car)

    print("\nПроверка наличия автомобиля Toyota:")
    print(avl_tree.contains(cars[0]))

    print("\nПроверка наличия автомобиля по VIN:")
    print(avl_tree.contains_by_vin("1FAHP3EN2AW123456"))

    print("\nСохранение в файл...")
    avl_tree.save_to_file("avl_tree_cars.pkl")

    print("\nОчистка дерева...")
    avl_tree = AVLTree()

    print("\nЗагрузка из файла...")
    avl_tree.load_from_file("avl_tree_cars.pkl")

    print("\nПроверка наличия автомобиля после загрузки:")
    print(avl_tree.contains(cars[0]))
