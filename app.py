from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from converter import FrenchNumberTranslator

# Initialize the FastAPI app
app = FastAPI()

# Reuse a single instance of FrenchNumberTranslator
translator = FrenchNumberTranslator()

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
        # Translate the number using the reusable translator instance
        translated_number = translator.convert_number(number)
        return {"translation": translated_number}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
