# Heimdall - Serverside

This repository contains code for the server-side applications of Heimdall SSH Logging system.

---
## Heimdall

Heimdall is a GitHub based server login manager. It uses GitHub to track the SSH Keys and manage the access of the servers.

For more information, please head to [Heimdall - Master](https://github.com/aitalshashank2/Heimdall-Master)

---

## Setup Instructions

- Clone this repository.

- Go into the folder.
	```bash
	cd Heimdall-serverside
	```

- Copy `.env-stencil` to `.env`
	```bash
	cp .env-stencil .env
	```

- Change the variables in `.env` according to the system configuration
	```
	AUTH= # path to the auth logs of your system (/var/log/auth.log in ubuntu)
	AUTHORIZED_KEYS= # path to the file containing authorized keys of the ssh server (~/.ssh/authorized_keys in ubuntu)
	```

- Go into the `configuration` directory in the `code` directory
	```bash
	cd code/configuration
	```

- Copy `config-stencil.yml` to `config.yml`
	```bash
	cp config-stencil.yml config.yml
	```

- Change the `config.yml` to the configurations of your system and **Heimdall - Master**
	```yml
	DESTINATION_FILE: /mounts/authorized_keys # DO NOT CHANGE
	AUTH_LOG: /mounts/auth.log # DO NOT CHANGE

	MASTER:
		URL: # URL of Heimdall - Master
		ENDPOINT_LOG: /bipolar/log # DO NOT CHANGE
		SECRET: # Secret that will be used by master to validate log requests
	```

- Build docker images
	```bash
	cd ../..
	docker-compose build
	```

- Use the following command to start the server
	```bash
	docker-compose up -d
	```

- Use the following command to stop the server
	```bash
	docker-compose down
	```
