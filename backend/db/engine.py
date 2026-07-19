from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True, pool_pre_ping=True)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# def get_session():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
