import os

import uvicorn


import sys
project_root = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, project_root)
if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=5001,
        reload=True
    )