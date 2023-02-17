# Plugin Interface

Location: `make/<plugin>/<plugin>.py`

## Imports

* Make sure you import the `../../` parent path for imports
```python
# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import AceFile, PluginDecorator
```

## Main function

* Make sure you use the `@PluginDecorator` decorator so the data gets logged. 
* Always return `bytes`

```python
@PluginDecorator
def make<plugin>(args...) -> bytes:
```


## Helper function 

* Each plugin should be usable form the commandline. Add arguments accordingly

```python
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('...', help='...')
    args = parser.parse_args()

    data = make<plugin>(args...)

    file = open(args.name, 'wb')
    file.write(data)
    file.close()


if __name__ == "__main__":
    main()