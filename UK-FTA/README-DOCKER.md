# RUNNING IN DOCKER/PODMAN

```bash
git clone git@github.com:bmrussell/uk-fta.git
cd uk-fta//UK-FTA
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## BUILD
```bash
docker build -t itvx --label keep=true .
```

## RUN
```bash
docker run --rm --volume /home/$USER/Downloads:/save -e UKFTA_PUSHOVER_TOKEN=$UKFTA_PUSHOVER_TOKEN -e UKFTA_PUSHOVER_KEY=$UKFTA_PUSHOVER_KEY itvx --path /save --show $url --episode 1
docker run --rm --volume /home/$USER/Downloads:/save -e UKFTA_PUSHOVER_TOKEN=$UKFTA_PUSHOVER_TOKEN -e UKFTA_PUSHOVER_KEY=$UKFTA_PUSHOVER_KEY itvx --path /save --show $url --season 2,4
docker run --rm --volume /home/$USER/Downloads:/save -e UKFTA_PUSHOVER_TOKEN=$UKFTA_PUSHOVER_TOKEN -e UKFTA_PUSHOVER_KEY=$UKFTA_PUSHOVER_KEY itvx --path /save --show $url --episode 1,12 --whatif
docker run --rm --volume /home/$USER/Downloads:/save -e UKFTA_PUSHOVER_TOKEN=$UKFTA_PUSHOVER_TOKEN -e UKFTA_PUSHOVER_KEY=$UKFTA_PUSHOVER_KEY itvx --path /save --show $url --newest
```