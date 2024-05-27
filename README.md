# Blogicum

**Описание проекта:**

Вымышленная социальная сеть, которая позволяет выкладывать свои публикации в формате блога. Для пользователей доступна возможность оставлять свои комментарии к публикациям.

**Цель проекта:**

Разработка полнофункциональной платформы для ведения блогов, где пользователи могут публиковать посты, добавлять комментарии, а также управлять своими профилями.</br>
Платформа включает в себя интеграцию таких функциональных модулей, как работа с пользователями, кастомные страницы для ошибок, пагинацию, загрузку изображений, создание новых публикаций и систему комментирования.</br>
В процессе разработки применены различные аспекты работы с веб-фреймворком Django.


| Адрес | Описание |
|-------------|-------------|
| 127.0.0.1   | Главная страница   |
| 127.0.0.1/admin/   | Панель администратора  |

### Используемые технологии:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![image](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)

## Установка:

Если Python не установлен, скачайте и установите его с [официального сайта](https://www.python.org/downloads/).

### Системные требования

- **Версия Python**: 3.9 или выше
- **Операционная система**: Windows / macOS / Linux

Клонировать репозиторий и перейти в него в командной строке:
```python
git clone git@github.com:Apollo297/django_sprint4.git
```
```python
cd django_sprint4
```
Cоздать и активировать виртуальное окружение:
```python
python3 -m venv env
```
```python
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```python
python3 -m pip install --upgrade pip
```
```python
pip install -r requirements.txt
```
Выполнить миграции:
```python
python3 manage.py migrate
```
Создать суперпользователя (если необходимо):
```python
python manage.py createsuperuser
```
Запустить проект:
```python
python3 manage.py runserver
```
Автор: Нечепуренко Алексей
