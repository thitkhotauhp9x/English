for ((i = 0 ; i < 3; i++)); do
  curl -X 'GET' \
  'http://127.0.0.1:8000/search' \
  -H 'accept: application/json' &
done
wait
