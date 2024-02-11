import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from app.src.yt_handler import yt_dl


app = FastAPI()

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "flag": False},
    )


@app.post("/")
async def read_raw_link(request: Request, raw_yt_link: str = Form(...)):
    print("entry : ", raw_yt_link)
    try:
        global yt
        yt = yt_dl(url=raw_yt_link)
        return templates.TemplateResponse(
            name="index.html",
            context={
                "request": request,
                "flag": True,
                "video_title": yt.title,
                "thumbnail_url": yt.thumbnail_url,
                "streams": yt.get_organized_options(),
            },
        )
    except Exception as e:
        print("ERROR : ", e)
        return templates.TemplateResponse(
            name="index.html",
            context={
                "request": request,
                "flag": False,
                "error_message": f"ERROR! : {e}",
            },
        )


@app.post("/quality")
async def get_video_quality(request: Request):
    form_data = await request.form()
    button_value = form_data["button"]
    print(button_value)
    global vid_stream
    vid_stream = yt.streams.get_by_itag(itag=int(button_value))
    print(vid_stream)
    try:
        return templates.TemplateResponse(
            name="index.html",
            context={
                "request": request,
                "flag": True,
                "video_title": yt.title,
                "thumbnail_url": yt.thumbnail_url,
                "streams": yt.get_organized_options(),
                "selected": True,
            },
        )
    except Exception as e:
        print("ERROR : ", e)
        return templates.TemplateResponse(
            name="index.html",
            context={
                "request": request,
                "flag": False,
                "error_message": f"ERROR! : {e}",
            },
        )


@app.get("/quality")
async def download_video(request: Request):
    try:
        download_path = vid_stream.download(output_path="app\\downloads")
        if os.path.exists(download_path):
            return FileResponse(
                path=download_path,
                media_type="video/mp4",
                filename=f"{vid_stream.title}.mp4",
            )
        else:
            return {"file": "does not exist"}
    except Exception as e:
        print("ERROR : ", e)
        return templates.TemplateResponse(
            name="index.html",
            context={
                "request": request,
                "flag": False,
                "error_message": f"ERROR! : {e}",
            },
        )
