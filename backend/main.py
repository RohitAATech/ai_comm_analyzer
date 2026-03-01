from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer import analyze_communication
from sample_data import seed_database
 
# FastAPI app — equivalent to @SpringBootApplication
app = FastAPI(title="AI CCM Analyzer", version="1.0.0")
 
# Allow React frontend to call this API — like CORS config in Spring Security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
 
# Request DTO — like a @RequestBody POJO in Spring
class AnalyzeRequest(BaseModel):
    communication: str
 
# Seed DB on startup — like @PostConstruct
@app.on_event("startup")
async def startup_event():
    seed_database()
 
# Health check endpoint — GET /health
# Like @GetMapping("/health") returning ResponseEntity<String>
@app.get("/health")
def health():
    return {"status": "UP", "service": "AI CCM Analyzer"}
 
# Main analysis endpoint — POST /analyze
# Like @PostMapping("/analyze") returning ResponseEntity<AnalysisResult>
@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    if not request.communication or len(request.communication.strip()) < 10:
        return {"error": "Communication text is too short"}
    result = analyze_communication(request.communication)
    return {"input": request.communication, "analysis": result}
 
# Run with: uvicorn main:app --reload --port 8000
# Swagger UI auto-available at: http://localhost:8000/docs
