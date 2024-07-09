// edit based on your project path
module.exports = {
    apps: [{
      name: "BrainSpark",
      script: "/home/p/production/BrainSpark/venv/bin/gunicorn",
      args: "--config gunicorn_config.py core.wsgi:application",
      cwd: "/home/p/production/BrainSpark",
      interpreter: "/home/p/production/BrainSpark/venv/bin/python",
    }]
  }