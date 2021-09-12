@echo off
setlocal

set TAG=%IMAGE_NAME%:%IMAGE_TAG%

docker build --rm -t %TAG% .
