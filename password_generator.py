import random


class PasswordGenerator:

    def __init__(self):
        self.__letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                          't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                          'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.__numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.__symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '=', '^']

        self.__password_list = []
        self.__password = ""

    def get_password(self) -> str:
        num_letters = random.randint(8, 10)
        num_numbers = random.randint(2, 4)
        num_symbols = random.randint(2, 4)

        self.__password_list = []

        for _ in range(num_letters):
            self.__password_list.append(random.choice(self.__letters))
        for _ in range(num_numbers):
            self.__password_list.append(random.choice(self.__numbers))
        for _ in range(num_symbols):
            self.__password_list.append(random.choice(self.__symbols))

        random.shuffle(self.__password_list)
        self.__password = "".join(self.__password_list)

        return self.__password
