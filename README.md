# Useful commands#
```shell 
rasa data validate
rasa train
```
Then start the action server:
```shell
rasa run actions
```

Run the dialog in test mode or interactive (learning mode):
```shell
rasa shell  --endpoints endpoints.yml
rasa interactive  --endpoints endpoints.yml
```


