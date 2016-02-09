@echo off
mode con:cols=240 lines=20
@title Ethereum testnet console
REM ##################################################
REM ## Initiates the Geth console with the local test block etc.  ##
REM ##                                                                                                    ##
REM ## Assumes that this is  Windows (given this is batch file)  ##
REM ## and that Chocolatey was used to install                            ##
REM ## As admin:                                                                                ##
REM ## cinst -y geth-stable

set GETH-DIR=C:\ProgramData\chocolatey\lib\geth-stable\tools\
set PATH=%PATH%;%GETH-DIR%

REM ## Sets up a local test Blockchain to use for development

geth --networkid 9876 --datadir ../data console
