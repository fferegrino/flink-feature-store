FROM jupyter/minimal-notebook:latest

# Switch to root to install additional dependencies
USER root

# Install additional Python packages if needed
RUN pip install mysql-connector-python pandas

# Switch back to notebook user
USER ${NB_UID}

# Disable token authentication
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]
