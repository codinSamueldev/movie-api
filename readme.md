# Key Notes

I am storing most valuables commands, insights, notes and things to keep in mind when using FastAPI.

## Commands
### Installation
Best practices when installing any framework/library in Python, we must create and activate a virtual environment.
In order to create and activate virtual environments, check this out:
Create a virtual environment
```bash
python3 -m venv virtualEnvironmentName
```
For **MacOS** and **Linux** users, activate the virtual environment with the following command
```bash
source virtualEnvironmentName/bin/activate
```
For **Windows** users, activate the virtual environment with the following command
```bash
virtualEnvironmentName/Scripts/activate
```

> "Great! Now that the virtual environment is activated, we can install *FastAPI* and *uvicorn*."

FastAPI installation
```bash
pip install fastapi
```
Then, uvicorn installation
```bash
pip install uvicorn
```

### Running our API
Now, let's say you already created your API but, how do we know if it is working as it should?
Good news, here are the *uvicorn* commands so as to run our API, change its port, set up reload functionality so we can add new features and we can see it instantly, or add a host so anyone with your network can see what are you developing.

Basic command
```bash
uvicorn main:app --reload
```
Set up a port
```bash
uvicorn main:app --reload --port 5000
```
Set up a host, so anyone can see your API locally
```bash
uvicorn main:app --reload --port 5000 --host 0.0.0.0
```