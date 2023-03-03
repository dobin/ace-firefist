Add-Type -AssemblyName PresentationCore,PresentationFramework; 
$msgBody = 'PowerShell Script Message Box';
[System.Windows.MessageBox]::Show($msgBody);