from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI()


class User(BaseModel):
    u_id: int
    name: str
    email: str
    password: str


users = []


@app.get('/users/', response_model=list[User])
async def show_users():
    return [user for user in users]


@app.get('/users/{u_id}', response_model=User)
async def show_users(u_id: int):
    return [user for user in users if user.u_id == u_id]


@app.post('/users/', response_model=User)
async def create_user(user: User):
    if users:
        for i in range(len(users)):
            if users[i].u_id == user.u_id:
                raise HTTPException(
                    status_code=404, detail="Пользователь с таким id уже существует")
    users.append(user)
    return user


@app.put('/users/{u_id}/', response_model=User)
async def change_user(u_id: int, user:User):
    for i in range(len(users)):
        if users[i].u_id == u_id:
            users[i].name = user.name
            users[i].email = user.email
            users[i].password = user.password
            return users[i]
    raise HTTPException(
        status_code=404, detail="Пользователя с таким id не существует")


@app.delete('/users/{u_id}/')
async def delete_user(u_id: int):
    for i in range(len(users)):
        if users[i].u_id == u_id:
            users.pop(i)
            return {u_id: 'Пользователь удален'}
    return {u_id: 'Пользователь ненайден'}


if __name__ == '__main__':
    uvicorn.run('Ex009:app', host='localhost', port=8000, reload=True)
