#!/usr/bin/env python
"""
Startup script for the backend server.
This ensures the correct working directory and environment.
"""
import os
import sys

# Set the working directory to the backend folder
backend_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(backend_dir)

# Add backend directory to Python path
sys.path.insert(0, backend_dir)

# Start uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
        reload_dirs=[backend_dir]
    )
