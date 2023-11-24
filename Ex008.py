from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI()


class Task(BaseModel):
    t_id: int
    title: str
    description: str
    status: str


tasks = []


@app.get('/tasks/', response_model=list[Task])
async def show_tasks():
    return [task for task in tasks]


@app.get('/tasks/{t_id}', response_model=list[Task])
async def show_tasks(t_id: int):
    return [task for task in tasks if task.t_id == t_id]


@app.post('/tasks/{t_id}/{title}/{des}/{status}/', response_model=Task)
async def create_task(t_id: int, title: str, des: str, status: str):
    if tasks:
        for i in range(len(tasks)):
            if tasks[i].t_id == t_id:
                raise HTTPException(
                    status_code=404, detail="Задача с таким id уже существует")
    temp = Task(t_id=t_id, title=title, description=des, status=status)
    tasks.append(temp)
    return temp


@app.put('/tasks/{t_id}/{title}/{des}/{status}/', response_model=Task)
async def change_task(t_id: int, title: str, des: str, status: str):
    for i in range(len(tasks)):
        if tasks[i].t_id == t_id:
            tasks[i].title = title
            tasks[i].description = des
            tasks[i].status = status
            return tasks[i]
    raise HTTPException(
        status_code=404, detail="Задачи с таким id не существует")


@app.delete('/tasks/{t_id}/')
async def delete_task(t_id: int):
    for i in range(len(tasks)):
        if tasks[i].t_id == t_id:
            tasks.pop(i)
            return {t_id: 'Задача удалена'}
    return {t_id: 'Задача ненайдена'}


if __name__ == '__main__':
    uvicorn.run('Ex001:app', host='localhost', port=8000, reload=True)
