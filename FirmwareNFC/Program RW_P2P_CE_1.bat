CLS
@echo off
rem This is a small helper script that programs a prebuilt binary for a device using MSP430Flasher
rem
rem Eric Chen, MSP430 Applications, Texas Instruments, Inc.
rem Last modified: 02/28/2014
:input
@echo MSP-EXP430F5529-LaunchPad Firmware Programmer

set device=MSP430F5529
set firmware=RW_P2P_CE_1.hex

@echo Programing %firmware% into %device% ......
..\MSP430Flasher\MSP430Flasher.exe -n %device% -w %firmware% -v -g -z [VCC]

pause