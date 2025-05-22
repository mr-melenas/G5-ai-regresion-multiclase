FROM python:3.13

# In order to avoid issues with other operating systems
RUN mkdir -p /tmp/cache/fontconfig && chmod 777 /tmp/cache/fontconfig

WORKDIR /G5-ai-regresion-multiclase

COPY requirements.txt .

# Install python
RUN python -m pip install --upgrade pip
# Copy and install the requirements
# --use-pep517 is needed to install some packages that are not compatible with the new version of pip
# --no-cache-dir is used to avoid caching the packages, which can save space
# --timeout 60 is used to avoid timeout issues when installing packages
# -v is used to show the verbose output of the installation process
RUN pip install -r requirements.txt --use-pep517 --no-cache-dir --timeout 60 -v
#RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 8000 
#EXPOSE 7860 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]