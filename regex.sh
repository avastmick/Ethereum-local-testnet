#!/bin/bash


enodeurl="enode://2f9fad543af751f0fcf46d4bc3d4835e56170b74e94afdc823ab96b01b39ce5e437cab71e8070d0a5bda9282c690cc3b13bc161f1fc1d43268ed6b25977961fd@[::]:30802?discport=0"

echo $enodeurl


enodeurl_t=$( echo $enodeurl | perl -pe "s/(\?.*)$//g" )
echo BOB $enodeurl_t
