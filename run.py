import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",         # Looks for the 'app' object in the 'main.py' file
        host="0.0.0.0",     # Makes the server accessible on your network
        port=5001,          # The port number for the API
        reload=True         # Automatically restarts the server on code changes
    )