import configparser
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn
import asyncio

from hzys import generate as his_generate
from res import check_and_download

app = FastAPI()


@app.get("/generate")
async def generate(
    reverse: bool,
    ysdd: bool,
    normalize: bool,
    speed: float,
    pitch: float,
    pause: float,
    sentence: str,
):
    try:
        voice = await his_generate(
            sentence, reverse, ysdd, normalize, speed, pitch, pause
        )
    except Exception:
        print("Failed to generate voice")
        raise HTTPException(status_code=204, detail="生成语音失败")
    return StreamingResponse(voice, media_type="audio/wav")


if __name__ == "__main__":
    asyncio.run(check_and_download())

    conf = configparser.ConfigParser()
    conf.read("config.ini", encoding="utf-8")
    # Melmodel = load_model(conf.get("model", "MELPATH"))
    uvicorn.run(
        "main:app", host=conf.get("net", "host"), port=int(conf.get("net", "port"))
    )
