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

## Fixtures
The provided fixtures include data for Todo, Comments, and User models. You can login with any of the provided users (password is '1234' for any user) or just sign up with a new one created by you.  
To load the fixtures into the app in order to have some sample data, just run the following command:
- Linux/macOS: 
	```
	python manage.py loaddata fixtures/*.json
	```
- Windows:
	```
	python manage.py loaddata fixtures\users.json
	python manage.py loaddata fixtures\todos.json
	```


## Coverage
To run the tests and see a coverage report, run the following command:
```
coverage run --rcfile=.coveragerc manage.py test && coverage report
```

## Running in Docker
To run the development server in Docker, use the following command:
```
docker-compose up --build
```
This will run 2 services:
- MySQL database
- Django API

Once the services are up, you have to run the migrations. To do this:
1. Find out Django App container ID:
	```
	docker container ls
	```
	It should have a similar name to `todo-app-bluequo-backend`.

2. Execute bash inside the container:
	```
	docker exec -it <CONTAINER_ID> bash
	```
3. Once inside the container, you can run any of the already seen commands (migrations command will be required if using Docker database):
	```
	python manage.py migrate

	python manage.py loaddata fixtures/*.json

	coverage run --rcfile=.coveragerc manage.py test && coverage report
	```
