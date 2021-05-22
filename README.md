# Json-Translator
this project aims to translate the json content into different langs using google translation

## Requirement library
-flatten_json (https://github.com/amirziai/flatten)
-deep_translator (https://github.com/nidhaloff/deep-translator)
install them using 
```
  pip install flatten_json
  pip install -U deep_translator
```

after installation, please comment out line 47-48 in deep-translator/parent.py
```
# if not payload or not isinstance(payload, str) or not payload.strip() or payload.isdigit():
    # raise NotValidPayload(payload)
```
### Why to comment out line 47-48?
bulk translate method in deep translator has 2 second delay for each phrase to prevent getting banned from overusing translation api

this project first flatten json content into a list, then all elements combine into a line string seperated by '\n' and therefore we can put multiple phrase into one api call.

However the parent.py will detect whether phrase exist illegal character such as '\n', so we nned to remove it


## How to use
python json-translate.py input-filename output-filename lang-code
