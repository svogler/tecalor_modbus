# Tecalor Heatpump Modbus Interface

### Visualization of Tecalor / Stiebel ACS Heatpump data. I use it for tracking and parameter optimization. ServiceWelt data is not enough for me and is super-slow. Modbus provides all the data, so let's visualize it.

This package reads Heatpump data from Tecalor Internet Service Gateway (ISG) and writes it into an influx database. A grafana dashboard is used to visualize the data.

Code is tested with a Tecalor ACS Heatpump, should work for other Tecalor / Stiebel Eltron models as well.

Modbus  Specification for Tecalor / Stiebel Eltron: https://www.stiebel-eltron.de/toolbox/content/docs/anleitungen/installation/ISG_Modbus/321798-44755-9770_ISG%20Modbus_de_en_fr_it_nl_cs_sk_pl_hu.pdf

config.yaml stores influx db access data and ISG parameters for the modbux interface.

The script runs every 30 mins via a cron job.
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
