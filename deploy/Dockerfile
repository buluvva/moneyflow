FROM python:3.9
COPY ./ opt/app
WORKDIR opt/app
RUN pip3 install -r deploy/requirements.txt
CMD python bot.py