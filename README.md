# Remainder

## How to run this
1. Run django server 
    `./manage.py runserver`
2. Run scheduler of celery
    `celery -A Remainder beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`
3. Run worker of celery
    `celery -A Remainder worker -l info -P eventlet`


## Use api to insert task
* URL : http://127.0.0.1:8000/api/v1
* DATA = 
>   {<br>
        "name":...(text max lenght 180),
        <br>
        "repeat":...(true,false),
        <br>
        "start_time":...(datetime (2022-02-3 09:08:00))
        <br>
        "every":...(Integer)
        <br>
        "period":...(string choice)
    <br>}

period choice => days,hours,minutes,seconds,microseconds
## Change token for change line api notify
`Change global TOKEN variable at line 7 in task/tasks.py`