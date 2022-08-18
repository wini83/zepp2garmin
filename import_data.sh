#!/bin/bash

# Data for MQTT broker, skip if you are not using mqtt
# Allowed mqtt parameter is "off" or "on"
mqtt=off
password=password
user=admin

# Version Info
echo "Mi Body Composition Scale 2 Garmin Connect v4.3 (import_data.sh)"
echo ""

# Verification of mqtt parameter
if [ -z $mqtt ] ; then
	echo "* Empty parameter mqtt detected"
	exit 0
elif [[ $mqtt != "off" && $mqtt != "on" ]] ; then
	echo "* Bad parameter mqtt detected"
	exit 0
fi

# Creating data backup file
path=`cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd`
if [ ! -f $path/backup.csv ] ; then
	echo "* Creating backup.csv file, checking for new data"
	if [ $mqtt == "off" ] ; then
		echo "Weight;Impedance;Unix_Time;Data_Status;Bone_Mass;BMI;Fat;Water;Metabolic_Age;Muscle_Mass;Body_Type;Visceral_Fat;Upload_Time;Scale_Time" > $path/backup.csv
	else echo "Weight;Impedance;Unix_Time;Data_Status;Bone_Mass;BMI;Fat;Water;Metabolic_Age;Muscle_Mass;Body_Type;Visceral_Fat;Upload_Time;Scale_Time;Bat_in_V;Bat_in_%" > $path/backup.csv
	fi
else echo "* Backup.csv file exists, checking for new data"
fi

# Importing raw data from source (BLE or MQTT)
if [ $mqtt == "off" ] ; then
	if [ -z `hcitool dev | awk 'NR>1 {print $2}'` ] ; then
		echo "* No BLE device detected"
	else echo "* Importing data from BLE device"
		read_scale=`python3 -B $path/scanner_ble.py | awk 'END{print}'`
	fi
else echo "* Importing data from MQTT broker"
	read_scale=`mosquitto_sub -h localhost -t 'data' -u $user -P $password -C 1 -W 10`
fi

# Checking raw data
unixtime_scale=`echo $read_scale | awk -F ";" '{print $3}'`
if [ -z $unixtime_scale ] ; then
	if [ $mqtt == "off" ] ; then
		echo "* No BLE data from scale or incomplete"
	else echo "* No MQTT data, check connection to MQTT broker or ESP32"
	fi
else cut_scale=`echo $read_scale | awk -F ";" '{print $1";"$2";"substr($3,1,8)}'`
	if grep -q $cut_scale $path/backup.csv ; then
		time_tag=`grep -m 1 $cut_scale $path/backup.csv | awk -F ";" '{print $3}'`
		time_dif=$(( $unixtime_scale - $time_tag ))
		absolute_dif=`echo ${time_dif#-}`
		if (( $absolute_dif < 30 )) ; then
			echo "* $time_dif s time difference, same or similar data already exists in backup.csv file"
		else unixtime_os=`date +%s`
			time_shift=$(( $unixtime_os - $unixtime_scale ))
			absolute_shift=`echo ${time_shift#-}`
			if (( $absolute_shift > 1200 )) ; then
				echo "* $time_shift s time difference, synchronize date and time scale"
			else echo "* Saving import $unixtime_scale to backup.csv file"
				echo $read_scale >> $path/backup.csv
			fi
		fi
	else unixtime_os=`date +%s`
		time_shift=$(( $unixtime_os - $unixtime_scale ))
		absolute_shift=`echo ${time_shift#-}`
		if (( $absolute_shift > 1200 )) ; then
			echo "* $time_shift s time difference, synchronize date and time scale"
		else echo "* Saving import $unixtime_scale to backup.csv file"
			echo $read_scale >> $path/backup.csv
		fi
	fi
fi

# Calculating data and upload to Garmin Connect, logging, handling errors, backup file
if grep -q "failed\|to_import" $path/backup.csv ; then
	python3 -B $path/export_garmin.py > $path/temp.log 2>&1
	import_no=`awk -F ": " '/Import number:/{print $2}' $path/temp.log`
	echo "* Calculating data from import $import_no, upload to Garmin Connect"
	if grep -q "Error\|panic\|denied\|There\|Exec" $path/temp.log ; then
		echo "* Upload to Garmin Connect has failed, check temp.log for error details"
		sed -i "s/$import_no;to_import/$import_no;failed/" $path/backup.csv
	else echo "* Data upload to Garmin Connect is complete"
		echo "* Saving calculated data from import $import_no to backup.csv file"
		calc_data=`awk -F ": " '/Calculated data:/{print $2}' $path/temp.log`
		sed -i "s/$import_no;failed/$import_no;uploaded;$calc_data/; s/$import_no;to_import/$import_no;uploaded;$calc_data/" $path/backup.csv
	fi
else echo "* There is no new data to upload to Garmin Connect"
fi