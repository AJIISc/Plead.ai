docker run -d --name opensearch \
    -p 9200:9200 -p 9600:9600 \
    -e "discovery.type=single-node" \
    -e "plugins.security.disabled=false" \  # Enable security
    -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=YourStrongPassword" \  # Set your strong password here
    opensearchproject/opensearch:latest
