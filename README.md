# Train Delay Estimation
This project is first of its kind, an attempt made to learn the delay trends of
Indian trains at their in-line stations. See [doc](
https://github.com/R-Gaurav/train-delay-estimation/tree/master/doc) dir for overview
presentation; papers (ITSC version accepted at [IEEE ITSC 2018](
http://www.ieee-itsc2018.org) and long version of [Arxiv](
https://arxiv.org/abs/1806.02825) and a [tutorial](
https://github.com/R-Gaurav/train-delay-estimation/blob/master/doc/Tutorial.md)
on using the code/ model/ data. This poject is licensed under GNU GENERAL PUBLIC
LICENSE Version 3.

## Team
Ramashish Gaurav (2016 - ),
Himadri Mishra (2018 - ),
Biplav Srivastava, *main contact*.
For data or any other queries, email: my.better.rail@gmail.com

## Description
India runs the fourth largest railway transport network size carrying
over 8 billion passengers per year. However, the travel experience of
passengers is frequently marked by delays, i.e., late arrival of trains at
stations, causing inconvenience. In a first, we study the systemic delays
in train arrivals using norder Markov frameworks and experiment with two
regression based models. Using train running-status data collected for two
years, we report on an efficient algorithm for estimating delays at
railway stations with near accurate results. This work can help
railways to manage their resources, while also helping passengers
and businesses served by them to efficiently plan their activities.

### List of trains covered so far
['12307', '12331', '12801', '12802', '12815', '12816', '12875', '12876', '13010', '13050', '13119', '13131', '13133', '13151', '13238', '13483', '14055', '18612', '22911', '12178', '12318', '12327', '12354', '12361', '12362', '12372', '12395', '12569', '12818', '12942', '14003', '15632', '15635', '15636', '22811', '22812', '22824', '12305', '12326', '12424', '12444', '12578', '12937', '22409', '09012', '09305', '12149', '12282', '12333', '12335', '12382', '13239', '01660', '02050', '02265', '02397', '03209', '03210', '03291', '03563', '03564', '04039', '04040', '04401', '04405', '04406', '04821', '05066', '06032', '12141', '12150', '12175', '12295', '12296', '12301', '12302', '12304', '12308', '12309', '12312', '12313', '12317', '12319', '12320', '12322', '12325', '12328', '12332', '12334', '12356', '12369', '12381', '12392', '12397', '12398', '12401', '12423', '12439', '12454', '12495', '12496', '12506', '12741', '12817', '12826', '12947', '12948', '12987', '12988', '13005', '13006', '13008', '13009', '13049', '13202', '13240', '13255', '13307', '13308', '13414', '15022', '15483', '15645', '15668', '18103', '18104', '18311', '18609', '18631', '19313', '22308', '22405', '22406', '22488', '25631']

## Tutorial to use our code
Please visit the [tutorial](
https://github.com/R-Gaurav/train-delay-estimation/blob/master/doc/Tutorial.md)
to find out the steps for using our code and setting up the experiment locally on
your system. In the tutorial you will also find how to deploy a train delay
estimation service locally on your system. On executing a REST API call, e.g.
*curl http://127.0.0.1:5000/12333* (more to be found in tutorial) you will get
delay estimates (in minutes) at in-line station of Train 12333's journey on
current date in a JSON format (example below).

`
{
  "Result": {
    ..., "ALY": 322.184, "DLN": 81.23, "KIUL": 29.395, ...
  },
  "Error": null
}
`

## Future work (how you can contribute to it...)
There are many avenues for extending current work. Please feel free to
contact us for any help.

- [Scaling] Expand the existing database of 135 trains (819 stations) to India wide.
- [Improving] Improve the accuracy of existing prediction framework. Examples are
time series prediction, neural networks.
- [Improving] The current prediction framework is off-line in approach, i.e. it learns by
batch processing the accumulated data. A realistic prediction framework will be
on-line, i.e. so that it can  keep learning with delays and railway network dynamics
throughout its lifetime.

In case you decide to contribute, please go through the [PEP8](
https://www.python.org/dev/peps/pep-0008/) coding conventions. The coding standards
in this repository is very much based on that.
--------

Suggestions and contributions are welcome.
