from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
from typing import Optional

# Importing constants and pipeline modules
from src.constants import APP_HOST, APP_PORT
from src.pipline.prediction_pipeline import VehicleData, VehicleDataClassifier
from src.pipline.training_pipeline import TrainPipeline

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.Gender: Optional[int] = None
        self.Age: Optional[int] = None
        self.Driving_License: Optional[int] = None
        self.Region_Code: Optional[float] = None
        self.Previously_Insured: Optional[int] = None
        self.Annual_Premium: Optional[float] = None
        self.Policy_Sales_Channel: Optional[float] = None
        self.Vintage: Optional[int] = None
        self.Vehicle_Age_lt_1_Year: Optional[int] = None
        self.Vehicle_Age_gt_2_Years: Optional[int] = None
        self.Vehicle_Damage_Yes: Optional[int] = None

    async def get_vehicle_data(self):
        form = await self.request.form()
        # Explicit casting to prevent "unhashable type" or model type errors
        self.Gender = int(form.get("Gender", 0))
        self.Age = int(form.get("Age", 0))
        self.Driving_License = int(form.get("Driving_License", 0))
        self.Region_Code = float(form.get("Region_Code", 0.0))
        self.Previously_Insured = int(form.get("Previously_Insured", 0))
        self.Annual_Premium = float(form.get("Annual_Premium", 0.0))
        self.Policy_Sales_Channel = float(form.get("Policy_Sales_Channel", 0.0))
        self.Vintage = int(form.get("Vintage", 0))
        self.Vehicle_Age_lt_1_Year = int(form.get("Vehicle_Age_lt_1_Year", 0))
        self.Vehicle_Age_gt_2_Years = int(form.get("Vehicle_Age_gt_2_Years", 0))
        self.Vehicle_Damage_Yes = int(form.get("Vehicle_Damage_Yes", 0))

@app.get("/", tags=["authentication"])
async def index(request: Request):
    # Use "result" instead of "context" to avoid Jinja2 reserved keyword issues
    return templates.TemplateResponse(
            "vehicledata.html", {"request": request, "result": None})

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
            Vehicle_Damage_Yes=form.Vehicle_Damage_Yes
        )

        vehicle_df = vehicle_data.get_vehicle_input_data_frame()
        model_predictor = VehicleDataClassifier()
        value = model_predictor.predict(dataframe=vehicle_df)[0]

        status = "Response-Yes" if value == 1 else "Response-No"

        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "result": str(status)},
        )
        
    except Exception as e:
        # Returning as a dictionary can sometimes cause the 'unhashable' error in templates
        return templates.TemplateResponse(
            "vehicledata.html",
            {"request": request, "result": f"Error: {str(e)}"},
        )

if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)