from datetime import datetime

import pydantic


class Monitoring(pydantic.BaseModel):
    execution_date: datetime
    success: pydantic.types.NonNegativeInt
    error: pydantic.types.NonNegativeInt

    class Config:
        allow_mutation = False
