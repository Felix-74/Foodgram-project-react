#### Описание проекта:  
Сайт с рецептами различных блюд  
Можно создавать свои уникальные рецепты  
Добавлять в избранное/корзину  
Скачивать необходимые ингредиенты для готовки блюд по рецепту  
  
#### Автоматизированно при запуске docker:  
 - Выполнение миграций  
 - Приминение миграций  
 - Загрузка Тегов, Ингредиентов, Пользователей  
 - Создание тестовых рецептов  
#### Автоматическая загрузка выполняется manage командой  
#### Фильтрации сделаны с помощью django-filter  
#### Картинки у тестовых рецептов могут повторяться, так как берутся рандомно из 11 доступных изображений.  
  
#### Инструкция по запуску:
Клонировать репозиторий на свой сервер  
Изменить 4-ю строку в файле ```infra/nginx.conf``` на ip адрес своего сервера  
Выполнить ```docker-compose up -d```  
Сайт будет доступен по ip адресу вашего сервера.  

#### Данные для тестирования:  
##### Сайт: http://84.201.154.63  
|    Тип пользователя      |     Почта       |         Пароль         |
| :---:| :-----: | :---:|
|Администратор |```0@0.ru```|```0```|
|Пользователь  |```1@1.ru```  | ```usr_test_password```|
|Пользователь  |```2@2.ru```  | ```usr_test_password```|
|Пользователь  |```3@3.ru```  | ```usr_test_password```|

#### Пример обращения к API:
![Image alt](https://github.com/Felix-74/foodgram-project-react/blob/master/example_img/get_recipes_api.png)

#### Используемые технологии:
PostgeSQL, Docker, DRF, Python3, Nginx

#### Автор:
https://t.me/Igor_Seo74
