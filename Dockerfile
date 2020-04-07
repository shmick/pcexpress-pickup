FROM python:3.8-alpine

WORKDIR /pcexpress

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY check.py check_all_by_postal_code.py run.sh locations.json ./

ENTRYPOINT ["./run.sh"]

# CMD [ "$@"]
