import email
import mysql.connector
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from datetime import datetime
from django.contrib import messages
import random

from django.http import JsonResponse


def generate_verification_code():
    return str(random.randint(100000, 999999))









def login(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        # Retrieve post details
        name = request.POST['name']
        pwd = request.POST['pwd']
        entered_code = request.POST['entered_code']
        generated_code = request.POST['generated_code']
        if entered_code == generated_code:
            # Code matches, proceed with login process
            sql = "SELECT * FROM customer_reg WHERE BINARY name = %s AND BINARY password = %s"
            params = (name, pwd)
            mycursor.execute(sql, params)
            result = mycursor.fetchone()
            if result:
                request.session['name'] = name
                return redirect('new_menu')
            else:
                message = "Invalid credentials! Please try again."
                return render(request, 'login.html', {'alert_message': message})
        else:
            # Code does not match
            message = "Verification code is incorrect."
            return render(request, 'login.html', {'alert_message': message})
    else:
        generated_code = generate_verification_code()
        return render(request, "login.html", {'generated_code': generated_code})
# Create your views here.












def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, "about.html")
def gallery(request):
    return render(request, "gallery.html")

def sucess(request):
    if 'name' in request.session:
        # Customer session is active, allow access to the success page
        return render(request, "sucess.html")
    else:
        # Customer session is not active, redirect to the login page
        return redirect('login')


def admin(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        # Retrieve post details
        name = request.POST['name']
        pwd = request.POST['pwd']
        query = "SELECT * FROM admin WHERE BINARY username = %s AND BINARY password = %s"
        values = (name, pwd)
        mycursor.execute(query, values)
        result = mycursor.fetchone()
        if result:
            request.session["username"] = name
            request.session['is_admin'] = True
            return redirect("day_revenue")
        else:
            message = "Invalid credentials! Please try again."
            return render(request, 'a_login.html', {'alert_message': message})
    else:
        return render(request, "a_login.html")
    


def registration(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        # retrive post details
        name = request.POST['name']
        pwd = request.POST['pwd']
        email = request.POST['email']
        phone_no = request.POST['phone_no']
        gender = request.POST['gender']
        query1 = "SELECT * FROM customer_reg WHERE name = '"+name+"'"
        mycursor=conn.cursor()
        mycursor.execute(query1)
        existing_user1 = mycursor.fetchone()
        query2 = "SELECT * FROM customer_reg WHERE email='"+email+"'"
        mycursor=conn.cursor()
        mycursor.execute(query2)
        existing_user2 = mycursor.fetchone()
        conn.close()
        query3= "SELECT * FROM customer_reg WHERE phone_no='"+phone_no+"'"
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor=conn.cursor()
        mycursor.execute(query3)
        existing_user3 = mycursor.fetchone()
        if existing_user1!=None:
            # Name already exists
            return render(request, "registration.html", {'status': 'User already exist with given name'})
        
        elif existing_user2!=None:
            # Name already exists
            return render(request, "registration.html", {'status': 'User already exist with given mail '})


        elif existing_user3!=None:
            # Name already exists
            return render(request, "registration.html", {'status': 'User already exist with given phone number '})

        else:
            mycursor.execute("insert into customer_reg(name,password,email,phone_no,gender) values('" +
                         name+"','"+pwd+"','"+email+"','"+phone_no+"','"+gender+"')")
            conn.commit()
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'manikanthmadishatti4@gmail.com'
            # For App Password, enable 2-step verification, then create an app password
            smtp_password = 'kely friw pbll qidr'
            # Email content
            subject = 'SDGS registration'
            body = 'You have successfully Registered' 
            sender_email = 'manikanthmadishatti4@gmail.com'
            receiver_email = email
            # Create a message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            # Connect to SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            message = "Successfull Registration"
            return redirect('login')
    else:
        return render(request, "registration.html")
def dashboard(request):
    if ('name' in request.session):
        name = request.session['name']
        return render(request, "dashboard.html")
    else:
        return render(request, "login.html", {'name': name})
def a_dashboard(request):
    return render(request, "a_dashboard.html")
def extra_menu(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usdk"
    )
    mycursor = conn.cursor()
    # retrive post details
    mycursor.execute("select * from menu")
    result = mycursor.fetchall()
    photos = []
    for x in result:
        p = menu()
        p.name = x[4]
        p.food_id = x[0]
        p.food_name = x[1]
        p.food_price = x[2]
        photos.append(p)
    return render(request, 'extra_menu.html', {"menu": photos})
def Starters(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usdk"
    )
    mycursor = conn.cursor()
    mycursor.execute("select * from menu where food_category='Starters'")
    result = mycursor.fetchall()
    m = []
    for row in result:
        obj = menu()
        obj.name = row[4]
        obj.food_name = row[1]
        obj.price = row[2]
        m.append(obj)
    return render(request, 'Starters.html', {'menu': m})
def Deserts(request):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usdk"
    )
    mycursor = conn.cursor()
    mycursor.execute("select * from menu where food_category='Deserts'")
    result = mycursor.fetchall()
    m = []
    for row in result:
        obj = menu()
        obj.food_id = row[0]
        obj.food_category = row[1]
        obj.food_item_name = row[2]
        obj.food_quantity = row[3]
        obj.price = row[4]
        m.append(obj)
    return render(request, 'Deserts.html', {'menu': m})
def dashboard(request):
    if ('name' in request.session):
        name = request.session['name']
        return render(request, "dashboard.html")
    else:
        return render(request, "login.html", {'name': name})
    


def view_menu(request):
    if request.session.get("username") and request.session.get("is_admin"):
        # If the admin session is active, proceed with the view logic
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        # Retrieve post details
        mycursor.execute("select * from menu")
        result = mycursor.fetchall()
        photos = []
        for x in result:
            p = menu()
            p.food_id = x[0]
            p.food_name = x[1]
            p.food_price = x[2]
            p.expire = x[3]
            p.quantity = x[4]
            photos.append(p)
        
        # Check if a food_id was posted and delete the corresponding feedback
        food_id = request.POST.get('food_id')
        if food_id:
            mycursor.execute(
                "DELETE FROM feedback WHERE feedback_id = %s", (food_id,))
            conn.commit()
            mycursor.execute(
                "SELECT * FROM feedback order by (feedback_id) DESC")
            photos = mycursor.fetchall()
        
        return render(request, 'view_menu.html', {"menu": photos})
    else:
        # Redirect to the admin login page or handle the case where the session is not active
        return redirect('admin')

def simple_upload(request):
    if request.session.get("username") and request.session.get("is_admin"):
        if request.method == 'POST' and request.FILES.get('myfile'):
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            newcur = con.cursor()
            food_id = request.POST['food_id']
            food_name = request.POST['food_name']
            food_price = request.POST['food_price']
            expire = request.POST['expire']
            quantity = request.POST['quantity']
            
            newcur.execute("INSERT INTO menu(food_id, food_name, food_price, expire, quantity, name) VALUES (%s, %s, %s, %s, %s, %s)",
                           (food_id, food_name, food_price, expire, quantity, filename))
            
            con.commit()
            return redirect('simple_upload')
        else:
            return render(request, 'simple_upload.html')
    else:
        # Redirect to the admin login page or handle the case where the session is not active
        return redirect('admin')




def new_menu(request):
    if 'name' in request.session:
        # Check if the 'name' key is present in the session, indicating an active customer session
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        # Retrieve post details
        mycursor.execute("select * from menu")
        result = mycursor.fetchall()
        photos = []
        for x in result:
            p = menu()
            p.name = x[5]
            p.food_id = x[0]
            p.food_name = x[1]
            p.food_price = x[2]
            p.expire = x[3]
            photos.append(p)
        return render(request, 'new_menu.html', {"menu": photos})
    else:
        # Redirect to the customer login page or handle the case where the session is not active
        return redirect('login')



def myaccount(request):
    if 'name' in request.session:
        # Customer session is active
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        name = request.session['name']
        mycursor.execute(
            "SELECT cust_id, name, email, phone_no, gender FROM customer_reg WHERE name=%s", (name,))
        result = mycursor.fetchone()
        if result:
            cust_id, name, email, phone, gender = result
            customer = {
                'cust_id': cust_id,
                'name': name,
                'email': email,
                'phone': phone,
                'gender': gender
            }
        else:
            customer = None
        conn.close()
        return render(request, 'myaccount.html', {'customer': customer})
    else:
        # Customer session is not active, redirect to the login page
        return redirect('login')







def edit_menu(request):
    if request.session.get("username") and request.session.get("is_admin"):
        # If the admin session is active, proceed with the view logic
        if request.method == 'POST' and request.FILES.get('myfile'):
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            mycursor = conn.cursor()
            food_id = request.POST['food_id']
            food_name = request.POST['food_name']
            price = request.POST['food_price']
            quantity = request.POST['quantity']
            mycursor.execute("UPDATE menu SET food_id ='"+food_id+"' , food_name = '"+food_name +
                             "', food_price='"+price+"',quantity='"+quantity+"' WHERE food_id = '"+food_id+"'")
            conn.commit()
            return render(request, 'new_menu.html')
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            mycursor = conn.cursor()
            food_id = request.GET.get('food_id')  # Get food_id from the query string
            mycursor.execute("SELECT * FROM menu WHERE food_id = %s", (food_id,))
            row = mycursor.fetchall()
            food = []
            for row in row:
                f = menu()
                f.food_id = row[0]
                f.food_name = row[1]
                f.food_price = row[2]
                f.food_category = row[3]
                f.name = row[4]
                food.append(f)
            return render(request, 'edit_sub_menu.html', {"fo": food})
    else:
        # Redirect to the admin login page or handle the case where the session is not active
        return redirect('admin')


def logout(request):
    if "name" in request.session:
        del request.session['name']
    if "cartlist" in request.session:
        del request.session['cartlist']
    request.session.modified = True
    return render(request, 'index.html')



def a_logout(request):
    if 'username' in request.session:
        del request.session['username']
    if 'is_admin' in request.session:
        del request.session['is_admin']
    request.session.modified = True
    return render(request, 'index.html')




import time


def add_cart(request, food_id):
    time.sleep(1)
    if "name" in request.session:
        # Check if the 'name' key is present in the session, indicating an active customer session
        name = request.session['name']
        if 'cartlist' not in request.session:
            cartlist = []
        else:
            cartlist = request.session['cartlist']
        if food_id not in cartlist:
            cartlist.append(food_id)
            request.session['cartlist'] = cartlist
        return redirect('new_menu')
    else:
        # Redirect to the customer login page or handle the case where the session is not active
        return render(request, 'login.html')


def remove_cart(request, food_id):
    if 'cartlist' in request.session:
        cartlist = request.session['cartlist']
        if str(food_id) in cartlist:
            cartlist.remove(str(food_id))
            request.session['cartlist'] = cartlist
    return redirect('view_cart')

def forgot_password(request):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        # retrieve post details
        email = request.POST['email']
        mycursor.execute(
            "SELECT password FROM customer_reg WHERE email='" + email + "'")
        result = mycursor.fetchone()
        pwd = str(result)
        if result is not None:
            # SMTP server configuration
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'manikanthmadishatti4@gmail.com'
            # For App Password, enable 2-step verification, then create an app password
            smtp_password = 'kely friw pbll qidr'
            # Email content
            subject = 'Password recovery'
            body = 'This is a Password recovery email sent from USDK. ' \
                   'Your password as per registration is: ' + pwd[2:len(pwd) - 3]
            sender_email = 'manikanthmadishatti4@gmail.com'
            receiver_email = email
            # Create a message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            # Connect to SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            message = "Password sent to the given email ID"
            return render(request, 'forgot_password.html', {'alert_message': message})
        else:
            message = "Please enter the correct email ID"
            return render(request, 'forgot_password.html', {'alert_message': message})
    else:
        return render(request, 'forgot_password.html')



def banking_register(request):
    if 'name' in request.session:
        # Customer session is active
        if request.method == 'POST':
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            mycursor = conn.cursor()
            # Retrieve name from session
            name = request.session.get('name')
            # Retrieve customer ID from customer_reg table
            mycursor.execute(
                "SELECT cust_id FROM customer_reg WHERE name = %s", (name,))
            cust_id = mycursor.fetchone()[0]
            # Retrieve post details
            cvv = request.POST['cvv']
            account_number = request.POST['account_number']
            # Check if name already exists in banking_details table
            query = "SELECT COUNT(*) FROM banking_details WHERE name = %s"
            values = (name,)
            mycursor.execute(query, values)
            result = mycursor.fetchone()[0]
            if result > 0:
                message = "You have already registered your banking details."
                return render(request, "banking_register.html", {'alert_message': message})
            # Use a parameterized query to avoid SQL injection
            query = "INSERT INTO banking_details(cust_id, name, cvv, account_number) VALUES (%s, %s, %s, %s)"
            values = (cust_id, name, cvv, account_number)
            mycursor.execute(query, values)
            conn.commit()
            conn.close()
            return render(request, "checkout.html")
        else:
            return render(request, "banking_register.html")
    else:
        # Customer session is not active, redirect to the login page
        return redirect('login')





def check1(request):
    if "name" in request.session:
        # print('user is in session')
        name = request.session['name']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        p = []
        if 'cartlist' in request.session:
            # print('in cart')
            p = list(request.session['cartlist'])
        # print(p)
        if p:
            # print('in cart add to db ')
            mycursor.execute(
                "SELECT cust_id FROM customer_reg WHERE name='" + name + "'")
            cust_id = mycursor.fetchone()[0]
            d = []
            total_price = 0
            grand_total = 0
            finalsub = str(request.POST['finalsub'])
        # print(finalsub)
            finalsubparts = finalsub.split('@')
            pids = finalsubparts[0]
            total = finalsubparts[1]
            stotal = str(total)
            # print(pids,":",total)
            qssplit = total.split(',')
            u = 0
            today = datetime.now()
            # print(today)
            b = str(today)
            # print(b)
            mycursor.execute(
                "INSERT INTO order_list (cust_id, total_price,order_date) VALUES (%s,%s, %s)", (cust_id, total, b))
            mycursor.execute(
                "SELECT order_id from order_list order by order_id desc limit 1")
            resultorder = mycursor.fetchone()
            order_id = resultorder[0]
            # print(order_id)
            pids = pids.split(',')
            # print(pids,)
            for aa in pids:
                # print(aa)
                mycursor.execute(
                    "SELECT * FROM menu WHERE food_id='" + str(aa) + "'")
                result = mycursor.fetchone()
                if result != None:
                    obj = menu()
                    obj.food_id = result[0]
                    obj.food_name = result[1]
                    obj.food_price = result[2]
                    obj.cust_id = cust_id
                    obj.order_id = order_id
                    obj.quantity = int(qssplit[u])
                    u += 1
                    obj.total_price = obj.food_price * obj.quantity
                    # shipping_charge = 10
                    grand_total = grand_total+obj.total_price
                    # grand_total += obj.grand_total
                    # print(grand_total)
                    d.append(obj)
                    # Insert the cart item with quantity
                    mycursor.execute("insert into order_details (cust_id,order_id, food_id,food_name, quantity, total_price) VALUES (%s, %s, %s, %s,%s, %s)", (
                        cust_id, order_id, obj.food_id, obj.food_name, obj.quantity, obj.total_price))
            # print(grand_total)
            mycursor.execute("UPDATE order_list SET total_price=" +
                             str(grand_total)+" WHERE order_id="+str(order_id))
            conn.commit()
            del request.session['cartlist']
            return render(request, 'checkout.html', {'pro': [], 'total_price': obj.total_price})
        else:
            return render(request, 'view_cart.html', {'pro': [], 'total_price': 0, 'grand_total': 0})
    else:
        return render(request, 'login.html')
    

    
    
def view_orders(request):
    if request.session.get("username") and request.session.get("is_admin"):
        # If the admin session is active, proceed with the view logic
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        mycursor.execute(
            "SELECT order_id, cust_id, order_date, total_price, order_status, estimated_time FROM order_list WHERE payment_status=1 ORDER BY order_id DESC")
        order_list_result = mycursor.fetchall()
        orders_dict = {}
        # Iterate over the results from the order_list table
        for order in order_list_result:
            order_id = order[0]
            cust_id = order[1]
            order_date = order[2]
            total_price = order[3]
            order_status = order[4]
            estimated_time = order[5]
            # Select the desired columns from the order_details table for the current order_id
            mycursor.execute(
                "SELECT food_name, quantity FROM order_details WHERE order_id=%s", (order_id,))
            order_details_result = mycursor.fetchall()
            # Create a list to store the food items for the current order
            food_items = []
            # Iterate over the results from the order_details table for the current order_id
            for order_detail in order_details_result:
                food_name = order_detail[0]
                quantity = order_detail[1]
                # Create a dictionary to store the current food item
                food_item_dict = {
                    'food_name': food_name,
                    'quantity': quantity
                }
                # Append the current food item to the list of food items for the current order
                food_items.append(food_item_dict)
            # Create a dictionary to store the current order
            order_dict = {
                'order_id': order_id,
                'cust_id': cust_id,
                'order_date': order_date,
                'total_price': total_price,
                'food_items': food_items,
                'order_status': order_status,
                'estimated_time': estimated_time
            }
            # Add the current order to the orders dictionary
            orders_dict[order_id] = order_dict
        # Close the database connection
        conn.close()
        # Pass the orders dictionary to the view_orders.html template
        return render(request, 'view_orders.html', {'orders_dict': orders_dict})
    else:
        # Redirect to the admin login page or handle the case where the session is not active
        return redirect('admin')
    


def sendfeedback(request):
    if 'name' in request.session:
        # Customer session is active
        name = request.session['name']
        # Retrieve cust_id from session
        cust_id = request.session.get('cust_id')
        if request.method == 'POST':
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            newcur = conn.cursor()
            newcur.execute(
                "SELECT cust_id FROM customer_reg WHERE name='" + name + "'")
            cust_id = newcur.fetchone()[0]
            food_id = request.POST['fid']
            newcur.execute(
                "SELECT food_name FROM menu WHERE food_id='" + food_id + "'")
            food_name = newcur.fetchone()[0]
            rating = request.POST['rating']
            comment = request.POST['comment']
            newcur.execute("INSERT INTO feedback(cust_id,food_id, food_name,rating,comment) VALUES (%s,%s, %s,%s, %s)",
                           (cust_id, food_id, food_name, rating, comment))
            conn.commit()
            messages.success(request, 'Feedback sent successfully!')
            conn.close()
            return redirect('sendfeedback')
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM menu")
            result = mycursor.fetchall()
            fb = []
            for x in result:
                p = menu()
                p.food_id = x[0]
                p.food_name = x[1]
                fb.append(p)
            conn.close()
            return render(request, 'sendfeedback.html', {'fb': fb})
    else:
        # Customer session is not active, redirect to the login page
        return redirect('login')



    

def view_feedback(request):
    if request.session.get("username") and request.session.get("is_admin"):
        # If the admin session is active, proceed with the view logic
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        newcur = conn.cursor()
        if request.method == 'POST':
            feedback_id = request.POST.get('feedback_id')
            if feedback_id:
                newcur.execute(
                    "DELETE FROM feedback WHERE feedback_id = %s", (feedback_id,))
                conn.commit()
        newcur.execute("SELECT * FROM feedback order by (feedback_id) DESC")
        feedbacks = newcur.fetchall()
        # Close the database connection
        conn.close()
        return render(request, 'view_feedback.html', {'feedbacks': feedbacks})
    else:
        # Redirect to the admin login page or handle the case where the session is not active
        return redirect('admin')


def edit_sub_menu(request, food_id):
    if request.session.get("username") and request.session.get("is_admin"):
        # If the admin session is active, proceed with the view logic
        if request.method == 'POST' and request.FILES.get('myfile'):
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            mycursor = conn.cursor()
            food_id = request.POST['food_id']
            food_name = request.POST['food_name']
            price = request.POST['food_price']
            mycursor.execute("UPDATE menu SET food_id ='"+food_id+"' , food_name = '"+food_name +
                             "', food_price='"+price+"', name='"+filename+"' WHERE food_id = '"+food_id+"'")
            conn.commit()
            return redirect('view_menu')  # Redirect to the view_menu page
        else:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            mycursor = conn.cursor()
            mycursor.execute("SELECT * FROM menu WHERE food_id = %s", (food_id,))
            row = mycursor.fetchall()
            food = []
            for row in row:
                f = menu()
                f.food_id = row[0]
                f.food_name = row[1]
                f.food_price = row[2]
                f.name = row[4]
                food.append(f)
            return render(request, 'edit_sub_menu.html', {"fo": food})
    else:
        # Redirect to the admin login page or handle the case where the session is not active
        return redirect('admin')


def del_sub_menu(request, food_id):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="usdk"
    )
    mycursor = conn.cursor()
    mycursor.execute("delete from menu where food_id='"+food_id+"'")
    conn.commit()
    return redirect(view_menu)



def update_order(request, order_id):
    if request.method == 'POST':
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        order_id = request.POST['order_id']
        order_status = request.POST['order_status']
        estimated_time = request.POST['estimated_time']
         

        mycursor.execute("SELECT cust_id FROM order_list WHERE order_id=%s", (order_id,))
        result1 = mycursor.fetchone()
        cust_id = result1[0]
    
        mycursor.execute("SELECT email FROM customer_reg WHERE cust_id=%s", (cust_id,))
        result2 = mycursor.fetchone()
        email = result2[0]



        mycursor.execute("UPDATE order_list SET order_id='"+order_id+"' ,order_status='" +
                     order_status+"', estimated_time='"+estimated_time+"' WHERE order_id = '"+order_id+"'")
        conn.commit()


        if order_status=='packed':
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'manikanthmadishatti4@gmail.com'
            # For App Password, enable 2-step verification, then create an app password
            smtp_password = 'kely friw pbll qidr'
            # Email content
            subject = 'SDGS order'
            body = 'Your order have been packed' 
            sender_email = 'manikanthmadishatti4@gmail.com'
            receiver_email = email
            # Create a message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            # Connect to SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            message = "Order packed"



        if order_status=='delivered':
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'manikanthmadishatti4@gmail.com'
            # For App Password, enable 2-step verification, then create an app password
            smtp_password = 'kely friw pbll qidr'
            # Email content
            subject = 'SDGS order delivery'
            body = 'Your order have been successfully delivered' 
            sender_email = 'manikanthmadishatti4@gmail.com'
            receiver_email = email
            # Create a message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))
            # Connect to SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            message = "Order delivered"


        return redirect(view_orders)
    


    else:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
    mycursor = conn.cursor()
    mycursor.execute(
        "SELECT * FROM order_list WHERE order_id = '"+order_id+"'")
    row = mycursor.fetchall()
    food = []
    for row in row:
        f = order_list()
        f.order_id = row[0]
        f.order_status = row[5]
        f.estimated_time = row[6]
        food.append(f)
    return render(request, 'update_order.html', {"fo": food})






from django.shortcuts import render, redirect

def order_status(request):
    if 'name' in request.session:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        # Retrieve the cust_id for the current user
        name = request.session['name']
        mycursor.execute(
            "SELECT cust_id FROM customer_reg WHERE name=%s", (name,))
        result = mycursor.fetchone()
        cust_id = result[0]
        # Retrieve the orders for the current customer that have been paid for and are scheduled for today
        mycursor.execute(
            """
            SELECT
                ol.order_id,
                ol.order_date,
                ol.total_price,
                ol.order_status,
                ol.estimated_time,
                GROUP_CONCAT(od.food_name SEPARATOR ', ') AS food_items
            FROM
                order_list ol
                JOIN order_details od ON ol.order_id = od.order_id
            WHERE
                ol.cust_id = %s
                AND ol.payment_status = 1
            GROUP BY
                ol.order_id
            ORDER BY
                ol.order_id DESC
            """,
            (cust_id,)
        )
        order_list_result = mycursor.fetchall()
        orders_dict = {}
        for order in order_list_result:
            order_id = order[0]
            order_date = order[1]
            total_price = order[2]
            order_status = order[3]
            estimated_time = order[4]
            food_items_str = order[5]
            # Convert the string of food items to a list of dictionaries
            food_items = []
            for item in food_items_str.split(', '):
                mycursor.execute(
                    "SELECT quantity FROM order_details WHERE order_id=%s AND food_name=%s ", (order_id, item))
                quantity = mycursor.fetchone()[0]
                food_item_dict = {
                    'food_name': item,
                    'quantity': quantity
                }
                food_items.append(food_item_dict)
            order_dict = {
                'order_id': order_id,
                'order_date': order_date,
                'total_price': total_price,
                'food_items': food_items,
                'order_status': order_status,
                'estimated_time': estimated_time
            }
            orders_dict[order_id] = order_dict
        conn.close()
        return render(request, 'order_status.html', {'orders_dict': orders_dict})
    else:
        return redirect('login')




def day_revenue(request):
    if request.session.get("username") and request.session.get("is_admin"):
        # If the admin session is active, proceed with the view logic
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()        
        if request.method == 'POST':
            date = request.POST.get('date')
            # Select orders with the specified date and payment status = 1
            mycursor.execute(
                "SELECT order_id, cust_id, order_date, total_price FROM order_list WHERE order_date = %s AND payment_status = 1", (date,))
            order_list_result = mycursor.fetchall()
            # Calculate the total revenue for the specified date
            mycursor.execute(
                "SELECT SUM(total_price) FROM order_list WHERE order_date = %s AND payment_status = 1", (date,))
            total_revenue = mycursor.fetchone()[0]
            orders_dict = {}
            # Iterate over the results from the order_list table
            for order in order_list_result:
                order_id = order[0]
                cust_id = order[1]
                order_date = order[2]
                total_price = order[3]
                # Select the desired columns from the order_details table for the current order_id
                mycursor.execute(
                    "SELECT food_name, quantity FROM order_details WHERE order_id=%s", (order_id,))
                order_details_result = mycursor.fetchall()
                # Create a list to store the food items for the current order
                food_items = []
                # Iterate over the results from the order_details table for the current order_id
                for order_detail in order_details_result:
                    food_name = order_detail[0]
                    quantity = order_detail[1]
                    # Create a dictionary to store the current food item
                    food_item_dict = {
                        'food_name': food_name,
                        'quantity': quantity
                    }
                    # Append the current food item to the list of food items for the current order
                    food_items.append(food_item_dict)
                # Create a dictionary to store the current order
                order_dict = {
                    'order_id': order_id,
                    'cust_id': cust_id,
                    'order_date': order_date,
                    'total_price': total_price,
                    'food_items': food_items,
                }
                # Add the current order to the orders dictionary
                orders_dict[order_id] = order_dict
            # Close the database connection
            conn.close()
            # Pass the orders dictionary and the total revenue to the day_revenue.html template
            return render(request, 'day_revenue.html', {'orders_dict': orders_dict, 'total_revenue': total_revenue})
        else:
            mycursor.execute(
                "SELECT order_id, cust_id, order_date, total_price FROM order_list")
        order_list_result = mycursor.fetchall()
        # Calculate the total revenue for the specified date
        mycursor.execute(
            "SELECT SUM(total_price) FROM order_list ")
        total_revenue = mycursor.fetchone()[0]
        orders_dict = {}
        # Iterate over the results from the order_list table
        for order in order_list_result:
            order_id = order[0]
            cust_id = order[1]
            order_date = order[2]
            total_price = order[3]
            # Select the desired columns from the order_details table for the current order_id
            mycursor.execute(
                "SELECT food_name, quantity FROM order_details WHERE order_id=%s", (order_id,))
            order_details_result = mycursor.fetchall()
            # Create a list to store the food items for the current order
            food_items = []
            # Iterate over the results from the order_details table for the current order_id
            for order_detail in order_details_result:
                food_name = order_detail[0]
                quantity = order_detail[1]
                # Create a dictionary to store the current food item
                food_item_dict = {
                    'food_name': food_name,
                    'quantity': quantity
                }
                # Append the current food item to the list of food items for the current order
                food_items.append(food_item_dict)
            # Create a dictionary to store the current order
            order_dict = {
                'order_id': order_id,
                'cust_id': cust_id,
                'order_date': order_date,
                'total_price': total_price,
                'food_items': food_items,
            }
            # Add the current order to the orders dictionary
            orders_dict[order_id] = order_dict
        # Close the database connection
        conn.close()
        # Pass the orders dictionary and the total revenue to the day_revenue.html template
        return render(request, 'day_revenue.html', {'orders_dict': orders_dict, 'total_revenue': total_revenue})
    else:
        # Redirect to the admin login page or handle the case where the session is not active
        return redirect('admin')    



def view_cart(request):
    if 'name' in request.session:
        # Customer session is active
        name = request.session['name']
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database="usdk"
        )
        mycursor = conn.cursor()
        # Get customer ID based on customer name
        mycursor.execute(
            "SELECT cust_id FROM customer_reg WHERE name='" + name + "'")
        cust_id = mycursor.fetchone()[0]
        p = []
        if 'cartlist' in request.session:
            p = list(request.session['cartlist'])
        d = []
        for aa in p:
            mycursor.execute(
                "SELECT * FROM menu WHERE food_id='" + str(aa) + "'")
            result = mycursor.fetchall()
            for row in result:
                obj = menu()
                obj.food_id = row[0]
                obj.food_name = row[1]
                obj.food_price = row[2]
                obj.name = row[5]
                obj.cust_id = cust_id
                d.append(obj)
        conn.close()
        return render(request, 'view_cart.html', {'menu': d})
    else:
        # Customer session is not active, redirect to the login page
        return redirect('login')





def checkout(request):
    if 'name' in request.session:
        # Customer session is active
        name = request.session['name']
        if request.method == 'POST':
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            mycursor = conn.cursor()
            name1 = request.POST.get('name')
            cvv = request.POST.get('cvv')
            account_number = request.POST.get('account_number')
            query = "SELECT * FROM banking_details WHERE name=%s AND cvv=%s AND account_number=%s"
            values = (name1, cvv, account_number)
            mycursor.execute(query, values)
            result = mycursor.fetchall()
            if not result:
                # Check if banking details exist for the user
                query = "SELECT * FROM banking_details WHERE name=%s"
                values = (name1,)
                mycursor.execute(query, values)
                result = mycursor.fetchall()
                if not result:
                    alert_message = "Please register your banking details first!"
                else:
                    alert_message = "Cannot Process as details are invalid."
                conn.close()
                return render(request, "checkout.html", {'status': 'error', 'alert_message': alert_message})
            mycursor.execute(
                "SELECT order_id FROM order_list ORDER BY order_id DESC LIMIT 1")
            result = mycursor.fetchone()
            if result:
                order_id = result[0]
                print(order_id)
            else:
                # handle case where there are no rows in order_list table
                order_id = None
            if order_id is not None:
                payment_status = 1
                mycursor.execute(
                    "UPDATE order_list SET payment_status=%s WHERE order_id=%s", (payment_status, order_id))
                conn.commit()
                mycursor.execute("SELECT email FROM customer_reg WHERE name=%s", (name,))
                result1 = mycursor.fetchone()
                email = result1[0]
                smtp_server = 'smtp.gmail.com'
                smtp_username = 'manikanthmadishatti4@gmail.com'
                smtp_port = 587
                # For App Password, enable 2-step verification, then create an app password
                smtp_password = 'kely friw pbll qidr'
                # Email content
                subject = 'SDGS Order Successfull'
                body = 'Your order has been placed successfully'
                sender_email = 'manikanthmadishatti4@gmail.com'
                receiver_email = email
                # Create a message
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = receiver_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                # Connect to SMTP server and send the email
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_username, smtp_password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                message = "Successfull  Order"
                alert_message = "Your order has been placed successfully"
                conn.close()
                return render(request, "sucess.html", {'status': 'success', 'alert_message': alert_message})
            else:
                alert_message = "No orders found in order list table."
                conn.close()
                return render(request, "checkout.html", {'status': 'error', 'alert_message': alert_message})
        else:
            conn.close()
            return render(request, "checkout.html")
    else:
        # Customer session is not active, redirect to the login page
        return redirect('login')





def check(request):
    if 'name' in request.session:
        # Customer session is active
        name = request.session['name']
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        mycursor = conn.cursor()
        p = []
        if 'cartlist' in request.session:
            p = list(request.session['cartlist'])
        if p:
            mycursor.execute(
                "SELECT cust_id FROM customer_reg WHERE name='" + name + "'")
            cust_id = mycursor.fetchone()[0]
            d = []
            total_price = 0
            grand_total = 0
            finalsub = str(request.POST['finalsub'])
            finalsubparts = finalsub.split('@')
            pids = finalsubparts[0]
            total = finalsubparts[1]
            stotal = str(total)
            qssplit = total.split(',')
            u = 0
            today = datetime.now()
            b = str(today)
            mycursor.execute(
                "INSERT INTO order_list (cust_id, total_price, order_date) VALUES (%s, %s, %s)", (cust_id, total, b))
            mycursor.execute(
                "SELECT order_id FROM order_list ORDER BY order_id DESC LIMIT 1")
            resultorder = mycursor.fetchone()
            order_id = resultorder[0]
            pids = pids.split(',')
            for aa in pids:
                mycursor.execute(
                    "SELECT * FROM menu WHERE food_id='" + str(aa) + "'")
                result = mycursor.fetchone()
                if result:
                    obj = menu()
                    obj.food_id = result[0]
                    obj.food_name = result[1]
                    obj.food_price = result[2]
                    obj.cust_id = cust_id
                    obj.order_id = order_id
                    obj.quantity = float(qssplit[u])
                    u += 1
                    obj.total_price = obj.food_price * obj.quantity
                    grand_total = grand_total + obj.total_price
                    d.append(obj)
                    mycursor.execute("INSERT INTO order_details (cust_id, order_id, food_id, food_name, quantity, total_price) VALUES (%s, %s, %s, %s, %s, %s)", (
                        cust_id, order_id, obj.food_id, obj.food_name, obj.quantity, obj.total_price))
            mycursor.execute("UPDATE order_list SET total_price=" +
                             str(grand_total) + " WHERE order_id=" + str(order_id))
            conn.commit()
            del request.session['cartlist']
            # Add 'total_price' to context dictionary
            context = {'total_price': grand_total}
            conn.close()
            return render(request, 'checkout.html', context)
        else:
            conn.close()
            return render(request, 'checkout.html')
    else:
        # Customer session is not active, redirect to the login page
        return redirect('login')




# Modify the edit_customer function
def edit_customer(request, cust_id):
    if 'name' in request.session:
        # Add your database connection details here
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="usdk"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer_reg WHERE cust_id = %s", (cust_id,))
        customer_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if customer_data:
            customer = {
                'cust_id': customer_data[0],
                'name': customer_data[1],
                'password': customer_data[2],
                'email': customer_data[3],
                'phone': customer_data[4],
                'gender': customer_data[5]
            }
        else:
            customer = None

        return render(request, 'edit_customer.html', {'customer': customer})
    else:
        return redirect('login')
    


    

# Modify the update_customer function
def update_customer(request):
    if 'name' in request.session:
        if request.method == 'POST':
            cust_id = request.POST.get('cust_id')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            # Add your database connection details here

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="usdk"
            )
            cursor = conn.cursor()

            cursor.execute(
                "UPDATE customer_reg SET name = %s, email = %s, phone_no = %s,gender= %s WHERE cust_id = %s",
                (name, email, phone, gender, cust_id)
            )

            conn.commit()

            cursor.close()
            conn.close()

        return redirect('myaccount')
    else:
        return redirect('login')
