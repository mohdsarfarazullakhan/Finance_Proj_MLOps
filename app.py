from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run

from typing import Optional

from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import VehicleData, VehicleDataClassifier
from src.pipline.training_pipeline import TrainPipeline

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    def __init__(self, request: Request):
        self.request = request

    async def get_vehicle_data(self):
        form = await self.request.form()

        self.Gender = int(form.get("Gender"))
        self.Age = int(form.get("Age"))
        self.Driving_License = int(form.get("Driving_License"))
        self.Region_Code = float(form.get("Region_Code"))
        self.Previously_Insured = int(form.get("Previously_Insured"))
        self.Annual_Premium = float(form.get("Annual_Premium"))
        self.Policy_Sales_Channel = float(form.get("Policy_Sales_Channel"))
        self.Vintage = int(form.get("Vintage"))
        self.Vehicle_Age_lt_1_Year = int(form.get("Vehicle_Age_lt_1_Year"))
        self.Vehicle_Age_gt_2_Years = int(form.get("Vehicle_Age_gt_2_Years"))
        self.Vehicle_Damage_Yes = int(form.get("Vehicle_Damage_Yes"))


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        "vehicledata.html",
        {"request": request, "result": None},
    )


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful!!!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_vehicle_data()

        vehicle_data = VehicleData(
            Gender=form.Gender,
            Age=form.Age,
            Driving_License=form.Driving_License,
            Region_Code=form.Region_Code,
            Previously_Insured=form.Previously_Insured,
            Annual_Premium=form.Annual_Premium,
            Policy_Sales_Channel=form.Policy_Sales_Channel,
            Vintage=form.Vintage,
            Vehicle_Age_lt_1_Year=form.Vehicle_Age_lt_1_Year,
            Vehicle_Age_gt_2_Years=form.Vehicle_Age_gt_2_Years,
            Vehicle_Damage_Yes=form.Vehicle_Damage_Yes,
        )

        vehicle_df = vehicle_data.get_vehicle_input_data_frame()

        model_predictor = VehicleDataClassifier()
        value = model_predictor.predict(dataframe=vehicle_df)[0]

        status = "Response-Yes" if value == 1 else "Response-No"

        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "result": status},
        )

    except Exception as e:
        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "result": f"Error: {str(e)}"},
        )


if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=5000)