# Remainder
---
## How to run this
1. Run django server 
    `./manage.py runserver`
2. Run scheduler of celery
    `celery -A Remainder beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`
3. Run worker of celery
    `celery -A Remainder worker -l info -P eventlet`

----
## Use api to insert task
* URL : http://127.0.0.1:8000/api/v1
* DATA = 
>   {
        "name":...(text),
        "repeat":...(yes,no),
        "day":...(int 1-30),
        "month":...(int 1-12),
        "year":...(int length 4),
        "hour":...(int 0-23),
        "minute":...(int 0-59),
    }
----
## Change token for change line api notify
`Change global TOKEN variable at line 7 in task/tasks.py`