FROM python:3.12.4
COPY requirement.txt /src/requirements.txt
WORKDIR /src
RUN pip install --no-cache-dir -r requirements.txt
COPY user_data_validator /src/
COPY csv_valid_app /src/
COPY dockerfile /src/
COPY manage.py /src/
COPY README.md /src/
EXPOSE 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]