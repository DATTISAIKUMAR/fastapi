from fastapi import FastAPI,Request
from pydantic import BaseModel,validator,Field,EmailStr
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from model import User
from math import ceil
from api import router

app=FastAPI()

app.include_router(router,tags=['items'])




class Items(BaseModel):
    name:str
    email:str
    phone_number:str


    @validator('phone_number')
    def hello(value):
        if(len(value)==10):
            return value
        return "enter valid phone number..."


  

temp=Jinja2Templates(directory="templates")

@app.get('/',response_class=HTMLResponse)
async def hello(request:Request):
    users=User.objects()
    page = 1
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = ceil(len(users) / per_page)
    paginated_data = users[start:end]
    content= {
        "start":start,
        "total_pages": total_pages,
        "request":request,
        'users':paginated_data
    }

    return temp.TemplateResponse('index.html',content)


@app.post('/homepage',response_class=HTMLResponse)
async def homepage(request:Request):
    form_data=await request.form()
    email=form_data.get('email')
    name=form_data.get('name')
    phone_number=form_data.get('phone_number')
    item=Items(name=name,email=email,phone_number=phone_number)
    user=User(
        name=item.name,
        email=item.email,
        phone_number=item.phone_number
    )
    user.save()
    users=User.objects()
    page = 1
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = ceil(len(users) / per_page)
    paginated_data = users[start:end]
    content= {
        "start":start,
        "total_pages": total_pages,
        "request":request,
        'users':paginated_data
    }
 
    return temp.TemplateResponse('index.html',content)


@app.get('/delete/{userid}')
async def delete_page(userid:str,request:Request):
    user_querset=User.objects(id=userid).first()
    users=user_querset.delete()
    return RedirectResponse(url=request.url_for('hello'))
   

@app.get('/edit/{userid}')
async def edit_page(userid:str,request:Request):
    user_queryset=User.objects(id=userid).first()
    email= request.query_params.get('email')
    name= request.query_params.get('name')
    phone_number= request.query_params.get('phone_number')
    item=Items(name=name,email=email,phone_number=phone_number)
    print(item)
    if item.name:
        user_queryset.name=item.name
    if item.email:
        user_queryset.email=item.email
    if item.phone_number:
        user_queryset.phone_number=item.phone_number
    user_queryset.save()

    return RedirectResponse(url=request.url_for('hello'))





@app.get('/edit_file/{userid}',response_class=HTMLResponse)
async def edit(userid:str,request:Request):
    return temp.TemplateResponse('file.html',{"request":request,'id':userid})




@app.get('/pagination/{page_num}',response_class=HTMLResponse)
async def pagination(page_num:int,request:Request):
    user=User.objects()
    page = page_num
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = ceil(len(user) / per_page)
    paginated_data = user[start:end]
    content= {
        "start":start,
        "total_pages": total_pages,
        "request":request,
        'users':paginated_data
    }
    return temp.TemplateResponse('index.html',content)




