python -m black . 
setup-cfg-fmt setup.cfg
python -m flake8 .
python -m pytest . -c pytest.ini