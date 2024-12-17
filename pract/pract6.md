![image](https://github.com/user-attachments/assets/7ffae966-e054-4668-88b0-c4633adb4d87)Работа с утилитой Make.
Изучить основы языка утилиты make. Распаковать в созданный каталог [make.zip](make.zip), если у вас в в системе нет make.
Создать приведенный ниже Makefile и проверить его работоспособность.

```
dress: trousers shoes jacket
    @echo "All done. Let's go outside!"

jacket: pullover
    @echo "Putting on jacket."

pullover: shirt
    @echo "Putting on pullover."

shirt:
    @echo "Putting on shirt."

trousers: underpants
    @echo "Putting on trousers."

underpants:
    @echo "Putting on underpants."

shoes: socks
    @echo "Putting on shoes."

socks: pullover
    @echo "Putting on socks."
```
Визуализировать файл [civgraph.txt](civgraph.txt).
![alt-text](https://sun9-9.userapi.com/impg/KrWq1kwEpVcFmUm_tVd0dP7MC3Mf3ABOi3ANjA/3DU6dmW_0gw.jpg?size=690x224&quality=96&sign=fb7455370b285aceb54125e9a8ff7de5&type=album)

## Задача 1

Написать программу на Питоне, которая транслирует граф зависимостей civgraph в makefile в духе примера выше. Для мало знакомых с Питоном используется упрощенный вариант civgraph: [civgraph.json](civgraph.json).

Пример:

```
> make mathematics
mining
bronze_working
sailing
astrology
celestial_navigation
pottery
writing
code_of_laws
foreign_trade
currency
irrigation
masonry
early_empire
mysticism
drama_poetry
mathematics
```
![alt-text](https://sun9-14.userapi.com/impg/6Nov9TnnHL9mMQmpsVC4Xty1TOYRG6VyViQGiA/ga4aLvEvOwE.jpg?size=747x681&quality=96&sign=f6e509aab04847ba7bc9a49e35fcf0d7&type=album)
## Задача 2

Реализовать вариант трансляции, при котором повторный запуск make не выводит для civgraph на экран уже выполненные "задачи".
![alt-text](https://sun9-51.userapi.com/impg/X5O5yKS2AoKkXV4MfzwQgFbp7nnGzaQw507YHA/VDvhbj9c0k8.jpg?size=977x1020&quality=96&sign=e6df8c6dd5c660ce057170ccd93eee81&type=album)

## Задача 3

Добавить цель clean, не забыв и про "животное".
![alt-text](https://sun9-39.userapi.com/impg/jpFkk24qbrd41GKtE51y2OvcW2u-kKBf8QGP9g/uDouqq7Pe9E.jpg?size=739x1024&quality=96&sign=86b9298a54acf39e299341a62c41b634&type=album)

## Задача 4

Написать makefile для следующего скрипта сборки:

```
gcc prog.c data.c -o prog
dir /B > files.lst
7z a distr.zip *.*
```

Вместо gcc можно использовать другой компилятор командной строки, но на вход ему должны подаваться два модуля: prog и data.
Если используете не Windows, то исправьте вызовы команд на их эквиваленты из вашей ОС.
В makefile должны быть, как минимум, следующие задачи: all, clean, archive.
Обязательно покажите на примере, что уже сделанные подзадачи у вас не перестраиваются.

![alt-text](https://sun9-61.userapi.com/impg/9r81YbN8OGq0zJTlWJiD_l25VNlg-H3lryTGDg/vFddBOFDFFg.jpg?size=721x547&quality=96&sign=38ad76879e47dacf9df1db1dc1ae1bf6&type=album)
