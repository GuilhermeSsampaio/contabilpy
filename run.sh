source ./venv/Scripts/activate
pip install streamlit
PORT=${PORT:-80}  # Define 8501 como porta padrão, caso $PORT não esteja definida
streamlit run --server.port $PORT app.py