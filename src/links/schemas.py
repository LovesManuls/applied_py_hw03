from datetime import datetime

from pydantic import BaseModel


class LinkCreateUserInput(BaseModel):
    orig_url: str
    short_code: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "orig_url": "https://www.wikipedia.org",
                    "short_code": "null"
                },
                {
                    "orig_url": "https://recsyswiki.com/wiki/Main_Page",
                    "short_code": "RecSys"
                }
            ]
        }
    }


class RedirectionUserInput(BaseModel):
    short_code: str

    class Config:
        json_schema_extra = {
            "example": {
                "short_code": "mfMyag"
            }
        }
