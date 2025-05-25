#include <iostream>
#include <string>
#include <Windows.h>

int main() {
    // Устанавливаем кодировку для Windows консоли
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    std::string inputText;

    // Ввод текста
    std::cout << "Введите текст: ";
    std::getline(std::cin, inputText);  // Ввод текста с пробелами

    // Вывод текста
    std::cout << "Вы ввели: " << inputText << std::endl;

    return 0;
}
