file_path = 'rdf_prompt_template.txt'

try:
    # Открытие файла для чтения ('r' означает режим чтения)
    with open(file_path, 'r', encoding='utf-8') as file:
        # Чтение содержимого файла
        content = file.read()
        # Вывод содержимого файла на экран
        print(content)
except FileNotFoundError:
    # Этот блок кода выполнится, если файл не будет найден
    print(f"File not found: {file_path}")
except Exception as e:
    # Этот блок кода выполнится, если возникнет любая другая ошибка при работе с файлом
    print(f"An error occurred: {e}")