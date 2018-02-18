# Goal
Get the tool working from end-to-end. Import a screenplay and get the underlying structure.

## Next Sprint
* Generate Times from location slugs
* Add details to scene (ext./int., time)
* Evaluate scene data from imports

## Backlog
* Import 100 screenplays from the public domain
* Catalog common slug usages
* Add custom manager for TextBlock to exclude empty string

### Importer
* Add support for importing screenplays from sfy.ru urls
* Add support for uploading text files
* Add support for uploading multiple file formats

### Parser
* Refactor RegexParser to use static methods
* Refactor ParseOperation to not be so complicated
* Review splitting ParseResult out of ParseOperation
* Split into a separate app
* Incorporate ML

### Interpreter
* Refactor InterpretOp into separate services
* Create non-reversed link between TextBlocks and Lines
* Split into a separate app
* Determine dialogue from action by following characters
