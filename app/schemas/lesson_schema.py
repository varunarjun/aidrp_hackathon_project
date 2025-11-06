from pydantic import BaseModel

class LessonCreate(BaseModel):
    title: str
    description: str
    video_url: str


class LessonResponse(BaseModel):
    id: int
    module_id: int
    title: str
    description: str
    video_url: str

    class Config:
        orm_mode = True
