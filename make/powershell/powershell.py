import os, sys
from base64 import b64encode
from jinja2 import Template

# necessary to make it possible to execute this file from this directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from model import *

# Notes:
# Use powershell.exe argument '-noexit' for testing


@PluginDecorator
def makePowershellDownloadAndExecuteBinary(url: str, path: str):
    templateFile = 'download_exec_file.ps1'
    return AceStr('')


@PluginDecorator
def makePowershellDownloadAndExecuteMemPs1(url: str) -> str:
    templateFile = 'download_exec_ps_enc_mem.ps1'
    with open('make/powershell/' + templateFile) as f:
        template = Template(f.read())
    renderedHtml = template.render(
        url=url
    )
    renderedHtml = renderedHtml.replace('\r', '')
    renderedHtml = renderedHtml.replace('\n', '')
    return AceStr(renderedHtml)


@PluginDecorator
def makePowershellMessageBox() -> str: 
    templateFile = 'messagebox.ps1'
    with open('make/powershell/' + templateFile) as f:
        template = Template(f.read())
    renderedHtml = template.render()
    renderedHtml = renderedHtml.replace('\r', '')
    renderedHtml = renderedHtml.replace('\n', '')
    return AceStr(renderedHtml)


@PluginDecorator
def makePowershellCommand(input: str) -> str:
    """For use with 'PowerShell.exe -Command {}'"""
    ret = "{}".format(input)
    return AceStr(ret)


@PluginDecorator
def makePowershellEncodedCommand(input: str) -> str:
    """For use with 'PowerShell.exe -EncodedCommand {}'"""
    text = "{}".format(input)
    # https://stackoverflow.com/questions/71642299/how-to-use-python-to-represent-the-powershell-tobase64string-function
    text = bytearray(text, 'utf-16-le')
    b64 = b64encode(text).decode() # bytearray to str
    return AceStr(b64)
