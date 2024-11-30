#####################Українська версія###########################

### Як зібрати гри у виконуваний файл:

1. Встановити бібліотеку: ```pip install pyinstaller```
2. Використовувати для шляхів у коді такий метод (далі код методу для визначення ффайлу в залежності від виду запуску з прикладом використання):

```python
import os
import sys


def resource_path(relative_path):
   """Отримати абсолютний шлях до ресурсу, враховуючи запакований .exe"""
   try:
      # Якщо програма запакована у виконуваний файл
      base_path = sys._MEIPASS
   except AttributeError:
      # Якщо запускається як скрипт
      base_path = os.path.abspath(".")

   return os.path.join(base_path, relative_path)


# Приклад використання
image_path = resource_path("assets/images/my_image.png")
```
3. Створити окрему папку, де буде лежати файли з кодом та папка з файлами, бажано, щоб зображення та інше знаходилося у папці ```assets```.
Приклад структури папки:
```
/my_game/
|-- main.py
|-- assets/
    |-- images/
    |-- sounds/
```
4. Запустити команду ```pyinstaller --onefile --windowed main.py```
5. Запустити команду ```pyinstaller --onefile --add-data "assets;assets" main.py```
6. Після усього створяться додаткові файли та папки у папці ```dist``` лежить .exe файл, який можна запустити, але у папку ```dist``` також треба скопіювати папку ```assets```. Після цього проект повинен запуститися.\
!!!Не впевнений на рахунок кроку 3, а саме переміщення папки ```assets``` у папку, де будемо збирати проект, можливо можна просто закинути у папку ```dist```, після збірки!!!

#####################English Version###########################

### How to package a game into an executable file:

1. **Install the required library:** 
   ```bash
   pip install pyinstaller
   ```

2. **Use the following method for handling paths in your code** (to define file paths based on the runtime environment). Below is the method for determining file paths and an example of its usage:
   ```python
   import os
   import sys

   def resource_path(relative_path):
       """Get the absolute path to a resource, accounting for the .exe."""
       try:
           # If the application is running as an executable
           base_path = sys._MEIPASS
       except AttributeError:
           # If running as a script
           base_path = os.path.abspath(".")

       return os.path.join(base_path, relative_path)

   # Example usage
   image_path = resource_path("assets/images/my_image.png")
   ```

3. **Prepare a separate folder** where you will place your code and all required resources. Ideally, images, sounds, and other assets should be located in an `assets` folder.  
   Example folder structure:
   ```
   /my_game/
   |-- main.py
   |-- assets/
       |-- images/
       |-- sounds/
   ```

4. **Run the following command to create an executable:**
   ```bash
   pyinstaller --onefile --windowed main.py
   ```

5. **Add resources to the executable by running this command:**
   ```bash
   pyinstaller --onefile --add-data "assets;assets" main.py
   ```

6. **Check the output folder.** After running the above commands, additional files and folders will be generated.  
   In the `dist` folder, you will find the `.exe` file. However, for the project to work, you may also need to copy the `assets` folder into the `dist` folder. Once that is done, your project should work correctly.  

   **Note:** Step 3 regarding moving the `assets` folder into the project build directory might not always be necessary. It might be sufficient to simply place the `assets` folder into the `dist` folder after building. Ensure to test this approach!  