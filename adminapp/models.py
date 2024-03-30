from django.db import models

# Create your models here.

class menu:
    
    food_id:str
    food_name:str
    food_price:str

    quantity:str
    name:str 
    total_price:int

class Cart:
    food_id:str
    food_name:str
    food_price:str
    cust_id:str
    quantity:int
    total_price:int
class orders:
    order_id:str
    cust_id:str
    food_quantity:str
    total_price:str
class order_list:
    order_id:str
    cust_id:str
    total_price:str
    order_date:str
    order_status:str
    estimated_time:str
class Order:
    order_id:int
    total_amount:str
    order_date:str
    delivery_date:str
    status:str
class customer:
    cust_id:str
    name:str
    password:str