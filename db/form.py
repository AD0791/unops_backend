
from typing import List
from db import db
from models.form import Form

form_collection = db.forms
async def retrieveForm(name:str,type:str)->Form:
    __form = form_collection.find_one({"name":name,"type":type})
    if __form:
        return Form(__form)

async def createForm(form:Form)->Form:
    result = await form_collection.insert_one(form.dict())
    if result:
        return form

async def createForms(forms:List[Form])->List[Form]:
    result = await form_collection.insert_many(forms)
    if result:
        return forms

async def updateForm(form:Form)->Form:
    result = await form_collection.update_one({"name":form.name,"type":form.type},{"$set":form.dict()})
    if result:
        return form

async def updateForms(forms:List[Form])->List[Form]:
    result = await form_collection.insert_many(forms)
    if result:
        return forms