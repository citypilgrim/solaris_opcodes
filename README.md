# solaris_opcodes

Operational code for solaris server

## Lidar laptop Setup

Some setup is required on the lidar laptop (Windows platform) before being able to run:
1. Enabling promptless SSH
    a. OpenSSH Server additional feature is installed
    b. solaris server public key is added to lidar laptop `C:\Users\mpluser\.ssh\authorized_keys'
    c. Comment out the following lines from `C:\DataProgram\ssh\sshd_config`
	i. #Match Group administrators
	ii. #       AuthorizedKeysFile __PROGRAMDATA__/ssh/administrators_authorized_keys
    d. restart OpenSSH services
2. Add `C:\Users\mpluser\Desktop\smmpl_opcodes\window_files\rsync` to lidar laptop PATH and restart OpenSSH services

## Usage

### Computing cloud product and writing to file

Will utilise the latest dataset avaiable to get a complete atmospheric profile sweep of cloud products.

```
python -m solaris_opcodes.product_calc.cloudproduct_print
```

### Pulling latest data

python -m solaris_opcodes.lidardata_pull

### Horizontal lidar sweep calibration check

Edit the mutable parameters in the module stated below accordingly and run
```
python -m solaris_opcodes.horisweep_calicheck
```

## Dependencies

1. A working `rsync` with it's dependencies on solaris server