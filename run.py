import os

from src.app import create_app

if __name__ == '__main__':
  env_name = os.getenv('FLASK_ENV')
  app = create_app(env_name)
  # run app
<<<<<<< HEAD
  app.run(host="192.168.43.112", port=5555)
=======
  app.run(host="192.168.1.49", port=5555)
>>>>>>> origin/master
