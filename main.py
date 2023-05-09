from data.config import BaseConfig
from data.server import create_app

app = create_app(BaseConfig)


if __name__ == '__main__':
    app.run()
