<h1 align="center">RAVEN</h1>

<p align="center">
  <em>command synthesis from intent</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-experimental-4B0082?style=flat"/>
  <img src="https://img.shields.io/badge/python-3.10+-3776AB?style=flat&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/license-MIT-3DA639?style=flat"/>
</p>

---

## > Overview

**Raven** is an experimental command synthesis engine that transforms natural language instructions into executable commands for Debian-based Linux systems.

The project combines:

* **Naive Bayes intent classification** for probabilistic interpretation
* **Regex-based pattern resolution** for command mapping
* Structured command generation focused on terminal workflows

Raven was built for:

* Command-line automation experiments
* NLP and intent classification studies
* Linux workflow research
* Controlled command execution environments

---

## > How It Works

The engine processes user input in multiple stages:

1. Natural language input is analyzed
2. Intent is classified using a Naive Bayes model
3. Regex patterns resolve command structures
4. A Linux command is generated and returned

Example:

```text
Input:
create a new directory called test

Output:
mkdir test
```

---

## > Installation

```bash
git clone https://github.com/0xf0xy/Raven
cd Raven
sudo pip install .
```

Verify installation:

```bash
raven -h
```

---

## > Requirements

* Python 3.10+
* Debian-based Linux distribution

---

## > Project Status

Raven is currently in an experimental stage and focused on research and workflow prototyping.  
Features and internal behavior may change over time.

---

## > Warning

This project is provided for **educational and research purposes only**.  
You are responsible for any commands executed through this software.

---

<p align="center">
  <a href="https://github.com/0xf0xy"><b>0xf0xy</b></a> • 
  <a href="./LICENSE"><b>MIT License</b></a>
</p>
