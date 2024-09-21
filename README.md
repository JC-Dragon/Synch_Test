Script to synch a folder with a Replica/Backup

Using python create a method to synchronize, only from source to destiny, a directory with a replica
Every file or directory created, removed or modified in source will be reproduced in replica folder and these actions will be logged in a text file as well as printed in the cmd.
These synch actions will be repeated periodically as instructed by the user.
In case synch happens while changing a file the method will wait 60s more to try again until you're done with the changes.

CMD command to run is:
   -py synch_script.py SourcePath DestinationPath Period

Source Path example: C:\Users\Lenovo\Documents\TESTES\PastaA
Destination Path example: C:\Users\Lenovo\Documents\TESTES\Replica
Period(minutes) example: 1
