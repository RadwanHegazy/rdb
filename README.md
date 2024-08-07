# rdb

-  rdb is a No-Sql database u can use it for caching like redis.
-  rdb can save multible vale of your datatypes  

## Let's now how it is work !


```python

# import lib
from db.rdb import cache
from datetime import timedelta

# setting data 
cache.set(
    key = "dict",
    val = {
        "name" : "radwan",
        'age' : 19,
        'phone': 111111, 
    },
    exp = timedelta(hours=2).total_seconds()
)


cache.set(
    key = "int",
    val = 100,
    exp = timedelta(hours=2).total_seconds()
)


cache.set(
    key = "str",
    val = 'String Saved here !',
    exp = timedelta(hours=1).total_seconds()
)



class MyObject : 
    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

obj_instance = MyObject("Radwan", 19)
string = cache.set(
    key = "object",
    val = obj_instance,
    exp = timedelta(minutes=10).total_seconds()
)




# getting data

print(cache.get('dict')) # {'name': 'radwan', 'age': 19, 'phone': 111111}
print(cache.get('int')) # 100
print(cache.get('str')) # String Saved here !

cached_obj = cache.get('object')
print(cached_obj.name, cached_obj.age ) # Radwan 19

# delete data
cache.delete('dict')
cache.delete('int')
cache.delete('str')
cache.delete('object')

```


## Use rdb cache with django :

```python

#app/views.py
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AppSerilaizer, AppModel
from db.rdb import cache
from datetime import timedelta



@api_view(["GET"])
def index (request) :

    data = cache.get('data')
    if data is None:
        print("getting data from db")
        data = AppModel.objects.all()
        cache.set(
            'data',
            data,
            timedelta(hours=2).total_seconds()
        )
    else:
        print('getting data from cache')

    serializer = AppSerilaizer(data, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
```


# Note: This caching system made for educional purposes and for fun .