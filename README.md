# PrologOntParse  

Набор сценариев для автоматической популяции баз знаний и автоматического извлечения отношений на шаблонах.

## Исходные файлы
`txt/` -- Исходные файлы с текстами лекций, необработанным (`lecion.txt`) и формализованным (`lecion_formal.txt`)  
`kb/` -- Базы знаний в формате языка Prolog: набора правил (`ontology.pr`), базы знаний, созданной вручную (`kb_hand.pr`) и автоматически (`kb_auto.pr`)  
`templates/` -- Файлы с шаблонами для автоматического извлечения терминов и отношений: для извлечения только терминов (`term.txt`), терминов и отношений (`templates.txt`), шаблоны для формализованного текста (`formal.txt`)  
`requirements.txt` -- Зависимости для среды Python, `pip install -r requirements.txt`
`morph.py` -- Модуль морфологического разбора и склонения слов/словосочетаний для русского языка (на основе `pymorphy2`)  

## Популяция баз знаний
`ont_to_text.py` -- Генерирует формализованный естественный текст по файлу .pr с онтологией: `python ont_to_text.py input_file output_file`  
`ont_parse.py` -- Код для генерации онтологии по тексту адаптированной лекции: `python ont_parse.py input_file output_file`  
`compile_ont.py` -- Собирает полную онтологию из файла с отношениями (`ontology.pr`) и файла с базой знаний: `python compile_ont.py ontology.pr kb.pr output.pr`.
Полную онтологию можно закинуть в интерпретатор языка пролог (например, https://swish.swi-prolog.org/) и позадавать вопросы, пользуясь синтаксисом языка. 
Парсер Онтологий работает на очень узком количестве шаблонов, и посему нормально обработать может только формализованные тексты.

## Извлечение терминов и отношений
`term_extract.py` -- простенькая извлекалочка на регулярных выражениях и захардкоженных ключевых словах
`gram_parse.py` -- извлекалочка посложнее. Кушает файлец с шаблонами, текст лекции, и опциональный файл для вывода в формате .tsv: `python gram_parse.py templates_file input_file [output_file]`

### Формат шаблонов:
**$TERM**, **$HYPONYM** и иже с ними -- нетерминальные символы (их значение пытается определить программулина), определение в терминах re: `'\$\w+'`   
**$*** -- нетерминальный символ, означающий любую последовательность, которая нас не интересует.  
Все остальные символы -- терминалы, совпадение с коими ищется в тексте.
Каждый терминал, обнаруженный в тексте, программулина пытается обработать и извлечь из него именную группу (совокупность согласованных прилагательных и существительных вместе с паравозом относительных существительных). Не рекомендуется употреблять **$*** непосредственно перед или после нетерминала, так как это порождает неоднозначность.
Пример: шаблон `$TERM - это $*` ищет все фразы, содержащие ключевую фразу " - это ", и извлекает левую часть этих фраз в качестве термина.


## Farenda:
* Пока Анализатор онтологий и Извлекатор терминов не сильно связаны -- надо переобработать выход Извлекатора, чтобы он делал правильные онтологические выводы.
* В теории, для этой задачи можно приспособить нормальные грамматики, но по факту обычные формальные грамматики слишком 'формальны' для нас -- нам желательно иметь более покладистые методы.
* Также, весь этот репозиторий, скорее всего, -- один большой велосипед, но чего не сделаешь ради того, чтобы разобраться в проблеме.
* Возможны различные варианты разбора, во-первых могут сработать несколько правил за раз -- надо решить, какое использовать (сейчас используется первое подходящее по списку). Во вторых наложение масок на предложение может быть совершенно разными способами, что пока не учитывается
* Была добавлена возможность фильтрации по поз-тегам, но убрана возможность автоматической нормализации, что и хорошо и плохо.

 

