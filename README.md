# Useful commands#
```shell 
rasa data validate
rasa train
```
Then start the action server:
```shell
rasa run actions
```
or
```shell script
python -m rasa_sdk --actions actions
```
Run the dialog in test mode or interactive (learning mode):
```shell
rasa shell  --endpoints endpoints.yml
rasa interactive  --endpoints endpoints.yml
```

# Challenges:
* Slot type list can collect several commodities and several quantities, but it doesn't know which one is which if one is missing
** https://blog.rasa.com/introducing-entity-roles-and-groups/
** https://github.com/BeWe11/rasa_composite_entities
* NLU model for units (e.g. pounds)
* 

