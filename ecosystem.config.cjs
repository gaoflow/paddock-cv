// pm2 deployment for the paddock-cv dashboard.
//   pm2 start ecosystem.config.cjs   # launch / reload
//   pm2 save                         # persist across reboots
// Override the python interpreter with PYTHON_BIN if "python3" is not the one
// you want (e.g. a conda install).
const path = require("path");

module.exports = {
  apps: [
    {
      name: "f1-dashboard",
      namespace: "f1_engineer",
      script: process.env.PYTHON_BIN || "python3",
      args: "server.py --host 0.0.0.0 --port 8000",
      cwd: __dirname,
      interpreter: "none",
      autorestart: true,
      max_restarts: 10,
    },
  ],
};
