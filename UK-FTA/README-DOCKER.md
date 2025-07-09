# RUNNING IN DOCKER/PODMAN


## BUILD
```bash
podman build -t itvx --label keep=true .
podman build -t itvx --build-arg APP_USER=$USER --build-arg APP_UID=$UID --label keep=true .
```

## RUN

```bash
podman run --rm --userns=keep-id --group-add keep-groups --volume /home/$USER/Downloads:/save -e UKFTA_PUSHOVER_TOKEN=$UKFTA_PUSHOVER_TOKEN -e UKFTA_PUSHOVER_KEY=$UKFTA_PUSHOVER_KEY itvx --path ~/save $@
```