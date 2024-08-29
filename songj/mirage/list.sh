for FILE in `ls *.mp3`
do
	TITLE=`exiftool $FILE|grep "Title"|cut -d ":" -f 2`
	ARTIST=`exiftool $FILE|grep "Artist"|cut -d ":" -f 2`
	echo $FILE ${ARTIST:1}-${TITLE:1}
done
