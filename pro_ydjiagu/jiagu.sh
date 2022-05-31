#!/bin/sh
export APK_DIR="./apk"
# shellcheck disable=SC2045
for temp in $(ls $APK_DIR)
do 
	export package="$APK_DIR/$temp"
	export apkfile=
	export jksfile=
	# shellcheck disable=SC2045
	for file in $(ls $package)
	do
		# 赋值
		if [ "${file##*.}" = "apk" ]; then
			apkfile="$file"
		elif [ "${file##*.}" = "jks" ]; then
			jksfile="$file"
		fi
		if [ -n "$apkfile" ] && [ -n "$jksfile" ] ; then
			# 替换config.ini
			gsed -i "s|keystore=.*|keystore=$package/$jksfile|g" config.ini
			# 执行加固
			echo "java -jar NHPProtect.jar -yunconfig -fullapk -apksign -input $package/$apkfile -output $package/output/${apkfile%.*}_protected_sign.apk"
			echo "java -jar NHPProtect.jar -yunconfig -fullapk -apksign -input $package/$apkfile -output $package/output/${apkfile%.*}_protected_sign.apk" |bash
		fi
    done
done