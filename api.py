from fastapi import APIRouter,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

temp=Jinja2Templates(directory='templates')
@router.get("/items",response_class=HTMLResponse)
async def get_items(request:Request):
    return temp.TemplateResponse('pagination.html',{"request":request})



@router.post("/items_data",response_class=HTMLResponse)
async def get_items(request:Request):
    form_data=await request.form()
    file=form_data.get('image')
    file.save(os.path.join("uploads",file))
    return temp.TemplateResponse('pagination.html',{"request":request})