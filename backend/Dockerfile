FROM bird:latest
MAINTAINER Robot

WORKDIR /code
#将当前文件夹下面的requirements.txt复制到容器中
COPY . .

EXPOSE 5500

CMD gunicorn -c gunicorn.conf run:app
