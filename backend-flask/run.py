#!/usr/bin/env python
from apps import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5500', debug=True)