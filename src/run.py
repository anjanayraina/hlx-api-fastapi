import os
import sys
import uvicorn

if __name__ == "__main__":
    # This makes the script runnable from anywhere by adding the project root to the path.
    # The project root is the parent directory of 'src', where this file lives.
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, project_root)

    # Now that the project root is on the path, uvicorn can reliably find 'src.main'
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=5001,
        reload=True,
    )
