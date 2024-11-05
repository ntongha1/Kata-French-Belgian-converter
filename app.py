from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from converter import translate_to_french

# Initialize the FastAPI app
app = FastAPI()

@app.get("/translate")
async def translate(number: int = Query(..., description="The number to translate")):
    """
    Endpoint to translate a number to its French word equivalent.

    Args:
        number (int): The number to be translated.

    Returns:
        dict: A dictionary containing the French translation.
    """
    try:
        # Translate the number using the imported function
        translated_number = translate_to_french(number)
        return {"translation": translated_number}
    
    # Handle invalid number input
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Handle unexpected errors
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run the FastAPI app, use uvicorn
# Command: uvicorn main:app --reload
