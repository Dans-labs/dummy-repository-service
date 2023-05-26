import importlib
import logging

import uvicorn
from fastapi import FastAPI, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src import db, public, protected, pages
from src.commons import settings

__version__ = importlib.metadata.metadata(settings.SERVICE_NAME)["version"]

api_keys = [
    settings.DANS_DUMMY_INBOX_SERVICE_API_KEY
]  # Todo: This should be encrypted in the .secrets.toml

# Authorization Form: It doesn't matter what you type in the form, it won't work yet. But we'll get there.
# See: https://fastapi.tiangolo.com/tutorial/security/first-steps/
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # use token authentication


def api_key_auth(api_key: str = Depends(oauth2_scheme)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Forbidden"
        )


# settings = Dynaconf(
#     settings_files=[f"{current_directory}/conf/settings.toml", f"{current_directory}/conf/.secrets.toml"],
# )

log = logging.getLogger(__name__)
app = FastAPI(title=settings.FASTAPI_TITLE, description=settings.FASTAPI_DESCRIPTION,
              version=__version__)

pp = FastAPI()



app.include_router(
    public.router,
    tags=["Signposting"],
    prefix=""
)

app.include_router(
    protected.router,
    # tags=["Protected"],
    tags=["LDN Inbox"],
    prefix="",
    dependencies=[Depends(api_key_auth)]
)


app.include_router(
    pages.router,
    tags=["UI Pages"],
    prefix="/ui"
)


@app.get('/')
def info():
    logging.info("Dummy Signposting Generator")
    logging.debug("info")
    return {"name": "Dummy Repository Service", "version": __version__}

if __name__ == "__main__":

    sql_create_inbox_table = """ CREATE TABLE `inbox` (`id` uuid,`created_time` datetime,`updated_time` datetime,
                                       `deleted_time` datetime,`sender` text,`payload` text, `payload_turtle` text,`valid_rdf` numeric,PRIMARY KEY (`id`));"""
    # todo: if not found, creates one.

    # create a database connection
    conn = db.create_sqlite3_connection(settings.data_db_file)

    # create tables
    if conn is not None:
        # create inbox table
        db.create_table(conn, sql_create_inbox_table)
    else:
        print("Error! cannot create the database connection.")
    logging.info("Start")
    uvicorn.run("src.main:app", host="0.0.0.0", port=2907, reload=False)
