FROM solr:8-slim

USER root

# Copy custom web.xml with CORS settings
COPY web.xml /opt/solr/server/solr-webapp/webapp/WEB-INF/web.xml

USER solr

EXPOSE 8983