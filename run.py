import os

from src.app import create_app

if __name__ == '__main__':
  env_name = os.getenv('FLASK_ENV')
  app = create_app(env_name)
  # run app
  app.run(host="10.24.7.151", port=80)
