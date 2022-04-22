## Задание:  
Реализовать REST API для системы комментариев блога.


**Функциональные требования:**  

У системы должны быть методы API, которые обеспечивают
* Добавление статьи (Можно чисто номинально, как сущность, к которой крепятся комментарии).
* Добавление комментария к статье.
* Добавление коментария в ответ на другой комментарий (возможна любая вложенность).
* Получение всех комментариев к статье вплоть до 3 уровня вложенности.
* Получение всех вложенных комментариев для комментария 3 уровня.
* По ответу API комментариев можно воссоздать древовидную структуру.  

**Нефункциональные требования:**  

* Использование Django ORM.
* Следование принципам REST.
* Число запросов к базе данных не должно напрямую зависеть от количества комментариев, уровня вложенности.
* Решение в виде репозитория на Github, Gitlab или Bitbucket.
* readme, в котором указано, как собирать и запускать проект. Зависимости указать в requirements.txt либо использовать poetry/pipenv.
* Использование свежих версий python и Django.  
 
**Будет плюсом:**  

* Использование PostgreSQL.
* docker-compose для запуска api и базы данных.
* Swagger либо иная документация к апи.
