from fastapi import FastAPI, HTTPException, Depends
import uvicorn

app = FastAPI()


@app.get('/')
async def root():
    return {'status': 'ok'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
