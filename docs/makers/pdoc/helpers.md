Module helpers
==============

Functions
---------

    
`base64encode(input: model.AceBytes) ‑> model.AceStr`
:   

    
`getRecipeInfo(file: str, routes: List[model.AceRoute])`
:   

    
`getRecipePyFiles()`
:   

    
`getTemplate(path: str) ‑> jinja2.environment.Template`
:   

    
`makeAceFile(name: str, data: bytes) ‑> model.AceFile`
:   

    
`readFileContent(filename) ‑> model.AceBytes`
:   

    
`readFileContentStr(filename) ‑> model.AceBytes`
:   

    
`renderTemplate(path, **kwargs)`
:   

    
`replacer(data: bytes, placeholder: bytes, exchange: bytes) ‑> bytes`
:   

    
`saveAceFile(file: model.AceFile)`
:   

    
`scanAv(aceFile: model.AceFile) ‑> bool`
:   

    
`yamlHelp(file)`
: