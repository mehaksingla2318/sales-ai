import os
from fastapi import FastAPI, UploadFile, Form
import pandas as pd
from groq import Groq
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.post("/upload")
async def upload(file: UploadFile, email: str = Form(...)):

    df = pd.read_csv(file.file)

    data = df.to_string()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this sales data:\n{data}"
            }
        ]
    )

    summary = response.choices[0].message.content

    msg = MIMEText(summary)
    msg["Subject"] = "Sales Summary"
    msg["From"] = "mehakgupta2318@gmail.com"
    msg["To"] = email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("mehakgupta2318@gmail.com", "exwj qjyk tryo hkxb")
    server.send_message(msg)
    server.quit()

    return {"summary": summary}