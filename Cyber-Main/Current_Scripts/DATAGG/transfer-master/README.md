# transfer
transfer is a simple bash script that uploads file or directory to [transfer.sh] and generates a download link. Directory will be compressed into an archive (tar.gz) and uploaded. Maximum filesize limit is 5 GB. File will expire in 14 days.


### Dependencies :
- curl - [curl] is a command line tool and library for transferring data with URL syntax. curl is available in repositories of almost every Linux distribution so you can install curl easily via your package manager.
- Tar - [Tar] Tar is a program for packaging a set of files as a single archive in tar format. It is useful for performing system backups and exchanging sets of files with others. Tar should already be installed in most Linux distributions.


### Installation :
Simply download [transfer-master.zip], extract it, and copy the file 'transfer' to '/usr/local/bin/' directory,
 ```sh
$ sudo cp transfer /usr/local/bin/
 ```
Next make it executable,
```sh
$ sudo chmod a+x /usr/local/bin/transfer
```


### Usage :
Run 'transfer' from terminal, give full path to the file or directory to upload and your file or directory will be uploaded to [transfer.sh] and a download link to that file or directory will be generated.


### Credits :
transfer is inspired from a bash alias by Remco Verhoef.


### License :
[![Public Domain Mark](http://i.creativecommons.org/p/mark/1.0/88x31.png)](http://creativecommons.org/publicdomain/mark/1.0/)  
This work (<span property="dct:title">transfer</span>, by [<span property="dct:title">hakerdefo</span>](https://github.com/hakerdefo/transfer)), identified by [<span property="dct:title">hakerdefo</span>](https://hakerdefo.blogspot.com), is free of known copyright restrictions.

[transfer.sh]:https://transfer.sh
[curl]:http://curl.haxx.se
[Tar]:https://www.gnu.org/software/tar/
[transfer-master.zip]:https://github.com/hakerdefo/transfer/archive/master.zip
