import uvicorn
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pymongo
import datetime
import json


app = FastAPI()

myclient = pymongo.MongoClient("mongodb+srv://root:IOTA@mydata.5wjhx.mongodb.net/")
mydb = myclient["iot"]
mycol = mydb["nhom2iott"]

API_KEY = "nhom2_iot"

class Item(BaseModel):
    id: int
    device: str
    data1: float
    data2: float
    time: str
    led1: str
    led2: str
    led3: str


def validate_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")


@app.get("/get")
async def get_data():
    data = mycol.find().sort("_id", -1).limit(1)
    dict = {
        "id": data[0]['id'],
        "device": data[0]['device'],
        "time": data[0]['time'],
        "humi": data[0]['humi'],
        "temp": data[0]['temp'],
    }
    return dict


@app.post("/update_post")
async def update_data_post(item: Item, api_key: str = Header(None, alias="api_key")):
    validate_api_key(api_key)

    dict_data = {
        "id": item.id,
        "device": item.device,
        "time": item.time,
        "humi": item.data1,
        "temp": item.data2,
        "led1": item.led1,
        "led2": item.led2,
        "led3": item.led3
    }
    result = mycol.insert_one(dict_data)

    dict_data['_id'] = str(result.inserted_id)
    return {"status": "success", "data": dict_data}


@app.get("/getlast")
async def get_data(limit: int = 1):
    data = list(mycol.find().sort("_id", -1).limit(limit))
    for d in data:
        d['_id'] = str(d['_id'])

    return data


@app.get("/get_by_time")
async def get_data_by_time(start_time: str, end_time: str):
    try:
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'.")

    query = {"time": {"$gte": start_time, "$lte": end_time}}
    data = list(mycol.find(query).sort("time", 1))

    for d in data:
        d['_id'] = str(d['_id'])

    return data


# New /graph endpoint to display temperature and humidity graph using Chart.js
@app.get("/graph", response_class=HTMLResponse)
async def get_graph():
    data = list(mycol.find().sort("time", 1))
    if not data:
        raise HTTPException(status_code=404, detail="No data available")

    times = [d['time'] for d in data]
    temps = [d['temp'] for d in data]
    humis = [d['humi'] for d in data]

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Temperature and Humidity Graph</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h2>Temperature and Humidity Over Time</h2>
        <canvas id="myChart" width="400" height="200"></canvas>
        <script>
            const labels = {json.dumps(times)};
            const data = {{
                labels: labels,
                datasets: [
                    {{
                        label: 'Temperature (°C)',
                        data: {json.dumps(temps)},
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    }},
                    {{
                        label: 'Humidity (%)',
                        data: {json.dumps(humis)},
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    }}
                ]
            }};
            const config = {{
                type: 'line',
                data: data,
                options: {{
                    scales: {{
                        x: {{
                            type: 'category',
                            labels: {json.dumps(times)}
                        }}
                    }}
                }}
            }};
            var myChart = new Chart(
                document.getElementById('myChart'),
                config
            );
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.134", port=9500)
