from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "RushPlate API",
        "version": "v2.0.0",
        "message": "Pipeline tested successfully!",
        "deployed_by": "AWS CodePipeline",
        "timestamp": "2026-03-11"
    }
