# ABM-Tasks
---

##  Architecture Design Overview

The system is engineered for high availability and horizontal scalability, ensuring that task processing remains fluid even under heavy load.



### Core Components:
* **Load Balancer:** Serves as the primary entry point, distributing traffic from users/applications to API Microservices to prevent bottlenecks.
* **RabbitMQ Message Queue:** Decouples the API from heavy processing. The API places tasks into an ordered queue, allowing the system to handle spikes in traffic without crashing.
* **Worker Node Architecture:** Designed for **Horizontal Scaling**. This allows the system to dynamically add "Worker Nodes" to handle task distribution based on demand.
* **Central SQL Database:** A unified persistence layer that ensures data safety and integrity for all processed outputs.
* **Integrated Monitoring Stack:** Real-time tracking of microservices across three key areas:
    * **System Health:** Overall uptime and status.
    * **System Current Load:** Real-time resource utilization.
    * **System Error Logging:** Centralized fault tracking and diagnostics.
* **Failover & Recovery:** Includes **Automatic Failover** for worker nodes and database instances, paired with **Data Recovery** to ensure maximum uptime.

---

##  Automation Suite (Tasks 1-3)

The provided Python scripts utilize **Playwright (Patchright)** and **Selenium** to navigate complex web security layers.

### 1. Cloudflare Turnstile Automated Solver (`Task1.py`)
* Uses asynchronous Playwright to launch a non-headless Chrome instance.
* Bypasses `AutomationControlled` detection.
* Monitors the DOM for the `cf-turnstile-response` token and calculates accuracy over 10 trials.
* For the Headless : True It Cannot Work As a Cloudflare can detect it easy so we can work with Headless false and minimize the browser screen. 

### 2. Manual Token Injection & Script Blocking (`Task2.py`)
* **Neutralization:** Redefines the `window.turnstile` object to block the challenge from loading.
* **Network Filtering:** Blocks all requests to `challenges.cloudflare.com`.
* **Injection:** Manually injects a valid token into the hidden input field to bypass server-side verification.

### 3. Visual CAPTCHA Data Extraction (`Task3.py`)
* Designed for grid-based CAPTCHAs (e.g., BLS Spain).
* **Color Analysis:** Filters "noise" text by identifying RGB color thresholds.
* **Z-Index Mapping:** Uses custom JavaScript to determine the actual visibility and stacking order of images.
* **JSON Export:** Outputs `visible_images_only.json` and `visible_texts.json` for further processing or ML training.

---


### Prerequisites
* Python 3.10+
* Google Chrome Browser
* Required Libraries:
    ```bash
    pip install patchright selenium
    ```



