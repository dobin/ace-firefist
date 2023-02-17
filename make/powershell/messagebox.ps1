Add-Type -AssemblyName PresentationCore,PresentationFramework; 
$msgBody = 'This is a simple message with just the default OK button';
[System.Windows.MessageBox]::Show($msgBody);
Start-Sleep -Seconds 10;