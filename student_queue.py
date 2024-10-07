from __future__ import annotations
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
import pickle


@dataclass
class Student:
    full_name: str
    group_number: str
    course: int
    age: int
    average_grade: float


class Node:
    def __init__(self, data: Student):
        self.data = data
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None


class QueueInterface(ABC):
    @abstractmethod
    def enqueue(self, item: Student) -> None:
        pass

    @abstractmethod
    def dequeue(self) -> Optional[Student]:
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def front(self) -> Optional[Student]:
        pass

    @abstractmethod
    def reverse(self) -> None:
        pass

    @abstractmethod
    def contains(self, item: Student) -> bool:
        pass

    @abstractmethod
    def contains_by_name(self, full_name: str) -> bool:
        pass

    @abstractmethod
    def save_to_file(self, filename: str) -> None:
        pass

    @abstractmethod
    def load_from_file(self, filename: str) -> None:
        pass


@dataclass
class StudentQueue(QueueInterface):
    head: Optional[Node] = None
    tail: Optional[Node] = None
    _size: int = 0

    def enqueue(self, item: Student) -> None:
        new_node = Node(item)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self) -> Optional[Student]:
        if self.is_empty():
            return None
        item = self.head.data
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self._size -= 1
        return item

    def is_empty(self) -> bool:
        return self.head is None

    def front(self) -> Optional[Student]:
        return self.head.data if self.head else None

    def reverse(self) -> None:
        if self.is_empty():
            return
        current = self.head
        self.head, self.tail = self.tail, self.head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev

    def contains(self, item: Student) -> bool:
        current = self.head
        while current:
            if current.data == item:
                return True
            current = current.next
        return False

    def contains_by_name(self, full_name: str) -> bool:
        current = self.head
        while current:
            if current.data.full_name == full_name:
                return True
            current = current.next
        return False

    def save_to_file(self, filename: str) -> None:
        data = []
        current = self.head
        while current:
            data.append(current.data)
            current = current.next
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    def load_from_file(self, filename: str) -> None:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        self.head = self.tail = None
        self._size = 0
        for item in data:
            self.enqueue(item)

    def __len__(self) -> int:
        return self._size


if __name__ == "__main__":
    queue = StudentQueue()

    students = [
        Student("Иван Иванов", "Группа1", 2, 20, 4.5),
        Student("Петр Петров", "Группа2", 3, 21, 4.2),
        Student("Анна Сидорова", "Группа1", 2, 19, 4.8),
        Student("Мария Козлова", "Группа3", 4, 22, 4.6),
        Student("Алексей Смирнов", "Группа2", 3, 20, 4.3),
        Student("Екатерина Новикова", "Группа1", 2, 19, 4.7),
        Student("Дмитрий Кузнецов", "Группа3", 4, 23, 4.1),
        Student("Ольга Морозова", "Группа2", 3, 21, 4.4),
        Student("Сергей Волков", "Группа1", 2, 20, 4.9),
        Student("Наталья Лебедева", "Группа3", 4, 22, 4.5)
    ]

    for student in students:
        queue.enqueue(student)

    print(f"Размер очереди: {len(queue)}")
    print(f"Первый студент: {queue.front()}")

    print(f"Содержит Анну Сидорову: {queue.contains(students[2])}")

    print(f"Содержит Дмитрия Кузнецова: {queue.contains_by_name('Дмитрий Кузнецов')}")

    queue.save_to_file("students_queue.pkl")

    while not queue.is_empty():
        queue.dequeue()

    print(f"Размер очереди после очистки: {len(queue)}")

    queue.load_from_file("students_queue.pkl")
    print(f"Размер очереди после загрузки: {len(queue)}")

    queue.reverse()
    print(f"Первый студент после реверса: {queue.front()}")
