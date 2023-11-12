# Tecalor Heatpump Modbus Interface

This package reads Heatpump data from Tecalor Internet Service Gateway (ISG) and writes it into an influx database. A grafana dashboard is used to visualize the data.

Code is tested with a Tecalor ACS Heatpump, should work for other Tecalor / Stiebel Eltron models as well.

Modbus  Specification for Tecalor / Stiebel Eltron: https://www.stiebel-eltron.de/content/dam/ste/cdbassets/historic/bedienungs-_u_installationsanleitungen/ISG_Modbus__b89c1c53-6d34-4243-a630-b42cf0633361.pdf

The script runs every 15 mins via a cron job.
```
*/30 * * * * /usr/bin/python3 /home/pi/tecalor_wp/isg.py /home/pi/tecalor_wp/config.yaml >> /home/pi/tecalor_wp/cron.log
```

## Screenshot
![Dashboard](docs/screenshot_grafana.jpg?raw=true "Dashboard")

# License

The MIT License (MIT)

Copyright (c) 2018-2020 Michael Schuster development@unltd-networx.de

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
