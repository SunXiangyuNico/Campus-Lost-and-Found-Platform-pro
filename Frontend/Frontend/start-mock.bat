@echo off
echo 正在启动Mock服务器...
echo.
echo 请确保已安装Node.js和npm
echo.
echo 安装依赖...
npm install express cors jsonwebtoken
echo.
echo 启动服务器...
node mock-server.js
pause 