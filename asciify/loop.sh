while true; do
	printf "%100s" " " | tr " " "\n";
	python -m asciify.display;
	sleep 1;

done
