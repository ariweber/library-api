from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
from database.member_db import MemberDB
from database.connection import DBconnection


class CreateMember(BaseModel):
    name: str
    email: str
    is_activae: bool = True
    borrows_total: int | None = None



class UpdateMember(BaseModel):
    name: str | None =  None
    email: str | None = None
    is_activae: bool | None = None
    borrows_total: int | None = None

crud = MemberDB(DBconnection())


router = APIRouter(prefix="/members")


@router.post("/", status_code=201)
def add_abook(data: CreateMember):
   return crud.create_member(data.model_dump())

@router.get("/")
def get_all_members():
    return crud.get_all_members()
    

@router.get("/{id}")
def get_by_members_id(id):
    member = crud.get_member_by_id(id)
    if not member:
        raise HTTPException(404, f"member{id} not found")
    return member


@router.put("/{id}/deactivate")
def deactivate(id: int):
    check = crud.deactivate_member(id)
    if not check:
        raise HTTPException(400, "Operation failed")
    return {id: "Updated successfully"}

@router.put("/{id}/activate")
def activate(id: int):
    check = crud.activate_member(id)
    if not check:
        raise HTTPException(400, "Operation failed")
    return {id: "Updated successfully"}



    

