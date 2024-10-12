// edit based on your project path
module.exports = {
    apps: [{
      name: "BrainSpark-8004",
      script: "/home/pi/production/BrainSpark/venv/bin/gunicorn",
      args: "--config gunicorn_config.py core.wsgi:application",
      cwd: "/home/pi/production/BrainSpark",
      interpreter: "/home/pi/production/BrainSpark/venv/bin/python",
    }]
  }