import uvicorn

from expense_tracker import app


def runserver(host: str, port: int):
    uvicorn.run(app, host=host, port=port, log_level="debug")


if __name__ == "__main__":
    # TODO add command line args
    runserver("localhost", 8000)
