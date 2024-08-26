FROM adoptopenjdk:11-jre-hotspot

RUN useradd -m iceberg

COPY rest-catalog/iceberg-rest-catalog-all.jar /usr/lib/iceberg-rest/iceberg-rest-catalog-all.jar
COPY rest-catalog/start.sh /usr/lib/iceberg-rest/start.sh
COPY rest-catalog/stop.sh /usr/lib/iceberg-rest/stop.sh

# Convertir les sauts de ligne en format Unix (LF) avec sed
RUN sed -i 's/\r$//' /usr/lib/iceberg-rest/start.sh && \
    sed -i 's/\r$//' /usr/lib/iceberg-rest/stop.sh

RUN chown -R iceberg:iceberg /usr/lib/iceberg-rest  # Changer le propriétaire du répertoire

USER iceberg
WORKDIR /usr/lib/iceberg-rest
CMD ["sh", "-c", "sh start.sh && tail -f log.log"]
