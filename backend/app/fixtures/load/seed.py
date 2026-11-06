import asyncio
import json
from pathlib import Path

from sqlalchemy import insert
from db.engine import async_session
from app.models.media import Media, media_genres
from app.models.genre import Genre

BASE_DIR = Path(__file__).resolve().parent.parent
FIXTURES_DIR = BASE_DIR / "fixtures"


def load_json(filename: str):
    with open(filename,
              "r",
              encoding="utf-8"
              ) as file:
        return json.load(file)


async def seed():
    async with async_session() as db:

        try:

            genres_fixture = load_json("app/fixtures/genres.json")
            media_fixture = load_json("app/fixtures/media.json")
            relations_fixture = load_json("app/fixtures/media_genres.json")

            # -----------------
            # Genres
            # -----------------

            genres = []

            for item in genres_fixture:
                genres.append(
                    Genre(
                        id=item["pk"],
                        name=item["fields"]["name"]
                    )
                )

            db.add_all(genres)

            await db.flush()

            # -----------------
            # Media
            # -----------------

            medias = []

            for item in media_fixture:
                fields = item["fields"].copy()

                fields.pop("genres", None)

                medias.append(
                    Media(
                        id=item["pk"],
                        **fields
                    )
                )

            db.add_all(medias)

            await db.flush()

            # -----------------
            # Media genres
            # -----------------

            relations = []

            for item in relations_fixture:
                relations.append(
                    {
                        "media_id": item["fields"]["media_id"],
                        "genre_id": item["fields"]["genre_id"]
                    }
                )

            await db.execute(
                insert(media_genres),
                relations
            )

            await db.commit()

            print("Seed completed")


        except Exception:

            await db.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(seed())
