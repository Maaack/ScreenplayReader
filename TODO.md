# Goal
Get the tool working from end-to-end. Import a screenplay and get the underlying structure.

## Next Sprint
* Split Interpreter to separate app
* Split Parser into separate app
* Add general tags to use on text

## Backlog
* Evaluate including django-taggit
* Add previous scene and next scene links to scene serializer
* Evaluate scene data from imports
* Import 100 screenplays from the public domain
* Catalog common slug usages
* Add custom manager for TextBlock to exclude empty string

### Importer
* Add support for importing screenplays from sfy.ru urls
* Add support for uploading text files
* Add support for uploading multiple file formats

### Parser
* Refactor ParseOperation to not be so complicated
* Review splitting ParseResult out of ParseOperation
* Refactor RegexParser to use static methods (I guess?)
* Split into a separate app
* Incorporate ML

### Interpreter
* Refactor InterpretOp into separate services
* Create non-reversed link between TextBlocks and Lines
* Split into a separate app
* Determine dialogue from action by following characters
