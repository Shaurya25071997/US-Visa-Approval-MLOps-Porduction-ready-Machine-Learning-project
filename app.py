from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from uvicorn import run as app_run
from typing import Optional

from us_visa.constants import APP_HOST, APP_PORT
from us_visa.pipeline.prediction_pipeline import USvisaData, USvisaClassifier
from us_visa.pipeline.training_pipeline import TrainPipeline

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# CORS middleware
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

    async def get_usvisa_data(self):
        form = await self.request.form()

        return {
            "continent": form.get("continent"),
            "education_of_employee": form.get("education_of_employee"),
            "has_job_experience": form.get("has_job_experience"),
            "requires_job_training": form.get("requires_job_training"),
            "no_of_employees": form.get("no_of_employees"),
            "company_age": form.get("company_age"),
            "region_of_employment": form.get("region_of_employment"),
            "prevailing_wage": form.get("prevailing_wage"),
            "unit_of_wage": form.get("unit_of_wage"),
            "full_time_position": form.get("full_time_position"),
        }


@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("usvisa.html", {"request": request, "context": "Rendering"})


@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful !!")

    except Exception as e:
        return Response(f"Error Occurred! {e}")


@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        data = await form.get_usvisa_data()

        usvisa_data = USvisaData(**data)

        usvisa_df = usvisa_data.get_usvisa_input_data_frame()

        model_predictor = USvisaClassifier()
        value = model_predictor.predict(dataframe=usvisa_df)[0]

        status = "Visa-approved" if value == 1 else "Visa Not-Approved"

        return templates.TemplateResponse(
            "usvisa.html", {"request": request, "context": status}
        )

    except Exception as e:
        return {"status": False, "error": f"{e}"}


if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)
