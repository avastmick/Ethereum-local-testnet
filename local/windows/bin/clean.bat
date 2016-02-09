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

set DATA-DIR=C:\Users\Mick\Documents\GitHub\Ethereum-local-testnet\**\data\chaindata
@echo on
echo %DATA-DIR%
REM rmdir -S -Q %DATA-DIR%
