@echo off
setlocal

set TAG=%IMAGE_NAME%:%IMAGE_TAG%

docker run --rm -it ^
    -p 8000:80/tcp ^
    -v %WORKSPASE%/tests/files:/v8i ^
    -e V8I_FOLDER="/v8i" ^
    -e APP_HOST="http://127.0.0.1:8000" ^
    %TAG%
