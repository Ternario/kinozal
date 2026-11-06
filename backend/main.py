from fastapi import FastAPI, HTTPException, Depends
import uvicorn

from app.routers.media import router as media_router

app = FastAPI(title='Media API Test')

app.include_router(media_router)


@app.get('/')
async def root():
    return {'status': 'ok'}


if __name__ == '__main__':
    # uvicorn.run('main:app', reload=True)

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
