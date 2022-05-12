### Generating supply chain tree for domain

#### Script generating json file as a solution in format:
```
<sellers tree>
{
    "buyer": <company domain>,
    "direct sellers": [<company domain>],
    "indirect sellers": [<sellers tree>]
}
```
file will be added to folder /out

#### Execution
```
syntax:
    $ python3 main.py <domain_name> <max_depth>

examples:
    $ python3 main.py openx.com 1
    $ python3 main.py ascendeum.com 2
```

Warning!
```
main.py openx.com 2
```
will be running about 5-10 minutes (14.57 MB)
