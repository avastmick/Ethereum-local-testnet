@echo off
mode con:cols=170 lines=20
REM set the path
set GETH-DIR=C:\ProgramData\chocolatey\lib\geth-stable\tools\
set PATH=%PATH%;%GETH-DIR%
REM fire up a CMD terminal to run Geth
start cmd /d /k title Ethereum Geth Command Terminal
