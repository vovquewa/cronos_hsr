import os


# Переменная пути проекта
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    print(PROJECT_PATH)
