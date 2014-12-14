for i in $(ls ../templates/*.html)
do
java -jar htmlcompressor-1.5.3.jar --compress-css --compress-js $i
done | gzip -c | wc -c
