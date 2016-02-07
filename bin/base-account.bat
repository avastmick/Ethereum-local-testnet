@echo off
mode con:cols=170 lines=20
@title Initialise Ethereum testnet Blockchain
REM ##################################################
REM ## Initiates the Geth console with the local test block etc.  ##
REM ##                                                                                                    ##
REM ## Assumes that this is  Windows (given this is batch file)  ##
REM ## and that Chocolatey was used to install                            ##
REM ## As admin:                                                                                ##
REM ## cinst -y geth-stable

set GETH-DIR=C:\ProgramData\chocolatey\lib\geth-stable\tools\
set PATH=%PATH%;%GETH-DIR%

mkdir ..\dataDir
@echo on
geth  --datadir ../dataDir --networkid 9876 --jspath "../conf/BaseAccount.js" --exec js

REM ## Initialise blockchain with base account
REM geth --datadir ../dataDir --networkid 9876 --password ../conf/testnet-pwd account new
