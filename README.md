# Campus Buzz Mini Project

This is a campus event submission and processing system based on Flask and Docker Compose, consisting of three services:

- `presentation-service`: Provides the event submission form and result display page.
- `workflow-service`: Handles submissions, writes data to the data service, and triggers event processing functions.
- `data-service`: Manages the storage, retrieval, and updating of event records.



## Project Structure

```text
.
├── data-service/
├── workflow-service/
├── presentation-service/
├── data/
├── docker-compose.yml
└── README.md
```



## How to Run

Make sure Docker Desktop is installed on your machine, then run the following command in the project root directory:

```
docker compose up --build
```



After starting, access the application at:

```
http://localhost
```



## Service Ports

- `presentation-service`: `80` on host, `5000` inside the container
- `workflow-service`: `5001`
- `data-service`: `5002`



## Submission to GitHub

When uploading to GitHub, only include the source code, configuration files, and documentation. Do **not** include virtual environments, IDE configurations, dependency directories, or zip files.
