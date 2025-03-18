# Todo App API

## Installation
1. Create virtual environment:
    ```
    python -m venv .venv
    ```
2. Activate the environment:
	- Linux/macOS: 
	``` 
	source .venv/bin/activate
	```
	- Windows:
	 ```
	 .venv\Scripts\activate
	 ```
3. Install packages:
	```
	pip install -r requirements.txt
	```
5. Migrate if running in local DB:
	```
	python manage.py migrate
	```
	
## Dotenv
In order to use the `dotenv` package, you will need to create a _.env_ file in the root of your project. You can change the location of the file by modifying this line in the `settings.py` file:
```python
# Load environment variables from .env
load_dotenv(os.path.join(BASE_DIR, '.env'))
```
You can find the required parameters for _.env_ in _.env.example_ file.

## Development Server
To run the development server, just run the command:
```
python manage.py runserver
```

### Running in Docker
To run the development server in Docker, use the following command:
```
docker-compose up --build
```
This will run 2 services:
- MySQL database
- Django API
