#Operating System Support
It is designed for a GNU/Linux based system, but it may work on others.

#Description
This is a cache for file decompression. Useful for facilitating efficient access to compressed static content. My original use case was increasing the efficiency of on-the-fly game decompression, similar to how some emulators handle ROMs in zip files. But this could be just as easily applied to archived log or sqlite database access. 

#Technical Description
It takes an archive file from the command line and returns a path to the decompressed content:
>cached_decompress [-h] [-l CACHE_LOCATION] [-m MAX_SIZE] archiveFile

The program computes a shallow hash of the file (using its name, size, and last modified date). This hash is the key used in the cache for the file. To decompress archives it relies on external command line programs as determined by the file's extension. If the cache creates an entry and exceeds its max size, it removes entries starting with the least recently accessed. 

Note: In the event of a power failure or other event that kills the program during decompression, it should fail to write the metadata files. On the next run it will remove any entries with missing metadata and warn you about them on stderr. Things should then proceed without issue.

#Configuration
After first run, it creates a config file at HOME/.config/decompression_cache.conf. Here you can set the default max cache size, which will start at 1G.

#Dependencies
- Python 2.7
- tar (for tar.* files)
- zcat (for .gz files)
- unzip (for .zip files)
- xzcat (for .xz files)