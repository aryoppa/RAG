from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# model Pydantic untuk input data (opsional)
class InputData(BaseModel):
    no: Optional[str] = None  # Opsional

class SSMResponse(BaseModel):
    tracking_number: str
    status: str
    details: str

# Dummy endpoint untuk "SSM QC" menggunakan GET method
@app.get("/api/statusAju", response_model=SSMResponse)
async def ssm_qc(no: str):
    return SSMResponse(
        tracking_number=no,
        status="Pengajuan Completed",
        details="Pengajuan completed successfully on 2024-06-17."
    )

# Dummy endpoint untuk "SSM QC" umenggunakan GET method
@app.get("/api/ssmQC", response_model=SSMResponse)
async def ssm_qc(no: str):
    return SSMResponse(
        tracking_number=no,
        status="QC Passed",
        details="Quality control completed successfully on 2024-06-17."
    )

# Dummy endpoint untuk "SSM Perizinan" menggunakan GET method
@app.get("/api/ssmPerizinan", response_model=SSMResponse)
async def ssm_perizinan(no: str):
    return SSMResponse(
        tracking_number=no,
        status="Approved",
        details="License approval completed on 2024-06-17."
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
