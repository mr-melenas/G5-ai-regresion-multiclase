import uvicorn
import os
import sys

# Asegurarse de que el directorio actual esté en el path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Ejecutar la aplicación FastAPI con uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    print("API iniciada en http://localhost:8000")