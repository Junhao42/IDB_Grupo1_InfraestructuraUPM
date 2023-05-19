FROM bigdatainf/hadoop-base:3.3.5

MAINTAINER Carlos Badenes <carlos.badenes@upm.es>

# based on the previous work of
MAINTAINER Ivan Ermilov <ivan.s.ermilov@gmail.com>

HEALTHCHECK CMD curl -f http://localhost:8088/ || exit 1

ADD run.sh /run.sh
RUN chmod a+x /run.sh

EXPOSE 8088

CMD ["/run.sh"]
