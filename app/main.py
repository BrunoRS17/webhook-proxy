from fastapi import FastAPI

app = FastAPI(title="Webhook Proxy", version="1.0.0", description="Desenvolvido por Bruno Ribeiro") 

@app.get("/health", status_code=200)
async def heath_check():
    return {"satus": "ok"}

