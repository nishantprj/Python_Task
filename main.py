import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi import FastAPI,Request
import uvicorn
import shutil
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="amaan",
    database="mydatabase"
)
mycursor = mydb.cursor()

app = FastAPI()

credits_df= pd.read_csv("destination.csv")


rows = len(credits_df.axes[0])

for i in range(rows):
        sql = "INSERT INTO Customers (Charger,Voltage,Curent,Temp,S1,S2,S3,Start_Time,End_Time,Remaining_Time, Current_Tim) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (str(credits_df.iloc[i][0]), str(credits_df.iloc[i][1]), str(credits_df.iloc[i][2]) ,str(credits_df.iloc[i][3]) ,str(credits_df.iloc[i][4]), str(credits_df.iloc[i][5]),str(credits_df.iloc[i][6]),str(credits_df.iloc[i][7]),str(credits_df.iloc[i][8]),str(credits_df.iloc[i][9]),str(credits_df.iloc[i][10]))
        mycursor.execute(sql, val) 
mydb.commit()

print("Tis is working ")

def location(col, n):
    l=[]
    for i in credits_df[col]:
        l.append(i)
    return(l[n])
    
#print(location(1000, 1000))


@app.get("/")
async def read_item(request: Request):
    return("hi")


@app.get("/{column}/{no}")
def getdata(column:str, no:int):
    if column=='title':
        return {'movie_name':(location(column, no))}
    elif column=='movie_id':
        return {'movie_id':(location(column, no))}
    else:
        return {'data':(location(column, no))}
    

templates = Jinja2Templates(directory="templates")
@app.get("/upload/", response_class=HTMLResponse)
async def upload(request: Request):
   return templates.TemplateResponse("uploadfile.html", {"request": request})

@app.post("/uploader/")
async def create_upload_file(file: UploadFile = File(...)):
   with open("destination.csv", "wb") as buffer:
      shutil.copyfileobj(file.file, buffer)
   return {"filename": file.filename}