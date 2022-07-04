from TODOS.model import users,todos

#authentication

def signin_required(fn):
    def wrapper(*args,**kwargs):
        if "user" in session:
            return fn(*args,**kwargs)
        else:
            print("you must log in")
    return wrapper

def authenticate(*args,**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user_data=[user for user in users if user["username"]==username and user["password"]==password]
    return user_data

# print(authenticate(username="akhil",password="Password@123"))

#login
session={}
class Signin:
    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=authenticate(username=username,password=password)
        if user:
            print("login success")
            session["user"]=user[0]
        else:
            print("Invalid credentials")

login=Signin()
login.post(username="akhil",password="Password@123")
print(session)

#alltodosview:

class Alltodosview:
    @signin_required
    def get(self,*args,**kwargs):
        return todos

all_todos=Alltodosview()
print(all_todos.get())

#createnew todos

class Newtodoview:
    @signin_required
    def post(self,*args,**kwargs):

        userId=session["user"]["id"]
        kwargs["userId"]=userId
        print(kwargs)
        todos.append(kwargs)
        print(todos)

new_todo=Newtodoview()
new_todo.post(todoId=9,
              task_name="phnbill",
              completed=True
              )


#mytodosview:

class Mytodoslistview:
    @signin_required
    def get(self,*args,**kwargs):
        userid=session["user"]["id"]
        my_todos=[todo for todo in todos if todo["userId"]==userid]
        return my_todos


mytodos=Mytodoslistview()
print(mytodos.get())

#updating and deleting todos

class Tododetailview:


    def get_object(self,id):
        todo=[todo for todo in todos if todo["todoId"]==id]
        return todo


    def get(self,*args,**kwargs):
        todo_Id=kwargs.get("todo_Id")
        todo=self.get_object(todo_Id)
        return todo

    @signin_required
    def put(self,*args,**kwargs):
        todo_Id=kwargs.get("todo_Id")
        data=kwargs.get("data")
        todo_data=self.get_object(todo_Id)
        if todo_data:
            todo_update=todo_data[0]
            todo_update.update(data)
            return(todos)

    @signin_required
    def delete(self,*args,**kwargs):
        todo_Id=kwargs.get("todo_Id")
        todo_data=self.get_object(todo_Id)

        if todo_data:
            todo_delete=todo_data[0]
            todos.remove(todo_delete)
            print("todo removed")
            print(len(todos))


data={
    "task_name":"house_rent"
}

todo_detail=Tododetailview()
# print(todo_detail.get(todo_id=5))
print(todo_detail.put(todo_Id=3,data=data))
todo_detail.delete(todo_Id=3)

@signin_required
def logout(*args,**kwargs):
    session.pop("user")

logout()
print(session)