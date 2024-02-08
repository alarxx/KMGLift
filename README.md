# KMGLift

### Задачи по ТКРС

**Определить тип операции:**
- Подъем
- Спуск
- Простой
- Другое

**Определить продолжительность операции:**
- Начало
- Конец
- Продолжительность

**Входящие данные:** Данные из датчика веса на крюке 
- время
- значение
- продолжительность

---
**Task Visualization:**

![Task_Visualization](https://github.com/Alar-q/KMGLift/blob/main/assets/1_TKRS_Tasks_Example.png)

---
**Data Visualization:**

![Data_Visualization1](https://github.com/Alar-q/KMGLift/blob/main/assets/2_TKRS_Tasks_Data1.png)

![Data_Visualization2](https://github.com/Alar-q/KMGLift/blob/main/assets/3_TKRS_Tasks_Data2.png)

---
**Filters don't work, even make it worse:**

![Filters](https://github.com/Alar-q/KMGLift/blob/main/assets/4_TKRS_Tasks_Filter1.png)

---
### Key Points

The task is easier to solve visually rather than by consistently observing each value. 

**Processing by convolutions:**

![Solution_1](https://github.com/Alar-q/KMGLift/blob/main/assets/5_TKRS_Tasks_Sol1_1.png)

![Solution_2](https://github.com/Alar-q/KMGLift/blob/main/assets/6_TKRS_Tasks_Sol1.png)

![Solution_3](https://github.com/Alar-q/KMGLift/blob/main/assets/7_TKRS_Tasks_Sol2.png)

**The exact slope:** 

![Solution_4](https://github.com/Alar-q/KMGLift/blob/main/assets/8_TKRS_Tasks_Sol3_1.png)

**Solution:**

![Solution_5](https://github.com/Alar-q/KMGLift/blob/main/assets/9_TKRS_Tasks_Sol3.png)

---
### Technical Description

old:
    Одно деление равно 3-м секундам: 3s=1, 6s=2... -> 
        Парсинг в часы = (value * 3) / 3600

prod_test:
    unsupported
    1) Определение отдельных процессов. "Visual" filter. Проблема basic в жестком программировании размера ядер
    2) Распознавание процессов. MSE. Проблема basic бывают выбросы на краях. 
    
prod:
    Ввод ->
    1) Определенение процессов (разбивка)
    2) Распознавание процессов
    -> Вывод

    Проблемы:
        1) Правильное выявление операций.(пока visual_filter основанный на morphological operations, далее MSE)
        2) Объединение операций. (пока последовательные одинаковые процессы)
