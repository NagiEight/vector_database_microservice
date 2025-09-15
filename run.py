import multiprocessing
import os
import sys
import time

def run_fastapi_backend():
    """Runs the FastAPI backend using Uvicorn."""
    print("Starting FastAPI Backend...")
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(project_root, 'vector_db'))
    
    from main import app as fastapi_app
    import uvicorn
    uvicorn.run(fastapi_app, host='0.0.0.0', port=8000)

def run_webgui_frontend():
    """Runs the simple Python web GUI server."""
    print("Starting Web GUI Frontend...")
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(project_root, 'webgui'))
    
    import server
    server.run_server()

if __name__ == '__main__':
    backend_process = multiprocessing.Process(target=run_fastapi_backend)
    backend_process.start()

    time.sleep(5) 

    frontend_process = multiprocessing.Process(target=run_webgui_frontend)
    frontend_process.start()

    print("\n" + "="*50)
    print("All services are starting. Please wait a moment.")
    print("Web GUI is available at: http://localhost:8080/webgui")
    print("FastAPI API is available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop all services.")
    print("="*50 + "\n")

    try:
        backend_process.join()
        frontend_process.join()
    except KeyboardInterrupt:
        print("\nStopping services...")
        backend_process.terminate()
        frontend_process.terminate()
        backend_process.join()
        frontend_process.join()
        sys.exit(0)