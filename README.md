$Object = 'C:\Users\mt4as\Desktop\codedump\docker'
$ACL = get-acl $Object
# pay attention to first property, the username
$Permission = "username", "FullControl", "ContainerInherit,ObjectInherit", "None" , "Allow"
$AccessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $Permission
$acl.SetAccessRule($AccessRule)
$ACL | Set-Acl $Object