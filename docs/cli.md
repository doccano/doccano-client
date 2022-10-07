# CLI

By using the CLI, you can pre-annotate texts with the spaCy model. Currently, `login` and `predict` commands are supported. `login` is the command to login to doccano and must be executed first. `predict` is the command to annotate data with the model. The usage is as follows:

```bash
# On GPU machine
$ python -m spacy train config.cfg \
    --output outputs \
    --paths.train /path/to/train.spacy \
    --paths.dev /path/to/dev.spacy \
    --gpu-id 0

# On another machine
$ docli login \
    --host http://127.0.0.1:8000 \
    --username admin \
    --password password
$ docli predict <task> \
    --project <project_id> \
    --model <en_core_web_sm> \
    --mapping [mapping.json] \
    --framework [spacy]
```

Currently, only `ner` is supported as a task and `spacy` as a framework. Also, the `framework` and `mapping` options can be omitted.

```bash
$ docli predict ner \
    --project <project_id> \
    --model <en_core_web_sm>
```

Mapping can be a path to a JSON file. This JSON file consists of keys and values as shown below. The key is the label names output by the model, and the value is the label names you defined in doccano. In this way, the label names output by the model is converted to the defined label names so that they can be labeled.

```bash
{
   "LOCATION":"LOC",
   "ORGANIZATION":"ORG",
   "GPE":"LOC"
}
```

Note that if the label names output by the model are not defined in doccano and are not converted using mapping, the labels will be discarded.

This feature is integrated with [spacy-partial-tagger](https://github.com/doccano/spacy-partial-tagger), which allows you to train models with just a dictionary and some text. Please see [the repository](https://github.com/doccano/spacy-partial-tagger) for more details.

## Installation

```bash
pip install doccano-client[spacy]
```
