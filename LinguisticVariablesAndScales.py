import base64
from io import BytesIO

import numpy as np
import matplotlib.pyplot as plt


def triangle(x, params):
    a, b, c = params
    if a <= x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return (c - x) / (c - b)
    elif x < a or x > c:
        return 0


def trapezoidal_mf(x, params):
    a, b, c, d = params
    if x < a or x > d:
        return 0
    elif a <= x <= b and a != b:
        return (x - a) / (b - a)
    elif c <= x <= d and c != d:
        return (d - x) / (d - c)
    elif b < x < c or a == b or c == d:
        return 1


class LinguisticScale:
    def __init__(self, num_labels=3,
                 label_names=None,
                 membership_functions=None,
                 user_values=None):

        if label_names is None:
            label_names = ["Высокая", "Средняя", "Низкая"]
        if user_values is None:
            user_values = [10.0, 20.0, 30.0, 40.0, 60.0, 70.0, 80.0, 90.0]
        if membership_functions is None:
            membership_functions = [
                [70.0, 80.0, 100.0, 100.0],
                [30.0, 50.0, 75.0],
                [0.0, 20.0, 35.0]
            ]
        self.num_labels = num_labels
        self.user_values = user_values
        self.label_names = label_names
        self.membership_functions = membership_functions
        self.result_func_list = []

    def plot_membership_functions(self):
        max_x = 0
        plt.tight_layout()
        for i in self.membership_functions:
            for j in i:
                if j > max_x:
                    max_x = j
        for i, func in enumerate(self.membership_functions):
            if len(func) == 3:
                plt.plot([func[0], func[1], func[2], func[0]], [0, 1, 0, 0],label=self.label_names[i])
            elif len(func) == 4:
                plt.plot([func[0], func[1], func[2], func[3], func[0]], [0, 1, 1, 0, 0], label=self.label_names[i])

        i = 0
        result = self.findResultList()
        for val in self.user_values:
            plt.plot([val, val], [0, result[i]], 'g--')
            plt.plot([val, val], [0, 0], 'g--')
            plt.scatter(val, result[i], color='red')
            i += 1

        plt.ylim([0, 1.2])
        plt.xlim([0, 100])
        plt.xlabel('Введенные значения')
        plt.ylabel('Лингвистические переменные и шкалы')
        plt.legend()
        plt.grid(True)
        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plt.close()
        return base64.b64encode(img.read()).decode()

    def findResultList(self):
        result = []
        for i in self.user_values:
            max = 0
            index = 0
            for j in range(len(self.membership_functions)):
                if len(self.membership_functions[j]) == 3:
                    temp = triangle(i, self.membership_functions[j])
                    if max < temp:
                        max = temp
                        index = j
                if len(self.membership_functions[j]) == 4:
                    temp = trapezoidal_mf(i, self.membership_functions[j])
                    if max < temp:
                        max = temp
                        index = j
            result.append(max)
            self.result_func_list.append((i, self.label_names[index]))
        return result
