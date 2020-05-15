# The solution
This folder contains all the files related to the exercise defined by **hiring_exercise.pdf**.

## Getting started
These instructions will help you to run the tools and modify settings if required.

### Prerequisites
To run the Vagrantfile, following software needs to be installed on the Vagrant host:
- Vagrant (2.x)
- python3 (3.6.x)
- ansible 2.9.x (pip3 install ansible)

VM Host requirements:
- internet connection
### Running
To start the environment, just execute the below command in the folder where file "Vagrantfile" is located:
```
vagrant up
```
## Exercise solutions
Following sections describe the solutions and related assumptions which have been done.
### Exercise 1
#### Programming
To run the Python script, export variables and execute using python3.
```
$ export |grep -E "WEATHER|CITY_NAME"
declare -x CITY_NAME="Bratislava"
declare -x OPENWEATHER_API_KEY="xxx"
$ python getweather.py
source=openweathermap, city="Bratislava", description="overcast clouds", temp=10.65, humidity=62
```
#### Ansible
Role **martin.docker** was created based on specifications and installs docker on target host, while configuring docker logging to syslog. The playbook is automatically executed from Vagrantfile during Vagrant provisioning by **playbook.yml**. A separate **site.yml** playbook has been added to the role directory to complete the requirement, so the role can be also executed manually. Please note, to execute the role, ansible 2.9.x is needed, but Ubuntu 16.04 packages provide ansible 2.0.0. Ansible 2.9 can be easily installed via pip3.

To apply the role manually, use:
```
$ pip3 install ansible
$ /usr/local/bin/ansible-playbook -i "localhost," -c local site.yml
```
Ansible role is based on ansible-galaxy role geerlingguy.docker.
#### Docker
Dockerfile was created using image python:3 and using pyowm. To test and execute use the following command in the folder where **Dockerfile** is located:
```
$ docker build --tag weather:dev .
$ docker run --rm -e OPENWEATHER_API_KEY="xxx" -e CITY_NAME="Bratislava" -ti weather:dev
```
The solution utilizes the logger command to write the getweather.py output to syslog. Valid API key must be provided.
### Exercise 2
#### Programming
Program **scanner.py** was created in Python and follows the requirements, using the Python **nmap** library. To execute use the following syntax:
```
$ pip3 install nmap
...
$ ./scanner.py 192.168.1.1
*Target - 192.168.1.1: Full scan results:*
Host: 192.168.1.1      Ports: 22/open/tcp////
Host: 192.168.1.1      Ports: 53/open/tcp////
Host: 192.168.1.1      Ports: 10000/open/tcp////
```
Scanner uses file **scanner_results.json** in working directory to store the results between runs in JSON format. Subsequent scans with no port changes on target ports:
```
$ ./scanner.py 192.168.1.1
*Target - 192.168.1.1: No new results in the last scan.*
```
After subsequent scans with changes on target host, full results are displayed:
```
$ ./scanner.py 192.168.1.1
*Target - 192.168.1.1: Full scan results:*
Host: 192.168.1.1      Ports: 22/open/tcp////
Host: 192.168.1.1      Ports: 23/open/tcp////
Host: 192.168.1.1      Ports: 53/open/tcp////
Host: 192.168.1.1      Ports: 10000/open/tcp////
```
Please note, as it was not specified, the assumption was made, that the requirement "change on target host" means any change in port state (e.g. closed->open and also open->closed).
NOTE: I believe the code is ugly. Everytime I write Python code and lookup alternatives to the same solution on the Internet, I am surprised on how nice the code can actually be...
### Exercise 3
#### Syslog configuration
Syslog configuration is configured automatically by the **martin.rsyslog** Ansible role. This role is applied during Vagrant provisining phase by **playbook.yml** (which includes also the **martin.docker** role).
#### Ansible
Role **martin.rsyslog** was created based on specifications and configures rsyslog based on variables defined below.
Settings can be modified via role level variables in **playbook.yml**:
```
playbook.yml:
...
  - role: martin.rsyslog
    vars:
      remote_syslog_send_default_logs: true
      remote_syslog_send_custom_logs: true
      remote_syslog_custom_files:
      - '/var/test1.log'
      - '/var/test2.log'
      remote_syslog_target: "192.168.1.17"
      remote_syslog_port: "514"
      remote_syslog_protocol: "tcp"
...
```
Configurable role variables are explained below:
```
remote_syslog_send_default_logs: true|false
remote_syslog_send_custom_logs: true|false
```
Variables define if default logs and/or custom logs will be sent to remote syslog server. If both are set to false, no configuration changes will be made.
```
remote_syslog_custom_files: []
```
A list of full paths to custom log files needs to be defined for custom log sending to be configured. Files do not need to exist.
```
remote_syslog_target: "192.168.1.17"
remote_syslog_port: "514"
remote_syslog_protocol: "tcp"
```
Remote syslog server configuration.
Please note, an assumption was made, that redirecting '\*.\*' to remote server is equivalent to /var/log/\*.log, as in a default minimal Ubuntu installation that is true. However, in a more complex scenario, additional modifications need to be done to exclude /var/log/\*/\*.log files to fully follow the requirements specified for this exercise.

## Developed with
Software package versions used during development:
- Vagrant 2.2.7
- python3 3.6.9
- ansible 2.9.5

Completed during ~9 hours...

## Author
- Martin
